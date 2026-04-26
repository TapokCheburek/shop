from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from src.models import OrderStateEnum, StateEnum, DeliveryTypeEnum

class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0, description="Количество товара")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    order_id: UUID
    price: Decimal = Field(..., description="Цена товара (на момент заказа)")
    created_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    order_state: OrderStateEnum
    phone_number: str
    user_name: str
    delivery_type: DeliveryTypeEnum
    address: str
    state: StateEnum
    comment: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: UUID
    order_number: str
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
