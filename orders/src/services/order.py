from sqlalchemy.orm import Session
from src import models
from src.schemas.order import OrderCreate
from typing import Optional
from src.repositories.order import order_repo

def get_order_by_number(db: Session, order_number: str) -> Optional[models.Order]:
    return order_repo.get_by_order_number(db, order_number)

def create_order(db: Session, order: OrderCreate) -> models.Order:
    return order_repo.create(db, order)

