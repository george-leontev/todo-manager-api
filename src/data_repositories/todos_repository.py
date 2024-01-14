import pathlib
from typing import List

from pydantic import TypeAdapter

from src.models.todo_model import TodoModel


class TodosRepository:
    def _get_root(self) -> str:
        return pathlib.Path(__file__).parent.parent.parent

    def _write_todos(self, todos: List[TodoModel]):
        root = self._get_root()
        with open(f'{root}/data/todos.json', 'w', encoding='utf-8') as f:
            todos_json = TypeAdapter(List[TodoModel]).dump_json(todos).decode('utf-8')
            f.write(todos_json)

    def get_list(self) -> List[TodoModel]:
        root = self._get_root()
        with open(f'{root}/data/todos.json', 'r', encoding='utf-8') as f:
            todos_json = f.read()

        todos: List[TodoModel] = TypeAdapter(List[TodoModel]).validate_json(todos_json)

        return todos

    def post(self, todo: TodoModel) -> TodoModel:
        todos = self.get_list()
        next_id = max([t.id for t in todos]) + 1
        todo.id = next_id
        todos.append(todo)

        self._write_todos(todos)

        return todo

    def delete(self, todo_id: int) -> TodoModel | None:

        todos = self.get_list()
        deleted_todo = next((todo for todo in todos if todo.id == todo_id), None)

        if deleted_todo is not None:
            todos.remove(deleted_todo)
            self._write_todos(todos)

        return deleted_todo

    def put(self, todo: TodoModel) -> TodoModel | None:
        todos = self.get_list()
        original_todo = next((t for t in todos if t.id == todo.id), None)

        if original_todo is not None:
            todos.remove(original_todo)
            todos.append(todo)
            todos.sort(key=lambda t: t.id)
            self._write_todos(todos)

            return todo

        return None
