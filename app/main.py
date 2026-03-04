from fastapi import FastAPI
from .routers import users, expenses, login
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!"}


app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(login.router)
