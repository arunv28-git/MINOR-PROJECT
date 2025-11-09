"""
SQLite database helper for user authentication.
This module provides functions to interact with the SQLite database for user management.
"""
import sqlite3
import os
from typing import Optional, Dict, Any

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tripster.db')

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows column access by name
    return conn

def init_user_db():
    """Initialize the users table in SQLite database."""
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create indexes for faster lookups
        conn.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_email ON users(email)")
        conn.commit()
        print("[Info] SQLite users table initialized successfully.")
    except Exception as e:
        print(f"[Error] Failed to initialize users table: {e}")
        raise
    finally:
        conn.close()

def create_user(username: str, email: str, hashed_password: str) -> Optional[int]:
    """
    Create a new user in the database.
    Returns the user ID if successful, None if username/email already exists.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError as e:
        # Username or email already exists
        conn.rollback()
        return None
    except Exception as e:
        print(f"[Error] Failed to create user: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get a user by username. Returns None if not found."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return dict(row)  # Convert Row to dict
        return None
    except Exception as e:
        print(f"[Error] Failed to get user: {e}")
        return None
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get a user by ID. Returns None if not found."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)  # Convert Row to dict
        return None
    except Exception as e:
        print(f"[Error] Failed to get user by ID: {e}")
        return None
    finally:
        conn.close()

def check_username_exists(username: str) -> bool:
    """Check if a username already exists."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None
    finally:
        conn.close()

def check_email_exists(email: str) -> bool:
    """Check if an email already exists."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        return cursor.fetchone() is not None
    finally:
        conn.close()



