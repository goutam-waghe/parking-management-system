from typing import Union
from fastapi import FastAPI
from user import userRouter
from database import Base , engine
from middleware.auth import isAuthenticated
app = FastAPI()
Base.metadata.create_all(bind=engine)


app.middleware("http")(isAuthenticated)
app.include_router(userRouter.router)