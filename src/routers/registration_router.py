from re import fullmatch
from fastapi import APIRouter
import yagmail

from src.models.registration_model import RegistrationModel


router = APIRouter(prefix="/registration", tags=["registration"])


@router.post("/")
async def post_registration(registration: RegistrationModel):
    if registration.password != registration.confirmed_password:
        raise Exception("The password and confirmed password do not match.")
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    if not fullmatch(email_pattern, registration.email):
        raise Exception("Email is wrong.")



    receiver = registration.email
    body = "Hello there from Yagmail"

    yag = yagmail.SMTP("egorleontev54@gmail.com", password='nc3pe41980')
    a = yag.send(
        to=receiver,
        subject="Yagmail test",
        contents=body,
    )

    return registration
