from db.db import execute_in


def insert_into_values(_into, _values):
    execute_in('''
                  INSERT into {} values ({})'''
               .format(_into, _values))


def insert_author(name, country, years):
    insert_into_values('Авторы (имя, страна, `годы жизни`)',
                       ','.join(map(repr, (name,
                                           country,
                                           years))))


def insert_book(author_id, title, pages_count, publisher, publishing_year):
    insert_into_values('''Книги (`id автора`,
                            название,
                           `количество страниц`,
                            издательство,
                           `год издания`)''',
                       ','.join(map(repr, (author_id,
                                           title,
                                           pages_count,
                                           publisher,
                                           publishing_year))))
