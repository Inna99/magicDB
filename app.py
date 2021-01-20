from PyQt5 import QtWidgets, uic

from config import UI_MAIN_WINDOW, DESIGN_DIR

from database.connection import Database

# Read more at
# https://doc.bccnsoft.com/docs/PyQt5/designer.html#using-the-generated-code
Ui_MainWindow, _ = uic.loadUiType(UI_MAIN_WINDOW, import_from=DESIGN_DIR)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.db = Database()
        self.movies_list.setAcceptRichText(True)
        self.btn_create_movie.pressed.connect(self.printMovies)

    def printMovies(self):
        self.movies_list.clear()
        cursor = self.movies_list.textCursor()
        cursor.insertHtml('<ul>')
        for movie in range(15):
            self.movies_list.append(f'<li>{movie}</li>')
        cursor.insertHtml('</ul>')
