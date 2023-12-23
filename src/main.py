from typing import List
from fastapi import FastAPI
import pathlib
from src.models.user_model import UserModel
from pydantic import TypeAdapter

app = FastAPI()

@app.get('/')
async def get():
    return {'message': 'Hello world'}

@app.get('/data')
def get_data():
    root = pathlib.Path(__file__).parent.parent

    with open(f'{root}/data/data.json', 'r', encoding='utf-8') as f:
        json_data = f.read()

    items: List[UserModel] = TypeAdapter(List[UserModel]).validate_json(json_data)

    return items
# Response(content=json_data, media_type="application/json")

@app.post('/data')
def post():
    root = pathlib.Path(__file__).parent.parent

    with open(f'{root}/data/data.json', 'w', encoding='utf-8') as f:
        pass
