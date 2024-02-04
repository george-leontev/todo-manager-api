from typing import Annotated, List
from fastapi import APIRouter, Depends

from src.models.user_model import UserModel
from src.models.todo_model import TodoModel
from src.data_repositories.todos_repository import TodosRepository
from src.utils.auth_utils import verify_access_token

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
async def get_user_list(
    auth_user: Annotated[UserModel, Depends(verify_access_token)]
) -> List[TodoModel]:
    todo_repository = TodosRepository()
    todos = todo_repository.get_list(auth_user)
    todos.sort(key=lambda todo: todo.date)
    
    return todos


@router.post("/")
async def post(
    todo: TodoModel, auth_user: Annotated[UserModel, Depends(verify_access_token)]
    ) -> TodoModel:
    todo_repository = TodosRepository()
    added_todo = todo_repository.post(todo, auth_user)

    return added_todo


@router.delete("/{todo_id}")
async def delete(
    todo_id: str, auth_user: Annotated[UserModel, Depends(verify_access_token)]
):
    todo_repository = TodosRepository()
    deleted_todo = todo_repository.delete(todo_id, auth_user)

    return deleted_todo


@router.put("/")
async def put(
    todo: TodoModel, auth_user: Annotated[UserModel, Depends(verify_access_token)]
) -> TodoModel:
    todo_repository = TodosRepository()
    edited_todo = todo_repository.put(todo, auth_user)

    return edited_todo
