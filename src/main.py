from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.routers.registration_router import router as registration_router
from src.routers.todos_router import router as todos_router
from src.routers.default_router import router as default_router
from src.routers.sign_in_router import router as sign_in_router


app = FastAPI()

origins = ["http://localhost:3000", "https://todo-manager-ui.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=default_router)
app.include_router(router=sign_in_router)
app.include_router(router=todos_router)
app.include_router(router=registration_router)
