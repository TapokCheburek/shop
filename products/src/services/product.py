from sqlalchemy.orm import Session
from src import models
from src.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional
from uuid import UUID
from src.repositories.product import product_repo

def get_product(db: Session, product_id: UUID) -> Optional[models.Product]:
    return product_repo.get_by_id(db, product_id)

def get_product_by_name(db: Session, name: str) -> Optional[models.Product]:
    return product_repo.get_by_name(db, name)

def get_products(
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
    return product_repo.get_all(
        db,
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_power=min_power,
        max_power=max_power,
        socket=socket,
        type=type,
        in_stock=in_stock
    )

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
