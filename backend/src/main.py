from fastapi import FastAPI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

app = FastAPI()

MY_PROJECT = os.environ.get("MY_PROJECT") or "This is my project"
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise NotImplementedError("'API_KEY' was not set")


@app.get("/")
async def greet():
    return {"say": "hello world!", "MY_PROJECT":MY_PROJECT, "API_KEY":API_KEY}