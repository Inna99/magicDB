from functools import wraps
from typing import List
from PyQt5 import QtWidgets, uic
from datetime import date
from config import UI_MAIN_WINDOW, DESIGN_DIR
from database.connection_orm import Movies, Connect

Ui_MainWindow, _ = uic.loadUiType(UI_MAIN_WINDOW, import_from=DESIGN_DIR)
Item = QtWidgets.QTableWidgetItem  # shortcut


def print_movies_from_db(self):
    self.clear_table()
    self.movies_list.setHorizontalHeaderLabels(["title", "year", "viewed"])
    self.id_dict = {}
    for row, movie in enumerate(Movies.select()):
        self.id_dict[row] = movie.id
        self.movies_list.insertRow(self.movies_list.rowCount())
        self.movies_list.setItem(row, 0, Item(movie.title))
        self.movies_list.setItem(row, 1, Item(str(movie.production_year)))
        self.movies_list.setItem(row, 2, Item(str(movie.viewed)))
    print(self.id_dict)


def refresh_table(func):
    print('Decorator was called', func.__name__)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print('wrapper called')
        result = func(self, *args, **kwargs)
        print('func called', func.__name__)
        print_movies_from_db(self)
        return result
    return wrapper


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    movies_list: QtWidgets.QTabWidget
    copied_row: List[str] = []
    column_name = ('title', 'production_year', 'viewed')

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.db = Connect()
        self.columns = Movies._meta.fields.keys()
        self.setupUi(self)
        self.btn_update_movies.pressed.connect(lambda: print_movies_from_db(self))
        self.btn_create_movie.pressed.connect(self.add_movie)
        #  self.btn_delete_by_id.pressed.connect(self.delete_by_id)
        #  self.create_table()
        self.create_menu()
        self.movies_list.itemChanged.connect(self.item_changed)
        self.movies_list.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.id_dict = {}  # можно использовать список /  можно удалить отсюда
        print_movies_from_db(self)
        self.cell_data = ()


    #  @refresh_table
    def item_changed(self, item: QtWidgets.QTableWidgetItem):

        if self.column_name[item.column()] == 'title':
            field = {self.column_name[item.column()]: item.text()}  # field for change {id: 'value'}
            result = Movies.update(**field).where(Movies.id == self.id_dict[item.row()]).execute()
            #  result = Movies.update(title=item.text()) не работает
        elif self.column_name[item.column()] == 'production_year':
            try:
                #  подключить виджет для корректного ввода данных?
                field = {self.column_name[item.column()]: item.text()}
                result = Movies.update(**field).where(Movies.id == self.id_dict[item.row()]).execute()
            except Exception:  #  peewee.
                self.create_qmessage_box_without_choice('', "Неправильый формат даты\nправильно ГГГГ-ММ-ДД")
        elif self.column_name[item.column()] == 'viewed':
            field = {self.column_name[item.column()]: item.text() == 'True'}
            result = Movies.update(**field).where(Movies.id == self.id_dict[item.row()]).execute()

    def clear_table(self):
        self.movies_list.clear()
        self.movies_list.setRowCount(0)
        #  self.create_table()

    @refresh_table
    def add_movie(self):
        """ button btn_create_movie """
        line_title = self.line_title.text()
        line_production_year = self.line_production_year.text()
        viewed = self.checkBox_viewed.isChecked()
        if "" not in [line_title, line_production_year]:
            self.line_title.clear()
            self.line_production_year.clear()
            self.checkBox_viewed.setChecked(False)
            Movies.create(title=line_title, production_year=date(int(line_production_year), 1, 1), viewed=viewed)

    @refresh_table
    def delete_by_id(self, id_row):
        """ button btn_delete_by_id """
        # if id_row == -1:
        #     id_row = Movies.select().order_by(Movies.id.desc()).get()

        Movies.select().where(Movies.id == id_row).get().delete_instance()

    @refresh_table
    def add_row(self, movie: Movies = None) -> Movies:
        return Movies.create(title='Null', production_year=date(1900, 1, 1), viewed=False)

    # def create_table(self):
    #     for i, column in enumerate(self.columns):
    #         self.movies_list.setHorizontalHeaderItem(i, Item(column))

    def delete_row(self):
        if len(self.id_dict) != 0:
            row = self.movies_list.currentRow()
            id_row = self.id_dict[row]
            self.delete_by_id(id_row)
        else:
            self.create_qmessage_box_without_choice('', 'Записей в базе нет')

    def clear_all(self):
        if self.create_qmessage_box('', 'Вы уверены?'):
            Movies.delete().execute()
            self.clear_table()

    def create_menu(self):
        """
        Set up the menu bar.
        """
        # Create file menu actions
        quit_act = QtWidgets.QAction("Quit", self)
        quit_act.setShortcut('Ctrl+Q')
        quit_act.triggered.connect(self.close)
        # Create table menu actions
        self.add_row_act = QtWidgets.QAction("Add Row", self)
        self.add_row_act.triggered.connect(self.add_row)
        self.delete_row_act = QtWidgets.QAction("Delete Row", self)
        self.delete_row_act.triggered.connect(self.delete_row)
        self.clear_table_act = QtWidgets.QAction("Clear All", self)
        self.clear_table_act.triggered.connect(self.clear_all)
        # Create the menu bar
        menu_bar = self.menu_bar
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(quit_act)
        # Create table menu and add actions
        table_menu = menu_bar.addMenu('Table')
        table_menu.addAction(self.add_row_act)
        table_menu.addSeparator()
        table_menu.addAction(self.delete_row_act)
        # table_menu.addAction(self.delete_col_act)
        table_menu.addSeparator()
        table_menu.addAction(self.clear_table_act)

    @refresh_table
    def paste_item(self):
        """
        self.cells_data = (kghckhg, 2000-05-05, False)
        """
        # new_row_index = self.movies_list.rowCount() + 1
        print(self.cells_data)
        Movies.create(**self.cells_data)
        # for column, cell_data in enumerate(self.cells_data):
        #     self.movies_list.setItem(new_row_index, column, QtWidgets.QTableWidgetItem(cell_data))

    def copy_item(self):
        copied_row = sorted(self.movies_list.selectedIndexes())
        # self.cells_data = (cell.data() for cell in copied_row)
        # self.cells_data = {k: v.data() for v in copied_row for k in self.column_name}

    def contextMenuEvent(self, event):
        """
        Create context menu and actions.
        """
        context_menu = QtWidgets.QMenu(self)
        context_menu.addAction(self.add_row_act)
        context_menu.addSeparator()
        context_menu.addAction(self.delete_row_act)
        # context_menu.addAction(self.delete_col_act)
        context_menu.addSeparator()
        copy_act = context_menu.addAction("Copy")
        paste_act = context_menu.addAction("Paste")
        context_menu.addSeparator()
        context_menu.addAction(self.clear_table_act)

        """
        # Execute the context_menu and return the action selected.
        mapToGlobal() translates the position of the window coordinates to
        the global screen coordinates. This way we can detect if a rightclick
        occurred inside of the GUI and display the context menu.
        # To check for actions selected in the context menu that were not
        created in the menu bar.
        """
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_act:
            self.copy_item()
        if action == paste_act:
            self.paste_item()

    def create_qmessage_box(self, title: str, msg: str) -> bool:

        reply = QtWidgets.QMessageBox.question(self, title, msg, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                               QtWidgets.QMessageBox.No)
        return reply == QtWidgets.QMessageBox.Yes

    def create_qmessage_box_without_choice(self, title: str, msg: str):
        QtWidgets.QMessageBox.question(self, title, msg, QtWidgets.QMessageBox.Ok,
                                       QtWidgets.QMessageBox.Ok)

