import hashlib
import hmac
import os
import sqlite3
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_DB_PATH = Path(os.getenv("CHATSENSE_AUTH_DB", BASE_DIR / "data" / "chat.db"))
SESSION_DAYS = 30


def _connect():
    connection = sqlite3.connect(AUTH_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _initialise_database():
    AUTH_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                salt TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )


_initialise_database()


def _password_hash(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return salt.hex(), digest.hex()


def create_user(name, email, password):
    key = email.strip().lower()
    salt, digest = _password_hash(password)
    user = {
        "id": secrets.token_hex(16),
        "name": name.strip(),
        "email": key,
        "salt": salt,
        "password": digest,
    }
    try:
        with _connect() as connection:
            connection.execute(
                """
                INSERT INTO users (id, name, email, salt, password, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user["id"], user["name"], user["email"], user["salt"], user["password"], _now()),
            )
    except sqlite3.IntegrityError:
        return None
    return user


def authenticate(email, password):
    with _connect() as connection:
        user_row = connection.execute(
            "SELECT id, name, email, salt, password FROM users WHERE email = ? COLLATE NOCASE",
            (email.strip(),),
        ).fetchone()
    user = dict(user_row) if user_row else None
    if not user:
        return None
    salt, digest = _password_hash(password, bytes.fromhex(user["salt"]))
    if not hmac.compare_digest(digest, user["password"]):
        return None
    return user


def create_session(user):
    token = secrets.token_urlsafe(32)
    with _connect() as connection:
        connection.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (_token_hash(token), user["id"], (datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)).isoformat()),
        )
    return token


def get_user(token):
    if not token:
        return None
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT users.id, users.name, users.email, users.salt, users.password
            FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.token_hash = ? AND sessions.expires_at > ?
            """,
            (_token_hash(token), _now()),
        ).fetchone()
    return dict(row) if row else None


def delete_session(token):
    with _connect() as connection:
        connection.execute("DELETE FROM sessions WHERE token_hash = ?", (_token_hash(token),))


def _now():
    return datetime.now(timezone.utc).isoformat()


def _token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()