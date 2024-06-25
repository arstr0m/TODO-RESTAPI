from fastapi import FastAPI

import Users.users
from Data import database
from Models import models

app = FastAPI()
app.include_router(Users.users.router)
models.Base.metadata.create_all(bind=database.engine)

@app.get("/health")
async def get_status():
    return {"message": "API is working"}
