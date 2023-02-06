from sqlalchemy import MetaData, Integer, String, Table, Column, Float, ForeignKey

from database import Base

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("price", Float, nullable=False)
)

cart = Table(
    "cart",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("product_id", Integer, ForeignKey("products.id"), unique=True),
    Column("amount", Integer, nullable=False),
    Column("total_price", Float, nullable=False)
)

class Product_DB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class Cart_DB(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    amount = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
