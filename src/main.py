import json
from typing import List


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
        self.__price = price
        self.quantity = quantity
        self.multiplication = price * quantity

    def __str__(self) -> str:
        """Строковое отображение"""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение цены всего товара"""
        return self.multiplication + other.multiplication

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input(f"Понизить цену с {self.__price} до {new_price}")
            if answer != "y":
                print("Отмена действия")
                return
        self.__price = new_price
        print("Цена успешно изменена")

    @classmethod
    def new_product(cls, product_data: dict, products: list["Product"] = None) -> "Product":
        """Создает новый товар из словаря с данными"""
        if products is None:
            products = []
        for product in products:
            if product.name == product_data["name"]:
                product.quantity += product_data["quantity"]
                product.price = max(product.price, product_data["price"])
                return product
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=float(product_data["price"]),
            quantity=int(product_data["quantity"]),
        )


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
        """Добавление товарок в категорию"""
        self.__products.append(product_obj)
        Category.category_count += 1

    @property
    def products(self) -> list:
        """Формируем вывод списка товаров"""
        return [f"{p.name}, {p.price}. Остаток: {p.quantity}." for p in self.__products]


def load_data_from_json(file_path: str) -> list[Category]:
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
