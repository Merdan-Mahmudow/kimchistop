from typing import Optional
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    name: Optional[str] = None
    tel: Optional[str] = None
    address: Optional[str] = None
    orders: Optional[str] = None
    nickname: Optional[str] = None
    chatID: Optional[str] = None
    favourites: Optional[list[int]] = []
    role: Optional[str]


class Order(BaseModel):
    number: Optional[int] = None
    items: Optional[list[dict]] = []
    total: Optional[int] = None
    date: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    isDelivery: Optional[bool] = False
    payment: Optional[str] = None
    comment: Optional[str] = None
    client: Optional[int] = None
    cutlery: Optional[int] = None


class Category(BaseModel):
    categoryName: Optional[str] = None
    food: Optional[list] = []

class Food(BaseModel):
    foodName: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    category: Optional[int] = None

class Promo(BaseModel):
    code: Optional[str] = None
    isPercent: Optional[bool] = None
    discount: Optional[int] = None
    maxUse: Optional[int] = None
    used: Optional[list[int]] = []
    desc: Optional[str] = None

    
