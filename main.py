from fastapi import FastAPI
from routers import hello, calculator, geocode, movies_extendedDB, movies_extendedDB_orm, moviesDB

app = FastAPI()

app.include_router(hello.router)
app.include_router(calculator.router)
app.include_router(geocode.router)
app.include_router(moviesDB.router)
app.include_router(movies_extendedDB.router)
app.include_router(movies_extendedDB_orm.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}
