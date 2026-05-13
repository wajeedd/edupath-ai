import sqlite3
import hashlib


def init_db():

    conn = sqlite3.connect("edupath.db")

    cursor = conn.cursor()

    cursor.executescript("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

        CREATE TABLE IF NOT EXISTS sessions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            subject TEXT,

            scores_json TEXT,

            weak_concepts_json TEXT,

            taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES users(id)

        );

    """)

    conn.commit()

    conn.close()


def hash_password(password: str) -> str:

    return hashlib.sha256(
        password.encode()
    ).hexdigest()