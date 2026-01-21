import sqlite3
from pathlib import Path

DIR_DATA = Path("/app/data")
PATH_DB = DIR_DATA / "budget.db"

def get_connection():
    """
    Retrun a SQLite connection.
    Create the database if it does not exist.
    """
    return sqlite3.connect(PATH_DB)

def init_db():
    """
    Initializes the database schema.
    Safe to run multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_transaction TEXT NOT NULL,
            amount REAL NOT NULL,
            merchant TEXT,
            description TEXT,
            account TEXT,
            institution TEXT,
            category TEXT,
            subcategory TEXT,
            label TEXT,
            source_file TEXT,
            date_imported TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()
