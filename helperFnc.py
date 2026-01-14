import sqlite3
from typing import Any, List, Dict, Callable
from fastapi import HTTPException

def connect_to_db():
    return sqlite3.connect('movies.db')

def fetch_all_movies() -> List[Dict[str, Any]]:
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = [{'id': movie[0], 'title': movie[1], 'year': movie[2], 'actors': movie[3]} for movie in cursor]
    db.close()
    return movies

def fetch_movie_by_id(movie_id: int) -> Dict[str, Any]:
    db = connect_to_db()
    cursor = db.cursor()
    movie = cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchone()
    db.close()
    if movie:
        return {'id': movie[0], 'title': movie[1], 'year': movie[2], 'actors': movie[3]}
    return {}

def insert_movie(params: Dict[str, Any]) -> int:
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
                   (params['title'], params['year'], params['actors']))
    db.commit()
    movie_id = cursor.lastrowid
    db.close()
    return movie_id

def delete_movie_by_id(movie_id: int) -> int:
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    db.commit()
    rowcount = cursor.rowcount
    db.close()
    return rowcount

def delete_movies_by_ids(movie_ids: List[int]) -> int:
    db = connect_to_db()
    cursor = db.cursor()
    placeholders = ','.join('?' for _ in movie_ids)
    cursor.execute(f"DELETE FROM movies WHERE id IN ({placeholders})", movie_ids)
    db.commit()
    rowcount = cursor.rowcount
    db.close()
    return rowcount

def update_movie_by_id(movie_id: int, params: Dict[str, Any]) -> int:
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("UPDATE movies SET title=?, year=?, actors=? WHERE id=?",
                   (params['title'], params['year'], params['actors'], movie_id))
    db.commit()
    rowcount = cursor.rowcount
    db.close()
    return rowcount

def fetch_movie_actors(movie_id: int) -> List[str]:
    db = connect_to_db()
    cursor = db.cursor()
    movie = cursor.execute("SELECT actors FROM movies WHERE id=?", (movie_id,)).fetchone()
    db.close()
    if movie and movie[0]:
        return movie[0].split(', ')
    return []

def with_db_connection(func: Callable[[sqlite3.Connection], Any]) -> Any:
    try:
        db = sqlite3.connect('movies-extended.db')
        return func(db)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

def fetch_one(cursor: sqlite3.Cursor, query: str, params: tuple) -> Any:
    result = cursor.execute(query, params).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return result

def execute_and_commit(db: sqlite3.Connection, query: str, params: tuple) -> int:
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    return cursor.rowcount
