from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["calculator"]
)

### These endpoints perform basic arithmetic operations (sum, subtraction, multiplication, and division) with default values ###

# Endpoint to calculate the sum of two numbers with default values
@router.get("/sum")
async def sum(x: int = 0, y: int = 10):
    return x + y

# Endpoint to calculate the difference between two numbers with default values
@router.get("/subtract")
async def subtract(x: int = 0, y: int = 10):
    return x - y

# Endpoint to calculate the product of two numbers with default values
@router.get("/multiply")
async def multiply(x: int = 0, y: int = 10):
    return x * y

# Endpoint to calculate the division of two numbers with default values, handling division by zero
@router.get("/divide")
async def divide(x: float = 0, y: float = 10):
    if y == 0:
        return {"error": "Division by zero is not allowed"}
    return x / y
