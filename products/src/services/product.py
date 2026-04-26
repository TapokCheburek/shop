from sqlalchemy.orm import Session
from .. import models
from typing import List, Optional
from uuid import UUID
from ..repositories.product import product_repo
from ..schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: UUID) -> Optional[models.Product]:
    return product_repo.get_by_id(db, product_id)

def get_product_by_name(db: Session, name: str) -> Optional[models.Product]:
    return product_repo.get_by_name(db, name)

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return product_repo.get_all(db, skip=skip, limit=limit)

def create_product(db: Session, product: ProductCreate) -> models.Product:
    return product_repo.create(db, product)

def update_product(db: Session, product_id: UUID, product: ProductUpdate) -> Optional[models.Product]:
    db_product = product_repo.get_by_id(db, product_id)
    if not db_product:
        return None

    update_data = product.model_dump(exclude_unset=True)
    return product_repo.update(db, db_product, update_data)

def delete_product(db: Session, product_id: UUID) -> bool:
    db_product = product_repo.get_by_id(db, product_id)
    if not db_product:
        return False

    return product_repo.delete(db, db_product)
