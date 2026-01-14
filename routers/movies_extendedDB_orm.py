from fastapi import APIRouter
from typing import Any
from models import Movie, Actor
from playhouse.shortcuts import model_to_dict

router = APIRouter(
    prefix="/orm",
    tags=["orm"]
)

### The provided endpoints interact with an SQLite database movies-extended-orm.db to manage movie records ###

# Fetches a list of all movies from the database
@router.get('/movies')
async def get_orm_movies(): 
    try:
        return list(Movie.select().dicts())
    except Exception as e:
        return {"error": f"Failed to fetch movies: {str(e)}"}
    
# Fetches details of a specific movie by its ID     
@router.get('/movies/{movie_id}')
async def get_orm_movie(movie_id: int):
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie is None:
        return {"error": "Movie not found"}
    return model_to_dict(movie)

# Adds a new movie to the database
@router.post('/movies')
def add_orm_movie(params: dict[str, Any]):
    movie = Movie.create(
        title=params['title'],
        year=params['year'],
        director=params['director'],
        description=params['description']
    )
    return {"message": "Movie added successfully", "id": movie.id}

# Updates an existing movie's details by its ID
@router.put('/movies/{movie_id}')
def update_orm_movie(movie_id: int, params: dict[str, Any]):    
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie is None:
        return {"error": "Movie not found - cannot update"}
    movie.title = params['title']
    movie.year = params['year']
    movie.director = params['director']
    movie.description = params['description']
    movie.save()
    return {"message": f"Movie with id {movie_id} updated successfully"}

# Deletes a specific movie by its ID
@router.delete('/movies/{movie_id}')
def delete_orm_movie(movie_id: int):
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie is None:
        return {"error": "Movie not found - cannot delete"}
    movie.delete_instance()
    return {"message": f"Movie {movie_id} deleted successfully"}

# Deletes multiple movies by their IDs
@router.delete('/movies')
def delete_orm_movies(movie_ids: list[int]):
    query = Movie.delete().where(Movie.id.in_(movie_ids))
    deleted_count = query.execute()
    if deleted_count == 0:
        return {"error": "Movie not found - cannot delete"}
    return {"message": f"Movie deleted successfully", "deleted_count": deleted_count}

# Fetches a list of all actors from the database
@router.get('/actors')
async def get_orm_actors(): 
    return list(Actor.select().dicts())

# Fetches details of a specific actor by their ID
@router.get('/actors/{actor_id}')
async def get_orm_actor(actor_id: int):
    actor = Actor.get_or_none(Actor.id == actor_id)
    if actor is None:
        return {"error": "Actor not found"}
    return model_to_dict(actor)

# Adds a new actor to the database
@router.post('/actors')
def add_orm_actor(params: dict[str, Any]):
    actor = Actor.create(
        name=params['name'],
        surname=params['surname']
    )
    return {"message": "Actor added successfully", "id": actor.id}

# Updates an existing actor's details by their ID
@router.put('/actors/{actor_id}')
def update_orm_actor(actor_id: int, params: dict[str, Any]):    
    actor = Actor.get_or_none(Actor.id == actor_id)
    if actor is None:
        return {"error": "Actor not found - cannot update"}
    actor.name = params['name']
    actor.surname = params['surname']
    actor.save()
    return {"message": f"Actor {actor_id} updated successfully"}

# Deletes a specific actor by their ID
@router.delete('/actors/{actor_id}')
def delete_orm_actor(actor_id: int):
    actor = Actor.get_or_none(Actor.id == actor_id)
    if actor is None:
        return {"error": "Actor not found - cannot delete"}
    actor.delete_instance()
    return {"message": f"Actor {actor_id} deleted successfully"}

# Deletes multiple actors by their IDs
@router.delete('/actors')
def delete_orm_actors(actor_ids: list[int]):
    query = Actor.delete().where(Actor.id.in_(actor_ids))
    deleted_count = query.execute()
    if deleted_count == 0:
        return {"error": "Actor not found - cannot delete"}
    return {"message": f"Actor deleted successfully", "deleted_count": deleted_count}

# Fetches all actors associated with a specific movie by its ID
@router.get('/movies/{movie_id}/actors')
async def get_movie_actors_orm(movie_id: int):
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie is None:
        return {"error": "Movie not found"}
    actors = [model_to_dict(actor) for actor in movie.actors]
    return {"movie_id": movie_id, "actors": actors}
