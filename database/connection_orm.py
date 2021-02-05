from peewee import *
from datetime import date
import os
#  from config import BASE_DIR

#  DB_PATH: str = os.path.abspath(os.path.join(BASE_DIR, 'db.db'))

# db = SqliteDatabase('db.db')
# Connect to a Postgres database.
# driver , объект базы данных

db = PostgresqlDatabase('postgres', user='postgres', password='mysecretpassword', host='localhost', port=5432)

#     id = AutoField()  # Auto-incrementing primary key. по умолчанию(peewee)
class BaseModel(Model):
    class Meta:
        database = db


class Producer(BaseModel):
    prodid = AutoField()
    fullname = CharField()

    class Meta:
        table_name = 'producer'


class Movies(BaseModel):
    title = CharField()
    production_year = DateField()
    viewed = BooleanField(default=False)
    #producer = ForeignKeyField(Producer, column_name='prodid')

    class Meta:
        table_name = 'movies'


class Connect(object):
    def __new__(cls):
        print(type(cls))
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connect, cls).__new__(cls)
            cls.db = db
            cls.db.connect()
            cls.db.create_tables([Producer, Movies])
        return cls.db





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
