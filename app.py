from PyQt5 import QtWidgets, uic
from datetime import date
from config import UI_MAIN_WINDOW, DESIGN_DIR
from PyQt5.QtCore import QDate

# from database.connection import Database
from database.connection_orm import Movies, Connect, db

# Read more at
# https://doc.bccnsoft.com/docs/PyQt5/designer.html#using-the-generated-code
Ui_MainWindow, _ = uic.loadUiType(UI_MAIN_WINDOW, import_from=DESIGN_DIR)
Item = QtWidgets.QTableWidgetItem  # shortcut


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    movies_list: QtWidgets.QTabWidget

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.db = Connect()
        self.columns = Movies._meta.fields.keys()
        self.setupUi(self)
        self.btn_update_movies.pressed.connect(self.printMovies)
        self.btn_create_movie.pressed.connect(self.addMovie)
        self.btn_delete_by_id.pressed.connect(self.deleteById)
        self.createTable()
        self.createMenu()
        self.printMovies()
        self.movies_list.itemChanged.connect(self.item_changed)

    def item_changed(self, item: QtWidgets.QTableWidgetItem):
        print(f"item changed {item.row()} {item.column()}")  # item.text() - value

    def addMovie(self):
        line_title = self.line_title.text()
        line_production_year = self.line_production_year.text()
        viewed = self.checkBox_viewed.isChecked()
        Movies.create(title=line_title, production_year=date(int(line_production_year), 1, 1), viewed=viewed)

        self.printMovies()
        self.line_title.clear()
        self.line_production_year.clear()
        self.checkBox_viewed.setChecked(False)


    def clearTable(self):
        self.movies_list.clear()
        self.movies_list.setRowCount(0)
        self.createTable()

    def addRow(self, movie: Movies = None) -> None:
        self.movies_list.insertRow(self.movies_list.rowCount())

    def printMovies(self):
        self.clearTable()
        for row, movie in enumerate(Movies.select()):
            self.addRow()
            self.movies_list.setItem(row, 0, Item(movie.title))
            self.movies_list.setItem(row, 1, Item(str(movie.production_year)))
            self.movies_list.setItem(row, 2, Item(str(movie.viewed)))

    def deleteById(self):
        Movies.select().order_by(Movies.id.desc()).get().delete_instance()
        self.printMovies()

    def createTable(self):
        for i, column in enumerate(self.columns):
            self.movies_list.setHorizontalHeaderItem(i, Item(column))

    def deleteRow(self):
        row = self.movies_list.currentRow()
        self.movies_list.removeRow(row)

    def createMenu(self):

        """
        Set up the menu bar.
        """
        # Create file menu actions
        quit_act = QtWidgets.QAction("Quit", self)
        quit_act.setShortcut('Ctrl+Q')
        quit_act.triggered.connect(self.close)
        # Create table menu actions
        self.add_row_act = QtWidgets.QAction("Add Row", self)
        self.add_row_act.triggered.connect(self.addRow)
        self.delete_row_act = QtWidgets.QAction("Delete Row", self)
        self.delete_row_act.triggered.connect(self.deleteRow)
        self.clear_table_act = QtWidgets.QAction("Clear All", self)
        self.clear_table_act.triggered.connect(self.clearTable)
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

    def pasteItem(self):
        ...

    def copyItem(self):
        ...

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
            self.copyItem()
        if action == paste_act:
            self.pasteItem()
