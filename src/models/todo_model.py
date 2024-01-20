from datetime import datetime
from enum import IntEnum

from src.models.app_base_model import AppBaseModel

class TodoStatus(IntEnum):
    PENDING = 1,
    DONE = 2


class TodoModel(AppBaseModel):
    id: int
    title: str
    description: str | None
    date: datetime
    status: TodoStatus
    user_id: int
