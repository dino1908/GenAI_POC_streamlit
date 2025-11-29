import sqlite3
from pathlib import Path

DB_PATH = "chat_history.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        role TEXT,
        content TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def create_chat(name: str = "New chat") -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO chats (name) VALUES (?)", (name,))
    chat_id = cur.lastrowid
    conn.commit()
    conn.close()
    return chat_id


def get_chats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM chats ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_messages(chat_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id",
        (chat_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [{"role": r, "content": c} for (r, c) in rows]


def add_message(chat_id: int, role: str, content: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
        (chat_id, role, content),
    )
    conn.commit()
    conn.close()
