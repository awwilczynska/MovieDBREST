from fastapi import APIRouter, HTTPException
import sqlite3
from typing import Any
from helperFnc import with_db_connection, fetch_one, execute_and_commit

router = APIRouter(
    prefix="/movies-extended",
    tags=["movies-extended"]
)

### The provided endpoints interact with an SQLite database movies-extended.db to manage movie records ###

# Fetches all movies from the database
@router.get('')
async def get_movies_extended():
    def fetch_movies(db: sqlite3.Connection):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movie")
        return [{'id': movie[0], 'title': movie[1], 'year': movie[2], 'director': movie[3], 'description': movie[4]} for movie in cursor]
    return with_db_connection(fetch_movies)

# Fetches a specific movie by its ID
@router.get('/{movie_id}')
async def get_movie_extended(movie_id: int):
    def fetch_movie(db: sqlite3.Connection):
        cursor = db.cursor()
        movie = fetch_one(cursor, "SELECT * FROM movie WHERE id=?", (movie_id,))
        return {'id': movie[0], 'title': movie[1], 'year': movie[2], 'director': movie[3], 'description': movie[4]}
    return with_db_connection(fetch_movie)

# Adds a new movie to the database
@router.post('')
def add_movie_extended(params: dict[str, Any]):
    def add_movie(db: sqlite3.Connection):
        cursor = db.cursor()
        cursor.execute("INSERT INTO movie (title, year, director, description) VALUES (?, ?, ?, ?)",
                       (params['title'], params['year'], params['director'], params['description']))
        db.commit()
        return {"message": "Movie added successfully", "Movie id": cursor.lastrowid}
    return with_db_connection(add_movie)

# Updates an existing movie by its ID
@router.put('/{movie_id}')
def update_movie_extended(movie_id: int, params: dict[str, Any]):
    def update_movie(db: sqlite3.Connection):
        rowcount = execute_and_commit(db, "UPDATE movie SET title=?, year=?, director=?, description=? WHERE id=?",
                                      (params['title'], params['year'], params['director'], params['description'], movie_id))
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Movie not found - cannot update")
        return {"message": f"Movie {movie_id} updated successfully"}
    return with_db_connection(update_movie)

# Deletes a specific movie by its ID
@router.delete('/{movie_id}')
def delete_movie_extended(movie_id: int):
    def delete_movie(db: sqlite3.Connection):
        rowcount = execute_and_commit(db, "DELETE FROM movie WHERE id=?", (movie_id,))
        if rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found. Nothing deleted.")
        return {"message": f"Movie {movie_id} deleted successfully", "deleted_count": rowcount}
    return with_db_connection(delete_movie)

# Deletes multiple movies by their IDs
@router.delete('')
def delete_movies_extended(movie_ids: list[int]):
    def delete_movies(db: sqlite3.Connection):
        placeholders = ','.join('?' for _ in movie_ids)
        rowcount = execute_and_commit(db, f"DELETE FROM movie WHERE id IN ({placeholders})", tuple(movie_ids))
        if rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No movies from {movie_ids} were found. Nothing deleted.")
        return {"message": f"Movie deleted successfully", "deleted_count": rowcount}
    return with_db_connection(delete_movies)

# Fetches a specific actor by their ID
@router.get('/actors/{actor_id}')
async def get_actor_extended(actor_id: int):
    def fetch_actor(db: sqlite3.Connection):
        cursor = db.cursor()
        actor = fetch_one(cursor, "SELECT * FROM actor WHERE id=?", (actor_id,))
        return {'id': actor[0], 'name': actor[1], 'surname': actor[2]}
    return with_db_connection(fetch_actor)

# Adds a new actor to the database
@router.post('/actors')
def add_actor_extended(params: dict[str, Any]):
    def add_actor(db: sqlite3.Connection):
        cursor = db.cursor()
        cursor.execute("INSERT INTO actor (name, surname) VALUES (?, ?)", (params['name'], params['surname']))
        db.commit()
        return {"message": "Actor added successfully", "Actor id": cursor.lastrowid}
    return with_db_connection(add_actor)

# Updates an existing actor by their ID
@router.put('/actors/{actor_id}')
def update_actor_extended(actor_id: int, params: dict[str, Any]):
    def update_actor(db: sqlite3.Connection):
        rowcount = execute_and_commit(db, "UPDATE actor SET name=?, surname=? WHERE id=?",
                                      (params['name'], params['surname'], actor_id))
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Actor not found - cannot update")
        return {"message": f"Actor {actor_id} updated successfully"}
    return with_db_connection(update_actor)

# Deletes a specific actor by their ID
@router.delete('/actors/{actor_id}')
def delete_actor_extended(actor_id: int):
    def delete_actor(db: sqlite3.Connection):
        rowcount = execute_and_commit(db, "DELETE FROM actor WHERE id=?", (actor_id,))
        if rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Actor {actor_id} not found. Nothing deleted.")
        return {"message": f"Actor {actor_id} deleted successfully", "deleted_count": rowcount}
    return with_db_connection(delete_actor)
