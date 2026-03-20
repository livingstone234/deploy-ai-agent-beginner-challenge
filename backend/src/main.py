import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from fastapi import FastAPI

from api.db import init_db
from api.chat.routing import router as chat_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    init_db()
    yield
    # after app startup 

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router)

MY_PROJECT = os.environ.get("MY_PROJECT") or "This is my project"

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise NotImplementedError("'API_KEY' was not set")


@app.get("/")
async def greet():
    return {"say": "hello world!", "MY_PROJECT":MY_PROJECT, "API_KEY":API_KEY}