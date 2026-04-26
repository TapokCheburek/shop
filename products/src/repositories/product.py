from sqlalchemy.orm import Session
from src import models
from src.schemas.product import ProductCreate
from typing import List, Optional
from uuid import UUID

class ProductRepository:
    def get_by_id(self, db: Session, product_id: UUID) -> Optional[models.Product]:
        return db.query(models.Product).filter(models.Product.id == product_id, models.Product.is_deleted == False).first()

    def get_by_name(self, db: Session, name: str) -> Optional[models.Product]:
        return db.query(models.Product).filter(models.Product.name == name, models.Product.is_deleted == False).first()

    def get_all(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            min_power: Optional[int] = None,
            max_power: Optional[int] = None,
            socket: Optional[str] = None,
            type: Optional[str] = None,
            in_stock: Optional[bool] = None
    ) -> List[models.Product]:
        query = db.query(models.Product).filter(models.Product.is_deleted == False)

        if min_price is not None:
            query = query.filter(models.Product.price >= min_price)
        if max_price is not None:
            query = query.filter(models.Product.price <= max_price)
        if min_power is not None:
            query = query.filter(models.Product.power >= min_power)
        if max_power is not None:
            query = query.filter(models.Product.power <= max_power)
        if socket is not None:
            query = query.filter(models.Product.socket == socket)
        if type is not None:
            query = query.filter(models.Product.type == type)
        if in_stock is not None:
            if in_stock:
                query = query.filter(models.Product.quantity > 0)
            else:
                query = query.filter(models.Product.quantity == 0)

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, product: ProductCreate) -> models.Product:
        db_product = models.Product(**product.model_dump())
        db.add(db_product)
        try:
            db.commit()
            db.refresh(db_product)
        except Exception as e:
            db.rollback()
            raise e
        return db_product

    def update(self, db: Session, db_product: models.Product, update_data: dict) -> models.Product:
        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    def delete(self, db: Session, db_product: models.Product) -> bool:
        db_product.is_deleted = True
        db.commit()
        return True

product_repo = ProductRepository()
