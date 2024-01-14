from src.models.app_base_model import AppBaseModel


class LoginModel(AppBaseModel):
    email: str
    password: str
