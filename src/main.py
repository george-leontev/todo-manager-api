from typing import List
from datetime import datetime, timedelta


from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from passlib.context import CryptContext

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.data_repositories.users_repository import UsersRepository
from src.models.access_token_model import AccessTokenModel
from src.models.login_model import LoginModel
from src.models.todo_model import TodoModel
from src.data_repositories.todos_repository import TodosRepository

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

origins = ["http://localhost:3000", "https://todo-manager-ui.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_password(plain_password, hashed_password):
    # s = pwd_context.hash(plain_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@app.get("/")
async def get():
    return RedirectResponse("/docs")


@app.get("/todos")
async def get_user_list() -> List[TodoModel]:
    todo_repository = TodosRepository()
    todos = todo_repository.get_list()

    return todos


@app.post("/todos")
async def post(todo: TodoModel) -> TodoModel:
    todo_repository = TodosRepository()
    todo = todo_repository.post(todo)

    return todo


@app.delete("/todos/{todo_id}")
async def delete(todo_id: int):
    todo_repository = TodosRepository()
    deleted_todo = todo_repository.delete(todo_id)

    return deleted_todo


@app.post("/sign-in")
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
