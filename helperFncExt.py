from fastapi import HTTPException
import sqlite3
from typing import Any, Callable

# Helper function to handle database connections
def with_db_connection(func: Callable[[sqlite3.Connection], Any]) -> Any:
    try:
        db = sqlite3.connect('movies-extended.db')
        return func(db)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

# Helper function to fetch a single record
def fetch_one(cursor: sqlite3.Cursor, query: str, params: tuple) -> Any:
    result = cursor.execute(query, params).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return result

# Helper function to execute a query and commit changes
def execute_and_commit(db: sqlite3.Connection, query: str, params: tuple) -> int:
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    return cursor.rowcount
