
from fastapi import APIRouter, HTTPException
from typing import Any, List, Dict
from helperFnc import *

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

### The provided endpoints interact with an SQLite database movies.db to manage movie records ###

# Fetches all movies from the database
@router.get('')
async def get_movies():
    try:
        return fetch_all_movies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movies: {str(e)}")

# Fetches a specific movie by its ID
@router.get('/{movie_id}')
async def get_movie(movie_id: int):
    try:
        movie = fetch_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movie: {str(e)}")

# Adds a new movie to the database
@router.post('')
def add_movie(params: Dict[str, Any]):
    try:
        movie_id = insert_movie(params)
        return {"message": "Movie added successfully", "movie_id": movie_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding movie: {str(e)}")

# Updates an existing movie by its ID
@router.put('/{movie_id}')
def update_movie(movie_id: int, params: Dict[str, Any]):
    try:
        updated_count = update_movie_by_id(movie_id, params)
        if updated_count == 0:
            raise HTTPException(status_code=404, detail="Movie not found")
        return {"message": f"Movie {movie_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating movie: {str(e)}")

# Deletes a specific movie by its ID
@router.delete('/{movie_id}')
def delete_movie(movie_id: int):
    try:
        deleted_count = delete_movie_by_id(movie_id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Movie not found")
        return {"message": f"Movie {movie_id} deleted successfully", "deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting movie: {str(e)}")

# Deletes multiple movies by their IDs
@router.delete('')
def delete_movies(movie_ids: List[int]):
    try:
        deleted_count = delete_movies_by_ids(movie_ids)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="No movies found to delete")
        return {"message": f"Movie deleted successfully", "deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting movies: {str(e)}")

# Fetches all actors associated with a specific movie
@router.get('/{movie_id}/actors')
async def get_movie_actors_endpoint(movie_id: int):
    try:
        actors = fetch_movie_actors(movie_id)
        if not actors:
            raise HTTPException(status_code=404, detail="Movie not found or no actors listed")
        return {"movie_id": movie_id, "actors": actors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movie actors: {str(e)}")
