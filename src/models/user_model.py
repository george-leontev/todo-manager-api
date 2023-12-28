from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    email: str
    hashed_password: str
