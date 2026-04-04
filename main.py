from fastapi import FastAPI
from database import engine
from models import book_model
from api import books

app = FastAPI()

book_model.Base.metadata.create_all(bind=engine)

app.include_router(books.router)