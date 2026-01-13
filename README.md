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
For basic endpoints:
```bash
fastapi dev main.py
```

For managing movies.db:
```bash
fastapi dev moviesManager.py
```

For managing movies-extended.db:
```bash
fastapi dev moviesManagerExt.py
```

For managing movies-extended-orm.db:
```bash
fastapi dev moviesManagerORM.py
```

Server available at http://127.0.0.1:8000

## API Documentation
Server available at http://127.0.0.1:8000
Once the server is running, the interactive documentation is available at:
**Swagger UI**: http://127.0.0.1:8000/docs

## Author
Aleksandra Wilczyńska
Created as part of the postgraduate studies ISSI (Inżynieria Systemów Sztucznej Inteligencji) program at AGH University of Science and Technology.

## License
This project is part of an academic assignment for AGH University of Science and Technology, course " Wprowadzenie do technologii aplikacji internetowych". This project is released under the MIT License.
