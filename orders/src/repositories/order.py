from fastapi import HTTPException
import uuid
import string
import random
from sqlalchemy.orm import Session
from src import models
from src.schemas.order import OrderCreate
from typing import Optional

def generate_order_number() -> str:
    """Генерация уникального 8-значного номера заказа"""
    return "ORD-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

class OrderRepository:
    def get_by_order_number(self, db: Session, order_number: str) -> Optional[models.Order]:
        return db.query(models.Order).filter(models.Order.order_number == order_number, models.Order.is_deleted == False).first()

    def create(self, db: Session, order: OrderCreate) -> models.Order:
        order_number = generate_order_number()

        total_amount = 0
        # Проверяем наличие товаров и вычитаем их со склада
        for item in order.items:
            product = db.query(models.Product).filter(
                models.Product.id == item.product_id,
                models.Product.is_deleted == False
            ).with_for_update().first() # Блокируем строку для обновления

            if not product:
                raise HTTPException(status_code=404, detail=f"Товар с id {item.product_id} не найден")

            if product.quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Недостаточно товара '{product.name}' на складе. В наличии: {product.quantity}, Запрошено: {item.quantity}"
                )

            # Считаем сумму по реальной цене из БД
            total_amount += product.price * item.quantity

            # Вычитаем из БД
            product.quantity -= item.quantity

        db_order = models.Order(
            order_number=order_number,
            order_state=order.order_state,
            phone_number=order.phone_number,
            user_name=order.user_name,
            delivery_type=order.delivery_type,
            address=order.address,
            state=order.state,
            total_amount=total_amount,
            comment=order.comment
        )
        db.add(db_order)
        db.flush() # Чтобы получить db_order.id

        for item in order.items:
            # Снова ищем цену, так как мы уже проверили существование
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

            db_order_item = models.OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            )
            db.add(db_order_item)

        db.commit()
        db.refresh(db_order)
        return db_order

order_repo = OrderRepository()
