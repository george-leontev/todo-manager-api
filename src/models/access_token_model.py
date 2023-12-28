from pydantic import BaseModel


class AccessTokenModel(BaseModel):
    id: int
    email: str
    token: str
