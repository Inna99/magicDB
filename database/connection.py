import sqlite3
import os
from datetime import date
from config import BASE_DIR

class Database():
    DB_PATH: str = os.path.abspath(os.path.join(BASE_DIR, 'db.db'))

    def __init__(self):
        self.connection = sqlite3.connect(self.DB_PATH)
        print('connection created', self.connection)
        self.create_table()
        self.create_movies()
        self.get_movies()
        #self.delete_movies()
        self.update_movies()

    #  создание таблицы
    def create_table(self):
        cursor: sqlite3.cursor = self.connection.cursor()
        cursor.execute('''create table if not exists movies 
                        (id integer primary key AUTOINCREMENT, 
                        title string not null,
                        production_year date,
                        viewed boolean default false)
                        ''')

    #  заполнение таблицы
    def create_movies(self):
        cursor: sqlite3.cursor = self.connection.cursor()
        cursor.execute('''insert into movies (title, production_year)
                        values (?, ?) 
                        ''', ["Великий Гэтсби", date.fromisoformat('2013-01-01')])
        self.connection.commit()

    #  извлечение всех записей из таблицы
    def get_movies(self):
        cursor: sqlite3.cursor = self.connection.cursor()
        movies = cursor.execute("SELECT * from movies").fetchall()
        print(movies)

    #  удаление
    def delete_movies(self):
        cursor: sqlite3.cursor = self.connection.cursor()
        cursor.execute("delete from movies where production_year = '2013-01-01'")
        self.connection.commit()

    # изменение
    def update_movies(self):
        cursor: sqlite3.cursor = self.connection.cursor()
        cursor.execute("update movies set production_year = '2013-02-02' where production_year = '2013-01-01'")
        self.connection.commit()
