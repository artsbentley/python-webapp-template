import sqlite3
import atexit
import model
import database
from loguru import logger


def main():
    conn = sqlite3.connect("app.db")
    atexit.register(lambda: conn.close())

    db = database.Database(conn, logger)

    user = model.User(name="Arno", age=28, email="arnoarts@hotmail.com")
    db.insert_user(user)

    users = db.get_all_users()
    for user in users:
        print(user.age)


if __name__ == "__main__":
    main()
