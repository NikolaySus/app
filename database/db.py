"""
Module with database access functions implementations.
"""
import sqlite3

DB_NAME = "evaluation.db"


def get_connection():
    """
    Returns connection.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Eval (
            eval_id INTEGER PRIMARY KEY AUTOINCREMENT,
            eval_name TEXT NOT NULL UNIQUE,
            eval_start_timestamp TEXT,
            eval_finish_timestamp TEXT,
            eval_state TEXT,
            eval_results TEXT
        )
    """)

    conn.commit()
    conn.close()


# Initialize DB on import (acceptable for prototype)
init_db()
