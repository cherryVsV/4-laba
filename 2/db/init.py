import sqlite3
from db.db import connect_to_database

def _create_database():
    with connect_to_database() as db:
        cursor = db.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Авторы(`id` INTEGER PRIMARY KEY,
                                                  `имя` TEXT,
                                                  `страна` TEXT,
                                                  `годы жизни` TEXT)
            ''')
        db.commit()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Книги(`id` INTEGER PRIMARY KEY,
                                                 `id автора` INTEGER,
                                                 `название` TEXT,
                                                 `количество страниц` INTEGER,
                                                 `издательство` TEXT,
                                                 `год издания` INTEGER,
                                                  FOREIGN KEY('id автора')
                                                  REFERENCES Авторы(id))
            ''')
        db.commit()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS
                    Пользователи(`id` INTEGER PRIMARY KEY,
                                 `логин` TEXT,
                                 `пароль` TEXT)
            ''')
        db.commit()


def _fill_database():
    authors = ("1|L.N.Tolstoi    |Russia |1828-1910\n"
               "2|F.M.Dostoyevsky|Russia |1821-1881\n"
               "3|B.Vian         |France |1920-1959\n"
               "4|A.Camus        |France |1913-1960\n"
               "5|F.Kafka        |Austria|1883-1924")

    books = ("1|1|War and Peace   |1225|The Russian Messanger|1869\n"
             "2|1|Resurrection    |483 |Niva                 |1899\n"
             "3|2|The Idiot       |678 |The Russian Messanger|1868\n"
             "4|2|The Gambler     |241 |The Moscow Renaisanse|1867\n"
             "5|3|The Foam of days|219 |Gallimard            |1947\n"
             "6|4|The Stranger    |159 |Hamish Hamilton      |1946\n"
             "7|4|The Rebel       |238 |Gallimard            |1951\n"
             "8|5|The Trial       |395 |Verlag Die Schmiede  |1925\n"
             "9|5|Amerika         |351 |Routledge            |1938")

    users = "1|admin|d4d1c9e67f05a7785990dea88020f20a"

    with connect_to_database() as db:
        cursor = db.cursor()

        def fill(table_string, table_name):
            for row_string in table_string.split('\n'):
                values = ','.join(repr(field.strip())
                                  for field in row_string.split('|'))
                cursor.execute('''
                        INSERT OR IGNORE into {} values ({})
                    '''.format(table_name, values))
            db.commit()

        fill(authors, 'Авторы')
        fill(books, 'Книги')
        fill(users, 'Пользователи')


def init_database():
    try:
        _create_database()
        _fill_database()
    except sqlite3.OperationalError as e:
        print(e)
        raise

if __name__ == '__main__':
    init_database()