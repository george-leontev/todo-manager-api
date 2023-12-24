from typing import List

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.data_repositories.todos_repository import TodosRepository

from src.models.todo_model import TodoModel

app = FastAPI()

origins = ["http://localhost:3000", "https://todo-manager-ui.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get():
    return RedirectResponse('/docs')


@app.get("/todos")
async def get_user_list() -> List[TodoModel]:
    todo_repository = TodosRepository()
    todos = todo_repository.get_list()

    return todos


@app.post("/todos")
async def post(todo: TodoModel) -> TodoModel:
    todo_repository = TodosRepository()
    todo = todo_repository.post(todo)

    return todo
