from uuid import uuid4 

from src.database.base import db
from src.database.models import Product, Review, User


def get_products():
    products = Product.query.all()
    

def get_product(product_id: str):
    return Product.query.filter_by(id=product_id).one_or_404()

def add_product(name: str, description: str, price: float, img_url: str):
    product = Product(
        id=uuid4().hex,
        name=name,
        description=description,
        price=price,
        img_url=img_url,
    )
    db.session.add(product)
    db.session.commit()
    return f"товар '{name} успешно додано"



def delete_product(product_id: str) -> str:
    product = Product.query.filter_by(id=product_id).one_or_404()
    db.session.delete(product)
    db.session.commit()
    return f"товар '{product.name}' успішно видалено"


def update_product(product_id: str, name: str, description: str, price: float, img_url: str) -> str:
    product = Product.query.filter_by(id=product_id).one_or_404()
    product.name = name
    product.description = description
    product.price = price
    product.img_url = img_url
    db.session.commit()
    return f"товар '{product_id}' успішно оновлено"


def add_review_product(product_id: str, text: str, name: str) -> str:
    user = User.query.filter_by(name=name).first()
    if not user:
        user = User(id=uuid4().hex, name=name)

    review = Review(id=uuid4().hex, text=text, user=user)
    product = Product.query.filter_by(id=product_id).one_or_404()
    product.reviews.append(review)
    db.session.commit()
    return f"відгук  успішно додано до товару'"


def buy_product(product_id: str, name: str) -> str:
    product = Product.query.filter_by(id=product_id).one_or_404()

    user = User.query.filter_by(name=name).first()
    if not user:
        user = User(id=uuid4().hex, name=name)

    user.products.append(product)
    db.session.add(user)
    db.session.commit()
    return f"товар '{product.name}' успішно куплено"