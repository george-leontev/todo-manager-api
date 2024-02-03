import pathlib
from typing import List
from uuid import uuid4

from pydantic import TypeAdapter
from src.models.user_model import UserModel


class UsersRepository:
    def _get_root(self) -> str:
        return pathlib.Path(__file__).parent.parent.parent

    def _write(self, users: List[UserModel]):
        root = self._get_root()
        with open(f"{root}/data/users.json", "w", encoding="utf-8") as f:
            users_json = (
                TypeAdapter(List[UserModel])
                .dump_json(users, by_alias=True)
                .decode("utf-8")
            )
            f.write(users_json)

    def get_list(self) -> List[UserModel]:
        root = self._get_root()
        with open(f"{root}/data/users.json", "r", encoding="utf-8") as f:
            users_json = f.read()

        users: List[UserModel] = TypeAdapter(List[UserModel]).validate_json(users_json)

        return users

    def get_by_id(self, user_id) -> UserModel | None:
        users = self.get_list()
        user = next((u for u in users if u.id == user_id), None)

        return user

    def get_by_email(self, email: str) -> UserModel | None:
        users = self.get_list()
        user = next((u for u in users if u.email == email), None)

        return user

    def post(self, user: UserModel) -> UserModel:
        users = self.get_list()
        next_id = uuid4().__str__()
        user.id = next_id
        users.append(user)

        self._write(users)

        return user
