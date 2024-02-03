from src.models.app_base_model import AppBaseModel


class AuthUserModel(AppBaseModel):
    user_id: str
    email: str
    token: str
