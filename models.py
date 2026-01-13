from peewee import *

db = SqliteDatabase('movies-extended-orm.db')

class BaseModel(Model):
    class Meta:
        database = db

class Actor(BaseModel):
    name = CharField()
    surname = CharField()

class Movie(BaseModel):
    title = CharField()
    year = IntegerField()
    director = CharField()
    description = TextField()
    actors = ManyToManyField(Actor, backref='movies')

ActorMovie = Movie.actors.get_through_model()

db.connect()
db.create_tables([Actor, Movie, ActorMovie])
db.close()
