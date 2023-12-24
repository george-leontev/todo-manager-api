from datetime import datetime

from pydantic import BaseModel

class TodoModel(BaseModel):
    id: int
    description: str
    date: datetime
    status: str
