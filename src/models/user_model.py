from src.models.app_base_model import AppBaseModel


class UserModel(AppBaseModel):
    id: str
    email: str
    hashed_password: str
