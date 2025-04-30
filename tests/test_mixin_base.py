from src.base_task import BaseEntity
from src.category import Category, Order
from src.product import Product


def test_correct_parameters(capsys) -> None:
    Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    massage = capsys.readouterr()
    assert (
        massage.out.strip()
        == "Создан объект Product с параметрами: ('Samsung Galaxy S23 Ultra', '256GB, Серый цвет, 200MP камера', 180000.0, 5)"
    )


def test_order_creation():
    product = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    order = Order(product, 2)

    assert order.product == product
    assert order.quantity == 2
    assert order.calculate_total() == 62000


def test_order_str():
    product = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    order = Order(product, 2)
    assert str(order) == "Заказ: Xiaomi Redmi Note 11, 2 шт., Итого: 62000.0 руб."


def test_base_entity_implementation():
    product = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product],
    )
    order = Order(product, 2)

    assert isinstance(category, BaseEntity)
    assert isinstance(order, BaseEntity)
    assert category.calculate_total() == 434000.0
    assert order.calculate_total() == 62000
