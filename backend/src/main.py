from fastapi import FastAPI
import os

MY_PROJECT = os.environ.get("MY_PROJECT")

app = FastAPI()

@app.get("/")
async def greet():
    return {"say": "hello world!", "MY_PROJECT":MY_PROJECT}