from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from sqlalchemy import String, DateTime, Integer, Float, Column, ForeignKey
from sqlalchemy.orm import relationship,mapped_column,relationships, Mapped

from src.database.base import db
from src.database.associative_tables import user_product_assoc


@dataclass
class Review(db.Model):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    text: Mapped[str] = mapped_column(String())
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))



@dataclass
class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column()
    img_url: Mapped[str] = mapped_column(String())
    reviews: Mapped[List[Review]] = relationship()



@dataclass
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    products: Mapped[List[Product]] = relationship(secondary=user_product_assoc)

