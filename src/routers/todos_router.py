from typing import List
from fastapi import APIRouter

from src.models.todo_model import TodoModel
from src.data_repositories.todos_repository import TodosRepository

router = APIRouter(prefix='/todos', tags=['todos'])


@router.get('/')
async def get_user_list() -> List[TodoModel]:
    todo_repository = TodosRepository()
    todos = todo_repository.get_list()

    return todos


@router.post('/')
async def post(todo: TodoModel) -> TodoModel:
    todo_repository = TodosRepository()
    added_todo = todo_repository.post(todo)

    return added_todo


@router.delete('/{todo_id}')
async def delete(todo_id: int):
    todo_repository = TodosRepository()
    deleted_todo = todo_repository.delete(todo_id)

    return deleted_todo

@router.put('/')
async def put(todo: TodoModel) -> TodoModel:
    todo_repository = TodosRepository()
    edited_todo = todo_repository.put(todo)

    return edited_todo