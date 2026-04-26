from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.order import OrderCreate, OrderResponse
from src.services import order as order_service
from src.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db=db, order=order)

@router.get("/track/{order_number}", response_model=OrderResponse)
def track_order(order_number: str, db: Session = Depends(get_db)):
    db_order = order_service.get_order_by_number(db, order_number=order_number)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
