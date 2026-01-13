from fastapi import FastAPI
import requests

app = FastAPI()

### Basic endpoints ###

# Endpoint to return a simple "Hello World!" message
@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

# Endpoint to greet the user by their name
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

# Endpoint to calculate the sum of two numbers with default values
@app.get("/sum")
async def sum(x: int = 0, y: int = 10):
    return x+y

# Endpoint to calculate the difference between two numbers with default values
@app.get("/subtract")
async def subtract(x: int = 0, y: int = 10):
    return x - y

# Endpoint to calculate the product of two numbers with default values
@app.get("/multiply")
async def multiply(x: int = 0, y: int = 10):
    return x * y

# Endpoint to calculate the division of two numbers with default values, handling division by zero
@app.get("/divide")
async def divide(x: float = 0, y: float = 10):
    if y == 0:
        return {"error": "Division by zero is not allowed"}
    return x / y

# Endpoint to fetch geocode data (address details) for given latitude and longitude
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

# Endpoint to fetch the display name (address) for given latitude and longitude
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
