from fastapi import FastAPI
from .routers import users
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!"}


app.include_router(users.router)
