import model
from typing import List
from sqlite3 import Connection, Cursor, DatabaseError
from contextlib import contextmanager
from loguru import logger


class Database:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.logger = logger
        self.create_tables()

    def model_factory(self, model_class):
        def factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return model_class(**{k: v for k, v in zip(fields, row)})

        return factory

    # @contextmanager
    # def get_cursor(self):
    #     cursor = self.conn.cursor()
    #     try:
    #         yield cursor
    #         self.conn.commit()
    #     except Exception as e:
    #         self.conn.rollback()
    #         self.logger.error(f"Database operation failed: {str(e)}")
    #         raise DatabaseError(f"Database operation failed: {str(e)}") from e
    #     finally:
    #         cursor.close()

    def create_tables(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                email TEXT,
                UNIQUE (name)
            )
            """
            )
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                in_stock INTEGER
            )
            """
            )
            self.conn.commit()
            self.logger.info("Tables created or verified successfully")

    def insert_user(self, user: model.User):
        assert isinstance(user, model.User), "input must be of type 'User'"
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
                (user.name, user.age, user.email),
            )
            self.logger.info(f"Inserted user: {user}")

    def get_all_users(self) -> List[model.User]:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.row_factory = self.model_factory(model.User)
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

            assert not rows or isinstance(
                rows[0], model.User
            ), "The function must return a list of Users"
            return rows
