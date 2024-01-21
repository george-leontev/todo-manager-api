from src.models.app_base_model import AppBaseModel


class RegistrationModel(AppBaseModel):
    email: str
    password: str
    confirmed_password: str
