from fastapi import FastAPI
from db.models import create_db_and_tables
from src.apis.api import router as ApiRouter


app = FastAPI(title = "IPL Analytics Agent")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(ApiRouter)


