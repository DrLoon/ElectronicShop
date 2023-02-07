from sqlalchemy import Integer, String, Column, Float, ForeignKey

from database import Base


class Product_DB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)

class Cart_DB(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    amount = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
