from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from src.schemas.order import OrderCreate, OrderResponse
from src.services import order as order_service
from src.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.get("/my", response_model=List[OrderResponse])
def get_my_orders(request: Request, db: Session = Depends(get_db)):
    user_id = request.headers.get("x-user-id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    orders = db.query(order_service.models.Order).filter(order_service.models.Order.user_id == user_id, order_service.models.Order.is_deleted == False).all()
    return orders

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(request: Request, order: OrderCreate, db: Session = Depends(get_db)):
    user_id = request.headers.get("x-user-id")
    if user_id:
        order.user_id = user_id
    return order_service.create_order(db=db, order=order)

@router.get("/track/{order_number}", response_model=OrderResponse)
def track_order(order_number: str, db: Session = Depends(get_db)):
    db_order = order_service.get_order_by_number(db, order_number=order_number)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
