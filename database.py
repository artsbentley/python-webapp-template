import model


class Database:
    def __init__(self, sqlite_connection, logger):
        self.conn = sqlite_connection
        self.logger = logger
        self.create_tables()

    def model_factory(self, model_class):
        def factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return model_class(**{k: v for k, v in zip(fields, row)})

        return factory

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            email TEXT
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
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            (user.name, user.age, user.email),
        )
        self.conn.commit()
        self.logger.info(f"Inserted user: {user}")

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.row_factory = self.model_factory(model.User)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        self.logger.info("Fetched all users")
        return rows
