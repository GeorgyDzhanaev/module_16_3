from fastapi import FastAPI, Path
from typing import Annotated, Dict

app = FastAPI()


users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def add_user(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    new_user_id = str(max(map(int, users.keys()), default=0) + 1)
    users[new_user_id] = f'Имя: {username}, возраст: {age}'
    return f"User {new_user_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(gt=0, le=100, description="Enter User ID")],
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str] = f'Имя: {username}, возраст: {age}'
        return f"User {user_id_str} has been updated"
    else:
        return f"User {user_id_str} not found"

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(gt=0, le=100, description="Enter User ID")]):
    user_id_str = str(user_id)
    if user_id_str in users:
        del users[user_id_str]
        return f"User {user_id_str} has been deleted"
    else:
        return f"User {user_id_str} not found"