from fastapi import APIRouter

router = APIRouter(
    prefix="/hello",
    tags=["hello"]
)

# Endpoint to greet the user by their name
@router.get("/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}!"}
