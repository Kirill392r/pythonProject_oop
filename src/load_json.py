import json
from src.product import Product
from src.category import Category

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