from src.models.app_base_model import AppBaseModel


class EmailConfig(AppBaseModel):
    smtp_server: str
    port: int
    sender_email: str
    password: str
    login: str

class AppSettingsModel(AppBaseModel):
    master_key: str
    email_config: EmailConfig
