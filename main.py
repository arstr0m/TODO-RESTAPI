from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

import Users.users
import Icons.icons
import Tasks.tasks
from Data import database
from Models import models

app = FastAPI()
app.include_router(Users.users.router)
app.include_router(Icons.icons.router)
app.include_router(Tasks.tasks.router)
models.Base.metadata.create_all(bind=database.engine)

# TODO create test

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/health", tags=["Health Check"])
async def get_status():
    return {"message": "API is working"}
