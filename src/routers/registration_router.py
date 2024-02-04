from base64 import b64decode
from http import HTTPStatus
import os
from passlib.context import CryptContext
from re import fullmatch
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import Response

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.data_repositories.users_repository import UsersRepository
from src.models.user_model import UserModel
from src.data_repositories.app_settings_repository import AppSettingsRepository
from src.models.registration_model import RegistrationModel
from src.utils.encoding import decrypt, encrypt

registration_cache: dict[str, str] = {}
router = APIRouter(prefix="/registration", tags=["registration"])


@router.post("/")
async def post_registration(
    registration: RegistrationModel,
    app_settings_repository: Annotated[
        AppSettingsRepository, Depends(AppSettingsRepository)
    ],
):
    app_settings = app_settings_repository.get_settings()

    if registration.password != registration.confirmed_password:
        raise Exception("The password and confirmed password do not match.")
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    if not fullmatch(email_pattern, registration.email):
        raise Exception("Email is wrong.")

    smtp_server = app_settings.email_config.smtp_server
    port = app_settings.email_config.port
    sender_email = app_settings.email_config.sender_email
    password = app_settings.email_config.password
    login = app_settings.email_config.login
    receiver_email = registration.email
    MASTER_KEY = app_settings.master_key

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Registration account in Todo Manager"
    secret = encrypt(
        f"{receiver_email}->{registration.password}", b64decode(MASTER_KEY)
    )
    registration_cache[receiver_email] = registration.password
    web_ui_root = (
        "http://localhost:3000"
        if os.environ.get("WEB_UI_ROOT") is None
        else os.environ.get("WEB_UI_ROOT")
    )

    message.attach(
        MIMEText(f"{web_ui_root}/registration/confirm?ticket={secret}", "plain")
    )

    with smtplib.SMTP(smtp_server, port, timeout=180) as server:

        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return registration


@router.post("/confirm")
def confirm_registration(
    ticket: str,
    app_settings_repository: Annotated[
        AppSettingsRepository, Depends(AppSettingsRepository)
    ],
):
    app_settings = app_settings_repository.get_settings()
    MASTER_KEY = app_settings.master_key
    secret = decrypt(ticket, b64decode(MASTER_KEY))
    secret_parts = secret.split("->")
    receiver_email = secret_parts[0]
    password = secret_parts[1]

    cached_password = registration_cache.get(receiver_email)
    if cached_password is not None and password == cached_password:
        user_repository = UsersRepository()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)

        existed_user = user_repository.get_by_email(receiver_email)
        if existed_user is not None:
            return Response(status_code=HTTPStatus.FORBIDDEN)

        user_repository.post(
            UserModel(id=0, email=receiver_email, hashed_password=hashed_password)
        )

        return Response(status_code=HTTPStatus.OK)

    return Response(status_code=HTTPStatus.BAD_REQUEST)
