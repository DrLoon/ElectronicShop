from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    price: float = Field(ge=0)

    class Config:
        orm_mode = True


class Cart_item(BaseModel):
    product: Product
    amount: int = Field(gt=0)
    total_price: float = Field(ge=0)
