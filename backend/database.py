import sqlite3
import json

DB_PATH = "data/chat.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            sender TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def load_messages():
    with open("data/messages.json", "r", encoding="utf-8") as f:
        return json.load(f)


def insert_messages():
    messages = load_messages()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages")

    cursor.executemany(
        """
        INSERT INTO messages (id, sender, timestamp, message)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                m["id"],
                m["sender"],
                m["timestamp"],
                m["message"]
            )
            for m in messages
        ]
    )

    conn.commit()
    conn.close()

    print(f"Inserted {len(messages)} messages")


if __name__ == "__main__":
    create_database()
    insert_messages()