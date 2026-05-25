from fastapi import FastAPI
from src.database import engine
from src import models
from src.api.auth import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Microservice")
app.include_router(router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Auth Microservice"}
