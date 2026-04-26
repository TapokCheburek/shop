import enum
import uuid
from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Numeric(8, 2), nullable=False)
    socket = Column(String, nullable=False)
    power = Column(Integer, nullable=False)
    color_temperature = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
    quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

class OrderStateEnum(str, enum.Enum):
    CREATED = "created"
    PAID = "paid"
    FAILED = "failed"

class StateEnum(str, enum.Enum):
    NEW = "Новый"
    IN_PROGRESS = "в работе"
    COMPLETED = "отработан"
    REJECTED = "отклонен"

class DeliveryTypeEnum(str, enum.Enum):
    PICKUP = "самовывоз"
    DELIVERY = "доставка"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    order_number = Column(String, nullable=False, unique=True)
    order_state = Column(SQLEnum(OrderStateEnum), nullable=False, default=OrderStateEnum.CREATED)
    phone_number = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    delivery_type = Column(SQLEnum(DeliveryTypeEnum), nullable=False)
    address = Column(String, nullable=False)
    state = Column(SQLEnum(StateEnum), nullable=False, default=StateEnum.NEW)
    total_amount = Column(Numeric(10, 2), nullable=False)
    comment = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_item"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), primary_key=True, nullable=False)
    product_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    order = relationship("Order", back_populates="items")
