from db.db import execute_out


def select_from(_select, _from):
    return execute_out('''
                          SELECT {} FROM {}'''
                       .format(_select, _from))


def select_from_where(_select, _from, _where):
    return execute_out('''
                          SELECT {} FROM {} WHERE {}'''
                       .format(_select, _from, _where))


def read_authors():
    return select_from('*', 'Авторы')


def read_books():
    return select_from('*', 'Книги')


def read_books_by_author_id(author_id):
    return select_from_where('*', 'Книги',
                             '`id автора` = {}'.format(author_id))


def read_books_with_author():
    return select_from('''Книги.id,
                          имя,
                          название,
                         `количество страниц`,
                          издательство,
                         `год издания`''',
                       '''Авторы
                          JOIN Книги
                          ON Авторы.id = Книги.`id автора`''')