import os
from dotenv import load_dotenv, find_dotenv

import sqlmodel
from sqlmodel import Session, SQLModel

load_dotenv(find_dotenv(), override=True)

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL == "":
    raise NotImplementedError("`DATABASE_URL` is not set.")

engine = sqlmodel.create_engine(DATABASE_URL)

# database models
def init_db():
    print("creating database tables...")
    SQLModel.metadata.create_all(engine)

# api routes 
def get_session():
    with Session(engine) as session:
        yield session

