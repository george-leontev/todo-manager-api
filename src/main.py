from typing import List
from fastapi import FastAPI
import pathlib
from src.models.user_model import UserModel
from pydantic import TypeAdapter

app = FastAPI()

@app.get('/')
async def get():
    return {'message': 'Hello world'}

@app.get('/users')
async def get_user_list():
    root = pathlib.Path(__file__).parent.parent

    with open(f'{root}/data/data.json', 'r', encoding='utf-8') as f:
        json_data = f.read()

    users: List[UserModel] = TypeAdapter(List[UserModel]).validate_json(json_data)

    return users

@app.post('/users')
async def post(user: UserModel):
    root = pathlib.Path(__file__).parent.parent

    with open(f'{root}/data/data.json', 'r', encoding='utf-8') as f:
        json_data = f.read()

    users: List[UserModel] = TypeAdapter(List[UserModel]).validate_json(json_data)

    users.append(user)

    with open(f'{root}/data/data.json', 'w', encoding='utf-8') as f:
        json_data = TypeAdapter(List[UserModel]).dump_json(users).decode("utf-8") 
        f.write(json_data)

    return users
