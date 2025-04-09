import json
from typing import List, Dict, Any


class Product:
    """Класс для представления товара в магазине"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует экземпляр класса Product"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Возвращает строковое представление товара"""
        return f"Product(name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity})"

    def __repr__(self) -> str:
        """Возвращает формальное строковое представление товара"""
        return self.__str__()


class Category:
    """Класс для представления категории товаров в магазине"""

    name: str
    description: str
    products: List[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """Инициализирует экземпляр класса Category"""
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count = len(products)

    def __str__(self) -> str:
        """Возвращает строковое представление категории"""
        products_str = "\n".join(f"  - {product}" for product in self.products)
        return f"Категория: {self.name}\n{self.description}\nТовары:\n{products_str}"

    def __repr__(self) -> str:
        """Возвращает формальное строковое представление категории"""
        return f"Category({self.name!r}, {self.description!r}, {self.products!r})"


def load_data_from_json(file_path: str) -> List[Category]:
    """Загружает данные из JSON файла и создает объекты Category и Product"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        categories = []

        for category_data in data:
            products = []
            for product_data in category_data["products"]:
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=float(product_data["price"]),
                    quantity=int(product_data["quantity"]),
                )
                products.append(product)

            category = Category(
                name=category_data["name"],
                description=category_data["description"],
                products=products,
            )
            categories.append(category)

        return categories

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except json.JSONDecodeError:
        raise ValueError("Ошибка декодирования JSON файла")
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательное поле в данных: {e}")
