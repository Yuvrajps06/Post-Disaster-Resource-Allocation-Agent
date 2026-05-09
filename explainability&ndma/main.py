# main.py

from fastapi import FastAPI
from routes.recommendation import router

app = FastAPI()

app.include_router(router)