from fastapi import FastAPI
from app.database import engine, Base
from app.api import evaluate
from app.api import campaigns
from app.api import schedule
from app.api import history
import app.models


# Создаём таблицы в базе (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campaign Rule Engine")

app.include_router(evaluate.router)
app.include_router(campaigns.router)
app.include_router(schedule.router)
app.include_router(history.router)

@app.get("/")
def root():
    return {"message": "Campaign Rule Engine is running"}
