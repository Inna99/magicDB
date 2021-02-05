from peewee import *


# Connect to a Postgres database.
# driver , объект базы данных
db = PostgresqlDatabase('postgres', user='postgres', password='mysecretpassword', host='localhost', port=5432)

#  id = AutoField()  # Auto-incrementing primary key
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
