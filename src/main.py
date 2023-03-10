from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends

import crud
import schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Electronic Store"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


@app.post("/api/product", response_model=schemas.Product)
def add_product(product: schemas.Product, db=Depends(get_db)):
    return crud.add_product(db, product)


@app.get("/api/products/", response_model=List[schemas.Product])
def get_products(name: str = None, price: float = None, sort_by_name: bool = False, sort_by_price: bool = False,
                 ascending_name: bool = True, ascending_price: bool = True, db=Depends(get_db)):
    return crud.get_products(db, name, price, sort_by_name, sort_by_price, ascending_name, ascending_price)


@app.get("/api/products/names/", response_model=List[str])
def get_product_names(name: str = None, price: float = None, sort_by_name: bool = False, sort_by_price: bool = False,
                      ascending_name: bool = True, ascending_price: bool = True, db=Depends(get_db)):
    return crud.get_product_names(db, name, price, sort_by_name, sort_by_price, ascending_name, ascending_price)


@app.post("/api/cart/{product_name}", response_model=schemas.Cart_item)
def add_product_to_cart(product_name: str, db=Depends(get_db)):
    return crud.add_product_to_cart(db, product_name)


@app.put("/api/cart/{product_name}", response_model=Optional[schemas.Cart_item])
def change_product_amount_in_cart(product_name: str, new_amount: int, db=Depends(get_db)):
    if new_amount < 0:
        raise HTTPException(status_code=404, detail=f"Product amount must be a positive number")
    if new_amount > 100_000_000:
        raise HTTPException(status_code=404, detail=f"Too big amount")
    if new_amount == 0:
        crud.remove_product_from_cart(db, product_name)
        return None
    return crud.set_cart_product_amount(db, product_name, new_amount)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
