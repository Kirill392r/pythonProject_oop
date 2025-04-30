from typing import List

from src.base_task import BaseEntity
from src.product import Product


class Category(BaseEntity):
    """Класс для представления категории товаров в магазине"""

    name: str
    description: str
    products: List[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        """Инициализирует экземпляр класса Category"""
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count = len(products)
        self.total_quantity = sum(product.quantity for product in products)
        super().__init__()

    def __str__(self) -> str:
        """Строковое отображение"""
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."

    def add_product(self, product_obj: Product) -> None:
        """Добавление товаров в категорию"""
        if not (isinstance(product_obj, Product) and issubclass(product_obj.__class__, Product)):
            raise TypeError
        self.__products.append(product_obj)
        Category.category_count += 1

    @property
    def products(self) -> list:
        """Формируем вывод списка товаров"""
        return [f"{p.name}, {p.price}. Остаток: {p.quantity} шт." for p in self.__products]

    def calculate_total(self) -> float:
        """Реализация абстрактного метода - общая стоимость всех товаров категории"""
        return sum(p.price * p.quantity for p in self.__products)


class Order(BaseEntity):
    """Класс для представления заказа"""

    def __init__(self, product: Product, quantity: int = 1):
        self.product = product
        self.quantity = quantity

    def calculate_total(self) -> float:
        """Реализация абстрактного метода - общая стоимость заказа"""
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, {self.quantity} шт., Итого: {self.calculate_total()} руб."
