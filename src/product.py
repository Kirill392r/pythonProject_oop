from src.base_task import BaseProduct
from src.mixin_product import ProductMixin


class Product(ProductMixin, BaseProduct):
    """Класс для представления товара в магазине"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует экземпляр класса Product"""
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        self.multiplication = price * quantity
        super().__init__(name, description, price, quantity)

    def __repr__(self):
        return f"({self.name}, {self.description}, {self.__price}, {self.quantity})"

    def __str__(self) -> str:
        """Строковое отображение"""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение цены товара"""
        if type(self) is not type(other):
            raise TypeError
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


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
