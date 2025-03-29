from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users 
from app.routers import users, auth

app = FastAPI(title="Audio Service")

@app.on_event("startup")
async def startup():
    # создаём таблицы, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Hello, мир!"}


app.include_router(users.router) 
app.include_router(users.router)
app.include_router(auth.router)