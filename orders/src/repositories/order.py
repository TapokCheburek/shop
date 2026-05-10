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

        from decimal import Decimal
        total_amount = Decimal('0')
        product_prices = {}

        import urllib.request
        import urllib.error
        import json
        import os

        product_service_url = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")

        # Проверяем наличие товаров и вычитаем их со склада через HTTP-вызов
        for item in order.items:
            try:
                # В PostgreSQL нет распределенных транзакций по умолчанию, поэтому просто делаем патч
                url = f"{product_service_url}/products/{item.product_id}/deduct?quantity={item.quantity}"
                req = urllib.request.Request(url, method="PATCH")
                with urllib.request.urlopen(req) as response:
                    product_data = json.loads(response.read().decode())
                    # Считаем сумму по реальной цене
                    price = Decimal(str(product_data.get("price")))
                    total_amount += price * Decimal(item.quantity)
                    product_prices[str(item.product_id)] = price
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    raise HTTPException(status_code=400, detail=f"Товар с id {item.product_id} не найден или недостаточно на складе")
                raise HTTPException(status_code=400, detail=f"Ошибка сервиса товаров: {e}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Ошибка связи с сервисом товаров: {e}")

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
            db_order_item = models.OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product_prices[str(item.product_id)]
            )
            db.add(db_order_item)

        db.commit()
        db.refresh(db_order)
        return db_order

order_repo = OrderRepository()
