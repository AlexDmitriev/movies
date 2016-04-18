from flask import Flask
from flask_restful import Resource, Api
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.fields import ManyToManyField
import collections
import json

app = Flask(__name__)
api = Api(app)
db = SqliteDatabase('movies.db')

class Actor(Model):
    name = CharField()
    class Meta:
        database = db

class Genre(Model):
    name = CharField()
    class Meta:
        database = db

class Movie(Model):
    imdbID   = CharField()
    title    = CharField()
    year     = CharField()
    plot     = CharField()
    director = CharField()
    actors   = ManyToManyField(Actor, related_name='movies')
    genres    = ManyToManyField(Genre, related_name='movies')
    class Meta:
        database = db

MovieActor = Movie.actors.get_through_model()
MovieGenre = Movie.genres.get_through_model()

db.connect()

class Index(Resource):
    def get(self):
        return {
            'usage': {
                'actors list': 'GET /actors',
                'single actor': 'GET /actors/<actor_id>',
                'genres list': 'GET /genres',
                'single genre': 'GET /genres/<genre_id>',
                'movies list': 'GET /movies',
                'single movie': 'GET /movies/<movie_id>',
                }
            }

class ActorsList(Resource):
    def get(self):
        actors = []
        for actor in Actor.select():
            actors.append(model_to_dict(actor))
        return actors

class ActorsItem(Resource):
    def get(self, actor_id):
        try:
            actor = Actor.get(Actor.id == actor_id)
            return model_to_dict(actor)
        except Actor.DoesNotExist:
            return {'error': 'User not found'}

class GenresList(Resource):
    def get(self):
        genres = []
        for genre in Genre.select():
            genres.append(model_to_dict(genre))
        return genres

class GenresItem(Resource):
    def get(self, genre_id):
        try:
            genre = Genre.get(Genre.id == genre_id)
            return model_to_dict(genre)
        except Genre.DoesNotExist:
            return {'error': 'Genre not found'}

class MoviesList(Resource):
    def get(self):
        movies = []
        for movie in Movie.select():
            model = {
                "id": movie.id,
                "title": movie.title,
                "year": movie.year,
                "imdbID": movie.imdbID,
                "plot": movie.plot,
                "actors": [],
                "genres": [],
            }
            for actor in movie.actors:
                model['actors'].append(model_to_dict(actor))
            for genre in movie.genres:
                model['genres'].append(model_to_dict(genre))
            movies.append(model)
        return movies

class MoviesItem(Resource):
    def get(self, movie_id):
        try:
            movie = Movie.get((Movie.id == int(float(movie_id))))
            model = {
                "id": movie.id,
                "title": movie.title,
                "year": movie.year,
                "imdbID": movie.imdbID,
                "plot": movie.plot,
                "actors": [],
                "genres": [],
            }
            for actor in movie.actors:
                model['actors'].append(model_to_dict(actor))
            for genre in movie.genres:
                model['genres'].append(model_to_dict(genre))
            return model
        except Movie.DoesNotExist:
            return {'error': 'Movie not found'}


api.add_resource(Index, '/')
api.add_resource(ActorsList, '/actors')
api.add_resource(ActorsItem, '/actors/<actor_id>')
api.add_resource(GenresList, '/genres')
api.add_resource(GenresItem, '/genres/<genre_id>')
api.add_resource(MoviesList, '/movies')
api.add_resource(MoviesItem, '/movies/<movie_id>')

if __name__ == '__main__':
    app.run(debug=True)
