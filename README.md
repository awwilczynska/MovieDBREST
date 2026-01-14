# Movies API

## Project Description
A REST API built with **FastAPI**. This project manages a movie database.

## Tech Stack
- **Framework:** [FastAPI](fastapi.tiangolo.com)
- **Database:** SQLite
- **Server:** [Uvicorn](www.uvicorn.org)
- **Environment:** Virtualenv
- **Language:** Python 3.11

## Installation & Setup
1. Clone or download this repository and navigate to the project directory
2. Create and activate a virtual environment
3. Install dependencies

### 1. Clone the repository
```bash
git clone git@github.com:awwilczynska/MovieDBREST.git
cd MovieDBREST
```
### 2. Create and activate virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate   # Windows
```

### 3. Install dependencies
Before installing dependencies, make sure your virtual environment is activated:
```bash
pip install -r requirements.txt
```
To uninstall all dependencies listed in `requirements.txt` run:
```bash
pip uninstall -r requirements.txt -y
```
To list all installed packages, use:
```bash
pip freeze
```
You can also update your `requirements.txt` file with the current environment’s packages running:
```bash
pip freeze > requirements.txt
```

## Running the Application
You can start the development server using the FastAPI CLI:
```bash
fastapi dev main.py
```
Server available at http://127.0.0.1:8000

## API Documentation
Server available at http://127.0.0.1:8000
Once the server is running, the interactive documentation is available at:
**Swagger UI**: http://127.0.0.1:8000/docs

## Available endpoints
### Greeting endpoints
    GET / # Endpoint to return a simple "Hello World!" message
    GET /hello/{name} - # Endpoint to greet the user by their name

### Endpoints to perform basic arithmetic operations ###
    GET /sum # Endpoint to calculate the sum of two numbers with default values
    GET /subtract # Endpoint to calculate the difference between two numbers with default values
    GET /multiply # Endpoint to calculate the product of two numbers with default values
    GET /divide # Endpoint to calculate the division of two numbers with default values, handling division by zero

### Endpoint to fetch geocode data (address details) for given latitude and longitude ###
    GET /geocode # Endpoint to fetch geocode data (address details) for given latitude and longitude

### Endpoints to interact with an SQLite database movies.db to manage movie records ###
    GET /movies # Fetches all movies from the database
    GET /movies/{movie_id} # Fetches a specific movie by its ID
    POST /movies # Adds a new movie to the database
    PUT /movies/{movie_id} # Updates an existing movie by its ID
    DELETE /movies/{movie_id} # Deletes a specific movie by its ID
    DELETE /movies # Deletes multiple movies by their IDs
    GET /movies/{movie_id}/actors # Fetches all actors associated with a specific movie

### Endpoints to interact with an SQLite database movies-extended.db to manage movie records ###
    GET /movies-extended # Fetches all movies from the database
    GET /movies-extended/{movie_id} # Fetches a specific movie by its ID
    POST /movies-extended # Adds a new movie to the database
    PUT /movies-extended/{movie_id} # Updates an existing movie by its ID
    DELETE /movies-extended/{movie_id} # Deletes a specific movie by its ID
    DELETE /movies-extended # Deletes multiple movies by their IDs
    GET /movies-extended/actors/{actor_id} # Fetches a specific actor by their ID
    POST /movies-extended/actors # Adds a new actor to the database
    PUT /movies-extended/actors/{actor_id} # Updates an existing actor by their ID
    DELETE /movies-extended/actors/{actor_id} # Deletes a specific actor by their ID

### Endpoints to interact with an SQLite database movies-extended-orm.db to manage movie records ###
    GET /orm/movies # Fetches a list of all movies from the database
    GET /orm/movies/{movie_id} # Fetches details of a specific movie by its ID   
    POST /orm/movies # Adds a new movie to the database
    PUT /orm/movies/{movie_id} # Updates an existing movie's details by its ID
    DELETE /orm/movies/{movie_id} # Deletes a specific movie by its ID
    DELETE /orm/movies # Deletes multiple movies by their IDs
    GET /orm/actors # Fetches a list of all actors from the database
    GET /orm/actors/{actor_id} # Fetches details of a specific actor by their ID
    POST /orm/actors # Adds a new actor to the database
    PUT /orm/actors/{actor_id} # Updates an existing actor's details by their ID
    DELETE /orm/actors/{actor_id} # Deletes a specific actor by their ID
    DELETE /orm/actors # Deletes multiple actors by their IDs
    GET /orm/movies/{movie_id}/actors # Fetches all actors associated with a specific movie by its ID

## Author
Aleksandra Wilczyńska
Created as part of the postgraduate studies ISSI (Inżynieria Systemów Sztucznej Inteligencji) program at AGH University of Science and Technology.

## License
This project is part of an academic assignment for AGH University of Science and Technology, course " Wprowadzenie do technologii aplikacji internetowych". This project is released under the MIT License.
