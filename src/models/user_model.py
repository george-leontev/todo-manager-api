from src.models.app_base_model import AppBaseModel


class UserModel(AppBaseModel):
    id: int
    email: str
    hashed_password: str
