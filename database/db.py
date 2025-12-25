"""
Модуль с реализацией функций доступа к базе данных.
"""
import sqlite3

DB_NAME = "evaluation.db"


def get_connection():
    """
    Возвращает соединение с базой данных.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Инициализация базы данных.
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


# Инициализация БД при импорте (допустимо для прототипа)
init_db()
