from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel

class TodoStatus(IntEnum):
    PENDING = 1,
    DONE = 2


class TodoModel(BaseModel):
    id: int
    description: str
    date: datetime
    status: TodoStatus
