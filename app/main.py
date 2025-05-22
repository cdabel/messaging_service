from fastapi import FastAPI
from app.routes.messaging import router as messaging_router
from app.models.message import create_tables

app = FastAPI()

app.include_router(messaging_router)


@app.get("/health")
def check_health():
    return {"status": "ok"}


create_tables()
