from PyQt5 import QtWidgets, uic
from datetime import date
from config import UI_MAIN_WINDOW, DESIGN_DIR

# from database.connection import Database
from database.connection_orm import Movies, Connect

# Read more at
# https://doc.bccnsoft.com/docs/PyQt5/designer.html#using-the-generated-code
Ui_MainWindow, _ = uic.loadUiType(UI_MAIN_WINDOW, import_from=DESIGN_DIR)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.db = Connect()
        self.setupUi(self)
        self.movies_list.setAcceptRichText(True)  # ?
        self.btn_update_movies.pressed.connect(self.printMovies)
        self.btn_create_movie.pressed.connect(self.addMovie)
        self.btn_delete_by_id.pressed.connect(self.deleteById)


    def addMovie(self):
        line_title = self.line_title.text()
        line_production_year = self.line_production_year.text()
        viewed = self.checkBox_viewed.isChecked()
        # movie = Movies(title=line_title, production_year=date(int(line_production_year), 1, 1), viewed=viewed)
        # movie.save()
        # ??? почему не так
        Movies(title=line_title, production_year=date(int(line_production_year), 1, 1), viewed=viewed).save()
        Movies.create(title=line_title, production_year=date(int(line_production_year), 1, 1), viewed=viewed)

        self.printMovies()
        self.line_title.clear()
        self.line_production_year.clear()
        print(self.checkBox_viewed.setChecked(False))

    def printMovies(self):
        self.movies_list.clear()
        cursor = self.movies_list.textCursor()
        cursor.insertHtml('<ul>')
        for movie in Movies.select().dicts():
            # '<li>' +
            self.movies_list.append(f'{movie["title"]} {movie["production_year"].year} {"Просмотрено" if movie["viewed"] == True else "Непросмотрено"}')
        cursor.insertHtml('</ul>')

    def deleteById(self):
        delete_id = Movies.select().order_by(Movies.id)[-1]
        Movies.delete().where(Movies.id == delete_id).execute()
        self.printMovies()
