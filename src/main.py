from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends

import crud
import models
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


@app.post("/add_product", response_model=schemas.Product)
def add_product(product: schemas.Product, db=Depends(get_db)):
    return crud.add_product(db, product)


@app.get("/products/", response_model=List[schemas.Product])
def get_products(name: str = None, price: float = None, sort_by_name: bool = False, sort_by_price: bool = False,
                 db=Depends(get_db)):
    return crud.get_products(db, name, price, sort_by_name, sort_by_price)


@app.get("/product_names/", response_model=List[str])
def get_product_names(name: str = None, price: float = None, sort_by_name: bool = False, sort_by_price: bool = False,
                      db=Depends(get_db)):
    return crud.get_product_names(db, name, price, sort_by_name, sort_by_price)


@app.post("/add_product_to_cart", response_model=schemas.Cart_item)
def add_product_to_cart(product_id: int, db=Depends(get_db)):
    return crud.add_product_to_cart(db, product_id)


@app.post("/change_cart_product_amount", response_model=Optional[schemas.Cart_item])
def change_product_amount_in_cart(product_id: int, new_amount: int, db=Depends(get_db)):
    if new_amount < 0:
        raise HTTPException(status_code=404, detail=f"Product amount must be a positive number")
    if new_amount == 0:
        crud.remove_product_from_cart(db, product_id)
        return None
    return crud.set_cart_product_amount(db, product_id, new_amount)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
