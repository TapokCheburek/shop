from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from src.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from src.services import product as product_service
from src.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if product_service.get_product_by_name(db, product.name):
        raise HTTPException(status_code=400, detail="Товар с таким названием уже существует")

    # Note: category checking is out of scope for this microservice as requested, but database will throw error if foreign key fails
    return product_service.create_product(db=db, product=product)

@router.get("/", response_model=List[ProductResponse])
def read_products(
    skip: int = 0,
    limit: int = 100,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_power: Optional[int] = None,
    max_power: Optional[int] = None,
    socket: Optional[str] = None,
    type: Optional[str] = None,
    in_stock: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    products = product_service.get_products(
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
    return products
@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: UUID, db: Session = Depends(get_db)):
    db_product = product_service.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_product
