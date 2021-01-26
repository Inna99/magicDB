from PyQt5 import QtWidgets, uic
from datetime import date
from config import UI_MAIN_WINDOW, DESIGN_DIR

# from database.connection import Database
from database.connection_orm import Movies, db

# Read more at
# https://doc.bccnsoft.com/docs/PyQt5/designer.html#using-the-generated-code
Ui_MainWindow, _ = uic.loadUiType(UI_MAIN_WINDOW, import_from=DESIGN_DIR)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        db.connect()
        db.create_tables([Movies])
        self.setupUi(self)
        #self.db = Movies()
        self.movies_list.setAcceptRichText(True) #  ?????????77
        self.btn_update_movies.pressed.connect(self.printMovies)
        self.btn_create_movie.pressed.connect(self.addMovie)


    def addMovie(self):
        line_title = self.line_title.text()
        line_production_year = self.line_production_year.text()
        viewed = self.checkBox_viewed.isChecked()
        movie = Movies(title=line_title, production_year=date(int(line_production_year), 1, 1), viewed=viewed)
        movie.save()

    def printMovies(self):
        print(list(Movies.select().dicts()))
        self.movies_list.clear()
        cursor = self.movies_list.textCursor()
        cursor.insertHtml('<ul>')
        for movie in Movies.select().dicts():
            self.movies_list.append(f'<li>{movie}</li>')
        cursor.insertHtml('</ul>')
