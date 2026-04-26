from sqlalchemy.orm import Session
from .. import models
from ..schemas.product import ProductCreate
from typing import List, Optional
from uuid import UUID

class ProductRepository:
    def get_by_id(self, db: Session, product_id: UUID) -> Optional[models.Product]:
        return db.query(models.Product).filter(models.Product.id == product_id, models.Product.is_deleted == False).first()

    def get_by_name(self, db: Session, name: str) -> Optional[models.Product]:
        return db.query(models.Product).filter(models.Product.name == name, models.Product.is_deleted == False).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
        return db.query(models.Product).filter(models.Product.is_deleted == False).offset(skip).limit(limit).all()

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
