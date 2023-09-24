import sqlite3


def create_connection():
    try:
        connection = sqlite3.connect('db.sqlite3', check_same_thread=False)
        execute_query(connection, """
        CREATE TABLE IF NOT EXISTS todo (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          task TEXT NOT NULL
        );
        """)
        return connection

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def execute_select_query(connection):
    try:
        cursor = connection.cursor()
        sqlite_select_query = """SELECT * from todo;"""
        cursor.execute(sqlite_select_query)
        total_rows = cursor.fetchall()
        cursor.close()
        return total_rows

    except sqlite3.Error as error:
        print("Ошибка", error)


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка", error)


def delete_query(task_id): return f"DELETE from todo WHERE id = '{task_id}';"


def update_query(task, task_id): return f"UPDATE todo SET task = '{task}' WHERE id = '{task_id}';"


def insert_query(task): return f"INSERT INTO `todo` (task) VALUES ('{task}');"
