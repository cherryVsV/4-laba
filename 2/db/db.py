import sqlite3

DBNAME = r'library.db'


def connect_to_database():
    return sqlite3.connect(DBNAME)


def _execute(cursor, request):
    try:
        cursor.execute(request)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        print(request)
        exit(1)


def execute_out(request):
    with connect_to_database() as db:
        cursor = db.cursor()
        _execute(cursor, request)
        return cursor.fetchall()


def execute_in(request):
    with connect_to_database() as db:
        cursor = db.cursor()
        _execute(cursor, request)
        db.commit()