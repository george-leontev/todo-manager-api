import pathlib
from typing import List

from pydantic import TypeAdapter
from src.models.user_model import UserModel

from src.models.todo_model import TodoModel


class TodosRepository:
    def _get_root(self) -> str:
        return pathlib.Path(__file__).parent.parent.parent

    def _write(self, todos: List[TodoModel]):
        root = self._get_root()
        with open(f"{root}/data/todos.json", "w", encoding="utf-8") as f:
            todos_json = (
                TypeAdapter(List[TodoModel])
                .dump_json(todos, by_alias=True)
                .decode("utf-8")
            )
            f.write(todos_json)

    def get_list(self, user: UserModel) -> List[TodoModel]:
        root = self._get_root()
        with open(f"{root}/data/todos.json", "r", encoding="utf-8") as f:
            todos_json = f.read()

        todos: List[TodoModel] = TypeAdapter(List[TodoModel]).validate_json(todos_json)

        todos = [todo for todo in todos if todo.user_id == user.id]

        return todos

    def post(self, todo: TodoModel, user: UserModel) -> TodoModel:
        todos = self.get_list(user)
        next_id = max([t.id for t in todos]) + 1
        todo.id = next_id
        todo.user_id = user.id
        todos.append(todo)

        self._write(todos)

        return todo

    def delete(self, todo_id: int, user: UserModel) -> TodoModel | None:
        todos = self.get_list(user)
        deleted_todo = next((todo for todo in todos if todo.id == todo_id), None)

        if deleted_todo is not None:
            todos.remove(deleted_todo)
            self._write(todos)

        return deleted_todo

    def put(self, todo: TodoModel, user: UserModel) -> TodoModel | None:
        todos = self.get_list(user)
        original_todo = next((t for t in todos if t.id == todo.id), None)

        if original_todo is not None:
            todo.user_id = user.id
            todos.remove(original_todo)
            todos.append(todo)
            todos.sort(key=lambda t: t.id)
            self._write(todos)

            return todo

        return None
