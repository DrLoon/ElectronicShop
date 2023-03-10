from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

import models
import schemas


def get_products_raw(db: Session, name: str = None, price: float = None, sort_by_name: bool = False,
                     sort_by_price: bool = False, ascending_name: bool = True, ascending_price: bool = True):
    res = db.query(models.Product_DB)
    if name:
        res = res.filter(models.Product_DB.name == name)
    if price:
        res = res.filter(models.Product_DB.price == price)
    if sort_by_name:
        if ascending_name:
            res = res.order_by(models.Product_DB.name.asc())
        else:
            res = res.order_by(models.Product_DB.name.desc())
    if sort_by_price:
        if ascending_price:
            res = res.order_by(models.Product_DB.price.asc())
        else:
            res = res.order_by(models.Product_DB.price.desc())
    return res


def get_products(db: Session, name: str = None, price: float = None, sort_by_name: bool = False,
                 sort_by_price: bool = False, ascending_name: bool = True, ascending_price: bool = True):
    return get_products_raw(db, name, price, sort_by_name, sort_by_price, ascending_name, ascending_price).all()


def get_product_names(db: Session, name: str = None, price: float = None, sort_by_name: bool = False,
                      sort_by_price: bool = False, ascending_name: bool = True, ascending_price: bool = True):
    res = get_products_raw(db, name, price, sort_by_name, sort_by_price, ascending_name, ascending_price).with_entities(
        models.Product_DB.name)
    return [i[0] for i in res]


def add_product(db: Session, product: schemas.Product):
    try:
        pr_db = models.Product_DB(**product.dict())
        db.add(pr_db)
        db.commit()
        db.refresh(pr_db)
    except exc.IntegrityError:  # if UniqueViolation exception
        raise HTTPException(status_code=404, detail=f"Probably, such a product has already been added")

    return pr_db


def add_product_to_cart(db: Session, product_name: str):
    res = db.query(models.Product_DB).filter(models.Product_DB.name == product_name).first()
    if not res:
        raise HTTPException(status_code=404, detail=f"There is no such product")

    try:
        cart_db = models.Cart_DB(product_id=res.id, amount=1, total_price=res.price)
        db.add(cart_db)
        db.commit()
        db.refresh(cart_db)
    except exc.IntegrityError:  # if UniqueViolation exception
        raise HTTPException(status_code=404, detail=f"Probably, such a product has already been added to the cart")

    return cart_db


def remove_product_from_cart(db: Session, product_name: str):
    pr = db.query(models.Product_DB).filter(models.Product_DB.name == product_name).first()
    if not pr:
        raise HTTPException(status_code=404, detail=f"No such product in the cart")
    db.query(models.Cart_DB).filter(models.Cart_DB.product_id == pr.id).delete()
    db.commit()
    return None


def set_cart_product_amount(db: Session, product_name: str, new_amount: int):
    pr = db.query(models.Product_DB).filter(models.Product_DB.name == product_name).first()
    if not pr:
        raise HTTPException(status_code=404, detail=f"There is no such product")
    cart_item = db.query(models.Cart_DB).filter(models.Cart_DB.product_id == pr.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail=f"There is no such product in the cart")

    cart_item.amount = new_amount
    cart_item.total_price = new_amount * pr.price
    db.commit()
    db.refresh(cart_item)
    return cart_item
