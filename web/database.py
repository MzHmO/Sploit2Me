import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

DATABASE = "database.db"

class User:
    def __init__(self, id, username, email=None):
        self.id = id
        self.username = username
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_email(self):
        return str(self.email)

    def get_username(self):
        return str(self.username)

    def check_password(self, password):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (self.username,))
        data = cursor.fetchone()
        conn.close()

        if data is None:
            return False

        password_hash = data['password']
        return check_password_hash(password_hash, password)


class Database:
    @staticmethod
    def Connect(db_name=DATABASE):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def setup_db():
        conn = Database.Connect(db_name=DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            cardsfilter TEXT NOT NULL
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chatid INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            tgfilter TEXT NOT NULL,
            enable INTEGER
        );
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def add_chat(chatid, username):
        conn = Database.Connect(db_name=DATABASE)
        cursor = conn.cursor()
        filter = ""
        cursor.execute("INSERT INTO chats (chatid, username, tgfilter, enable) VALUES (?, ?, ?, ?)", (chatid, username, filter, 0))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_chat_ids():
        conn = Database.Connect(db_name=DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT chatid FROM chats")
        chatids = [row['chatid'] for row in cursor.fetchall()]
        conn.close()
        return chatids

    @staticmethod
    def chat_exists(chatid):
        conn = Database.Connect(db_name=DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM chats WHERE chatid = ?", (chatid,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @staticmethod
    def apply_tg_filter(username, filter_value):
        conn = Database.Connect(db_name=DATABASE)

        try:
            if (username[0] == "@"):
                username = username[1:]
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE chats 
                SET tgfilter = ?, enable = 1 
                WHERE username = ?;
            """, (filter_value, username))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
        except Exception as e:
            logging.error(f"Exception in check_and_send_message: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        return User(id=data['id'], username=data['username'], email=data['email'])

    @staticmethod
    def get_user_by_email(email):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        return User(id=data['id'], username=data['username'], email=data['email'])

    @staticmethod
    def get_user_by_username(username):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        return User(id=data['id'], username=data['username'], email=data['email'])

    @staticmethod
    def register_user(username, password, email):
        conn = Database.Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))

        user = cursor.fetchone()

        if user:
            conn.close()
            return 'Имя пользователя занято', False

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))

        user = cursor.fetchone()

        if user:
            conn.close()
            return 'Почта уже используется другим аккаунтом', False
        
        filter = ""

        cursor.execute("INSERT INTO users (username, password, email, cardsfilter) VALUES (?, ?, ?, ?)",
                       (username, generate_password_hash(password), email, filter))

        conn.commit()
        conn.close()

        user_folder = os.path.join(os.getcwd(), 'files', str(cursor.lastrowid))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        return 'User successfully registered', True

    @staticmethod
    def validate_login_by_username(username, password):
        user = Database.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def validate_login_by_email(email, password):
        user = Database.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def change_password(username, old_password, password):
        user = Database.get_user_by_username(username)
        if user.check_password(old_password):
            conn = Database.Connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE username = ?;
                """,
                (generate_password_hash(password), username)
            )


            conn.commit()
            conn.close()
            return 'Password changed successfully', True
        return 'Wrong user password', False