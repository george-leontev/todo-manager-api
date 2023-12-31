from datetime import timedelta

from fastapi import APIRouter, Response

from src.models.access_token_model import AccessTokenModel
from src.data_repositories.users_repository import UsersRepository
from src.models.login_model import LoginModel
from src.utils.auth_utils import verify_password, create_access_token


router = APIRouter(prefix='/sign-in', tags=['sign-in'])

@router.post("/sign-in")
async def sign_in(login: LoginModel):
    user_repository = UsersRepository()
    user = user_repository.get_by_email(login.email)

    if user is not None:
        if verify_password(login.password, user.hashed_password):
            access_token = create_access_token(
                data={"sub": user.email}, expires_delta=timedelta(minutes=60)
            )

            return AccessTokenModel(
                id=1,
                email=login.email,
                token=access_token,
            )

    return Response(status_code=401)
