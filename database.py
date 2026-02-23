import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="bot_database.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                is_subscribed INTEGER DEFAULT 1
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                text TEXT,
                timestamp TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                text TEXT,
                timestamp TEXT
            )
        """)

        self.conn.commit()

    def add_user(self, user_id, full_name):
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, full_name, is_subscribed) VALUES (?, ?, 1)", 
            (user_id, full_name)
        )
        self.conn.commit()

    def set_subscription(self, user_id, status: bool):
        self.cursor.execute(
            "UPDATE users SET is_subscribed = ? WHERE user_id = ?", 
            (1 if status else 0, user_id)
        )
        self.conn.commit()

    def get_subscribed_users(self):
        self.cursor.execute("SELECT user_id FROM users WHERE is_subscribed = 1")
        return [row[0] for row in self.cursor.fetchall()]

    def add_feedback(self, user_id, user_name, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO feedback (user_id, user_name, text, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, user_name, text, timestamp)
        )
        self.conn.commit()

    def add_error_report(self, user_id, user_name, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO error_report (user_id, user_name, text, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, user_name, text, timestamp)
        )
        self.conn.commit()

db = Database()