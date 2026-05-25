from fastapi import FastAPI
from src.database import engine
from src import models
from src.api import orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders Service")

app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в Orders Microservice. Документация доступна по адресу /docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
