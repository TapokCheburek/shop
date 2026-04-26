import sys

import uvicorn
from fastapi import FastAPI
from src.database import engine, Base

from src.api import orders

# Create tables and Seed
print("Initializing Database...")
try:
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")
except Exception as e:
    print(f"CRITICAL ERROR during DB init: {e}")
    sys.exit(1)

app = FastAPI(
    title="Orders Service",
    docs_url="/api/docs",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "orders"}

app.include_router(orders.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)