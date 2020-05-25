import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Author(Base):
    __tablename__ = 'Авторы'

    id = Column(Integer, primary_key=True)
    name = Column(String, name='Имя')
    country = Column(String, name='Страна')
    years = Column(String, name='Годы_жизни')

    def __repr__(self):
        return "<Author(id={}, name='{}', country='{}', years='{}')>" \
            .format(self.id, self.name, self.country, self.years)


class Book(Base):
    __tablename__ = 'Книги'

    author_id = Column(Integer, ForeignKey('Авторы.id'), name='id_автора')
    title = Column(String, primary_key=True, name='Название')
    sheets_count = Column(Integer, name='Количество_страниц')
    publisher = Column(String, name='Издательство')
    year = Column(Integer, name='Год_издания')

    def __repr__(self):
        return "<Author(author_id={}, title='{}', sheets_count={}," \
               " publisher='{}', year={})>" \
            .format(self.author_id, self.title, self.sheets_count,
                    self.publisher, self.year)


class User(Base):
    __tablename__ = 'Пользователи'
    login = Column(String, primary_key=True, name='Логин')
    password = Column(String, name='Пароль')

    def __repr__(self):
        return "<User(login='{}', password='{}'".format(self.login, self.password)


"""
-----------------------------------------------------------------------------------
"""


def task1(ses):
    print('First task: вывод фамилий всех авторов, родившихся в диапазоне '
          'между X и Y годами (задайте программно числа X и Y)')
    for author in ses.query(Author):
        birth = int(author.years.split('-')[0])
        if 1900 < birth < 1950:
            print(author.name)
    print()


def task2(ses):
    print('Second task: вывод всех книг, написанных авторами из России')
    authors = ses.query(Author).filter(Author.country == 'Россия' or Author.country == 'Russia')
    for author in authors:
        books = ses.query(Book).filter(Book.author_id == author.id)
        for book in books:
            print(book.title)
    print()


def task3(ses):
    print('Third task: вывод всех книг с количеством страниц более N')
    books = ses.query(Book).filter(Book.sheets_count > 200)
    for book in books:
        print(book.title)
    print()


def task4(ses):
    print('Fourth task: вывод всех книг с количеством страниц более N')
    for author in ses.query(Author):
        books = list(ses.query(Book).filter(Book.author_id == author.id))
        if len(books) > 2:
            print(author.name)
    print()


def main():
    engine = sqlalchemy.create_engine('sqlite:///Library.db', echo=False)
    Session = sessionmaker(bind=engine)
    sessia = Session()

    task1(sessia)
    task2(sessia)
    task3(sessia)
    task4(sessia)

    sessia.close()


if __name__ == '__main__':
    main()
