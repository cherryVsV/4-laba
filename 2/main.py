from db import reader, writer
from db.init import init_database
from auth import User
from view_info import Ui_ViewInfo
from add_author_dialog import Ui_AddAuthorDialog
from add_book_dialog import Ui_AddBookDialog
from auth_dialog import Ui_AuthDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import loaders
import sys


class AuthDialog(QDialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_AuthDialog()
        self.ui.setupUi(self)

    def accept(self):
        user = User(self.ui.login.text(),
                    self.ui.password.text())
        QDialog.accept(self)

    def reject(self):
        QDialog.reject(self)
        exit(0)


class AddAuthorDialog(QDialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.new_item = None
        self.ui = Ui_AddAuthorDialog()
        self.ui.setupUi(self)

    def accept(self):
        birth_year = self.ui.birth_year.text()
        death_year = self.ui.death_year.text()
        self.new_item = (self.ui.name.text(),
                         self.ui.country.text(),
                         '-'.join((birth_year,
                                   death_year))
                         if len(death_year) > 0
                         else birth_year)
        writer.insert_author(*self.new_item)
        self.close()


class AddBookDialog(QDialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.new_item = None
        self.ui = Ui_AddBookDialog()
        self.ui.setupUi(self)
        self.author_id_list = list()
        for _id, name in reader.select_from('id, имя', 'Авторы'):
            self.ui.author.addItem(name)
            self.author_id_list.append(_id)

    def accept(self):
        author_id = self.author_id_list[self.ui.author.currentIndex()]
        self.new_item = (self.ui.author.currentText(),
                         self.ui.title.text(),
                         self.ui.pages_count.value(),
                         self.ui.publisher.text(),
                         self.ui.publishing_year.value())
        writer.insert_book(author_id, *self.new_item[1:])
        self.close()


class MyForm(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_ViewInfo()
        self.ui.setupUi(self)
        self.reload()
        self.nameFilters = {'JSON (*.json)': loaders.json_loader,
                            'XML (*.xml)': loaders.xml_loader}

    @staticmethod
    def _append_items(model, items):
        model.appendRow(filter(lambda x: x.setEditable(False) or True,
                               map(lambda x: QStandardItem(str(x)), items)))

    @staticmethod
    def _load_authors(model):
        for author_id, *author in reader.read_authors():
            MyForm._append_items(model, author)

    @staticmethod
    def _load_books(model):
        for book_id, *book in reader.read_books_with_author():
            MyForm._append_items(model, book)

    def _init_authors(self):
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(['Имя',
                                         'Страна',
                                         'Годы жизни'])
        MyForm._load_authors(model)
        self.ui.authors.setModel(model)

    def _init_books(self):
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(['Автор',
                                         'Название',
                                         'Количество страниц',
                                         'Издательство',
                                         'Год издания'])
        MyForm._load_books(model)
        self.ui.books.setModel(model)

    def add_author(self):
        dialog = AddAuthorDialog(self)
        dialog.exec()
        if dialog.new_item is not None:
            MyForm._append_items(self.ui.authors.model(), dialog.new_item)

    def add_book(self):
        dialog = AddBookDialog(self)
        dialog.exec()
        if dialog.new_item is not None:
            MyForm._append_items(self.ui.books.model(), dialog.new_item)

    def reload(self):
        self._init_authors()
        self._init_books()

    def import_authors(self):
        dialog = QFileDialog(self)
        dialog.setNameFilters(self.nameFilters.keys())
        if dialog.exec():
            with open(dialog.selectedFiles()[0], 'rt') as file:
                loader = self.nameFilters[dialog.selectedNameFilter()]
                for name, country, years in loader.load(file.read()):
                    writer.insert_author(name, country, years)
                    MyForm._append_items(self.ui.authors.model(),
                                         (name, country, years))

    def export_authors(self):
        indexes = self.ui.authors.selectedIndexes()
        if len(indexes) < 1:
            return
        dialog = QFileDialog(self)
        dialog.setNameFilters(self.nameFilters.keys())
        dialog.setAcceptMode(dialog.AcceptSave)
        if dialog.exec():
            loader = self.nameFilters[dialog.selectedNameFilter()]
            with open(dialog.selectedFiles()[0], 'wt') as file:
                model = self.ui.authors.model()
                name, country, years = (model.item(indexes[0].row(), _).text()
                                        for _ in range(model.columnCount()))
                file.write(loader.dump(name, country, years))


if __name__ == '__main__':
    init_database()
    app = QApplication(sys.argv)
    form = MyForm()
    auth_dialog = AuthDialog(form)
    auth_dialog.exec()
    form.show()
    try:
        sys.exit(app.exec_())
    except SystemExit as se:
        print('Program has exited with code {}'.format(se))