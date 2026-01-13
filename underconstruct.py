from fastapi import FastAPI, HTTPException
import requests
import sqlite3
from typing import Any

app = FastAPI()

### Basic endpoints below ###

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/sum")
async def sum(x: int = 0, y: int = 10):
    return x+y

@app.get("/subtract")
async def subtract(x: int = 0, y: int = 10):
    return x - y

@app.get("/multiply")
async def multiply(x: int = 0, y: int = 10):
    return x * y

@app.get("/divide")
async def divide(x: float = 0, y: float = 10):
    if y == 0:
        return {"error": "Division by zero is not allowed"}
    return x / y

@app.get("/geocode")
async def geocode(lat: float = 50.0680275, lon: float = 19.9098668):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch geocode data: {str(e)}"}

@app.get("/geocodename")
async def geocodename(lat: float = 50.0680275, lon: float = 19.9098668):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("display_name")
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch geocode data: {str(e)}"}

### Endpoints for managing movies.db below ###

@app.get('/movies')
async def get_movies(): 
    try:
        output = []
        db = sqlite3.connect('movies.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movies")
        for movie in cursor:
            movie = {'id': movie[0], 'title': movie[1], 'year': movie[2], 'actors': movie[3]}
            output.append(movie)
        return output
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

@app.get('/movies/{movie_id}')
async def get_movie(movie_id: int): 
    try:
        db = sqlite3.connect('movies.db')
        cursor = db.cursor()
        movie = cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchone()
        if movie is None:
            return {"error": "Movie not found"}
        return {'id': movie[0], 'title': movie[1], 'year': movie[2], 'actors': movie[3]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

@app.post('/movies')
def add_movie(params: dict[str, Any]):
    db=sqlite3.connect('movies.db')
    cursor=db.cursor()
    cursor.execute("INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)", 
                   (params['title'], params['year'], params['actors']))
    db.commit()
    return {"message": "Movie added successfully", "Movie id": cursor.lastrowid}
    
@app.delete('/movies/{movie_id}')
def delete_movie(movie_id: int): 
    db=sqlite3.connect('movies.db')
    cursor=db.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    db.commit()
    if cursor.rowcount == 0:
        return {"error": f"Movie {movie_id} not found. Nothing deleted."}
    return {"message": f"Movie {movie_id} deleted successfully", "deleted_count": cursor.rowcount}

@app.delete('/movies')
def delete_movies(movie_ids: list[int]):
    db=sqlite3.connect('movies.db')
    cursor=db.cursor()
    lista=','.join('?' for _ in movie_ids)
    cursor.execute(f"DELETE FROM movies WHERE id IN ({lista})", movie_ids)
    db.commit()
    if cursor.rowcount == 0:
        return {"error": f"No movies from {movie_ids} were found. Nothing deleted."}
    return {"message": f"Movies {movie_ids} deleted successfully", "deleted_count": cursor.rowcount}
    
@app.put('/movies/{movie_id}')
def update_movie(movie_id: int, params: dict[str, Any]):
    db=sqlite3.connect('movies.db')
    cursor=db.cursor()
    cursor.execute("UPDATE movies SET title=?, year=?, actors=? WHERE id=?", 
                   (params['title'], params['year'], params['actors'], movie_id))
    db.commit()
    if cursor.rowcount == 0:
        return {"error": "Movie {movie_id} not found"}
    return {"message": f"Movie {movie_id} updated successfully"}

@app.get('/movies/{movie_id}/actors')
async def get_movie_actors(movie_id: int):
    db=sqlite3.connect('movies.db')
    cursor=db.cursor()
    movie=cursor.execute("SELECT actors FROM movies WHERE id=?", (movie_id,)).fetchone()
    if movie is None:
        return {"error": "Movie not found"}
    actors = movie[0].split(', ') if movie[0] else []
    return {"movie_id": movie_id, "actors": actors}


### Endpoints for managing movies-extended.db below ###

@app.get('/movies-extended')
async def get_movies_extended(): 
    try:
        output = []
        db = sqlite3.connect('movies-extended.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movie")
        for movie in cursor:
            movie = {'id': movie[0], 'title': movie[1], 'year': movie[2], 'director': movie[3], 'description': movie[4]}
            output.append(movie)
        return output
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

@app.get('/movies-extended/{movie_id}')
async def get_movie_extended(movie_id: int): 
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    movie=cursor.execute("SELECT * FROM movie WHERE id=?", (movie_id,)).fetchone()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {'id':movie[0], 'title':movie[1], 'year':movie[2], 'director':movie[3], 'description':movie[4]}

@app.post('/movies-extended')
def add_movie_extended(params: dict[str, Any]):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    cursor.execute("INSERT INTO movie (title, year, director, description) VALUES (?, ?, ?, ?)",
                   (params['title'], params['year'], params['director'], params['description']))
    db.commit()
    return {"message": "Movie added successfully", "Movie id": cursor.lastrowid}

@app.put('/movies-extended/{movie_id}')
def update_movie_extended(movie_id: int, params: dict[str, Any]):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    cursor.execute("UPDATE movie SET title=?, year=?, director=?, description=? WHERE id=?", 
                   (params['title'], params['year'], params['director'], params['description'], movie_id))
    db.commit()
    if cursor.rowcount == 0:
        return {"error": "Movie not found - cannot update"}
    return {"message": f"Movie {movie_id} updated successfully"}
    
@app.delete('/movies-extended/{movie_id}')
def delete_movie_extended(movie_id: int): 
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    cursor.execute("DELETE FROM movie WHERE id=?", (movie_id,))
    db.commit()
    if cursor.rowcount == 0:
        return {"error": f"Movie {movie_id} not found. Nothing deleted."}
    return {"message": f"Movie {movie_id} deleted successfully", "deleted_count": cursor.rowcount}

@app.delete('/movies-extended')
def delete_movies_extended(movie_ids: list[int]):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    lista=','.join('?' for _ in movie_ids)
    cursor.execute(f"DELETE FROM movie WHERE id IN ({lista})", movie_ids)
    db.commit()
    if cursor.rowcount == 0:
        return {"error": f"No movies from {movie_ids} were found. Nothing deleted."}
    return {"message": f"Movies {movie_ids} deleted successfully", "deleted_count": cursor.rowcount}

@app.get('/movies-extended/actors/{actor_id}')
async def get_actor_extended(actor_id: int):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    actor=cursor.execute("SELECT * FROM actor WHERE id=?", (actor_id,)).fetchone()
    if actor is None:
        return {"error": "Actor not found"}
    return {'id':actor[0], 'name':actor[1], 'surname':actor[2]}

@app.post('/movies-extended/actors')
def add_actor_extended(params: dict[str, Any]):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    cursor.execute("INSERT INTO actor (name, surname) VALUES (?, ?)",
                   (params['name'], params['surname']))
    db.commit()
    return {"message": "Actor added successfully", "Actor id": cursor.lastrowid}

@app.put('/movies-extended/actors/{actor_id}')
def update_actor_extended(actor_id: int, params: dict[str, Any]):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    cursor.execute("UPDATE actor SET name=?, surname=? WHERE id=?", 
                   (params['name'], params['surname'], actor_id))
    db.commit()
    if cursor.rowcount == 0:
        return {"error": "Actor not found - cannot update"}
    return {"message": f"Actor {actor_id} updated successfully"}

@app.delete('/movies-extended/actors/{actor_id}')
def delete_actor_extended(actor_id: int):
    db=sqlite3.connect('movies-extended.db')
    cursor=db.cursor()
    cursor.execute("DELETE FROM actor WHERE id=?", (actor_id,))
    db.commit()
    if cursor.rowcount == 0:
        return {"error": f"Actor {actor_id} not found. Nothing deleted."}
    return {"message": f"Actor {actor_id} deleted successfully", "deleted_count": cursor.rowcount}
