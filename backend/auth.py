import hashlib
import hmac
import secrets
import uuid


USERS = {}
SESSIONS = {}


def _password_hash(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return salt.hex(), digest.hex()


def create_user(name, email, password):
    key = email.strip().lower()
    if key in USERS:
        return None
    salt, digest = _password_hash(password)
    user = {"id": uuid.uuid4().hex, "name": name.strip(), "email": key, "salt": salt, "password": digest}
    USERS[key] = user
    return user


def authenticate(email, password):
    user = USERS.get(email.strip().lower())
    if not user:
        return None
    salt, digest = _password_hash(password, bytes.fromhex(user["salt"]))
    if not hmac.compare_digest(digest, user["password"]):
        return None
    return user


def create_session(user):
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = user["id"]
    return token


def get_user(token):
    user_id = SESSIONS.get(token)
    return next((user for user in USERS.values() if user["id"] == user_id), None)


def delete_session(token):
    SESSIONS.pop(token, None)