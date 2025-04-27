from typing import List

from src.product import Product


class Category:
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
        return [f"{p.name}, {p.price}. Остаток: {p.quantity}." for p in self.__products]
