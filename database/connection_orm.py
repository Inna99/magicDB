from peewee import *
import os
#  from config import BASE_DIR

#  DB_PATH: str = os.path.abspath(os.path.join(BASE_DIR, 'db.db'))

db = SqliteDatabase('db.db')

class Movies(Model):
    title = CharField()
    production_year = DateField()
    viewed = BooleanField(default=False)

    class Meta:
        database = db


# db.connect()
# db.create_tables([Movies])
#
# TheLordOfTheRing = Movies(title='Властелин колец', production_year=date(2001, 1, 1), viewed=True)
# Matrix = Movies(title='Матрица', production_year=date(1999, 1, 1))
# TheLordOfTheRing.save()
# Matrix.save()



#print([movie for movie in Movies.select()])
# print(type(Movies.select()))
# query_set = Movies.select().where((Movies.title == 'Властелин колец') | (Movies.viewed == False))
# for movie in query_set:
#     print(movie.title, end=' ')
#     movie.delete_instance()
# print(f"{type(query_set)=}")
# TheLordOfTheRing.delete_instance()
# print(list(Movies.select().dicts()))
# print(Movies.select().count())
