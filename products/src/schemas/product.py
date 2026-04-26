from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., description="Название товара")
    price: Decimal = Field(..., description="Цена")
    socket: str = Field(..., description="Цоколь (например, E27, E14, GU10)")
    power: int = Field(..., description="Мощность")
    color_temperature: int = Field(..., description="Температура цвета")
    type: str = Field(..., description="Тип лампочки")
    description: Optional[str] = Field(None, description="Описание товара")
    quantity: int = Field(0, description="Остаток на складе")
    category_id: UUID = Field(..., description="ID категории")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    socket: Optional[str] = None
    power: Optional[int] = None
    color_temperature: Optional[int] = None
    type: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    category_id: Optional[UUID] = None
    is_deleted: Optional[bool] = None

class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
