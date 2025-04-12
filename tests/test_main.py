import json
import os
import tempfile

import pytest

from src.main import Category, Product, load_data_from_json


@pytest.fixture
def sample_json_file() -> str:
    """Фикстура для создания временного JSON-файла с тестовыми данными."""
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Тестовое описание",
            "products": [
                {
                    "name": "Тестовый товар",
                    "description": "Тестовое описание товара",
                    "price": 100.0,
                    "quantity": 5,
                }
            ],
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf8", delete=False, suffix=".json") as tmp:
        json.dump(test_data, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    yield tmp_path
    os.unlink(tmp_path)


def test_load_data_success(sample_json_file: str) -> None:
    """Тест успешной загрузки данных из JSON файла."""
    categories = load_data_from_json(sample_json_file)

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert len(categories[0].add_product) == 1
    assert "Тестовый товар" in categories[0].add_product[0]
    assert "100.0" in categories[0].add_product[0]
    assert "5" in categories[0].add_product[0]


def test_load_nonexistent_file() -> None:
    """Тест обработки случая с несуществующим файлом."""
    with pytest.raises(FileNotFoundError):
        load_data_from_json("nonexistent.json")


def test_load_invalid_json() -> None:
    """Тест обработки некорректного JSON."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
        tmp.write("invalid json")
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError):
            load_data_from_json(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_missing_required_field() -> None:
    """Тест обработки отсутствия обязательных полей в данных."""
    invalid_data = [{"name": "Категория", "products": []}]

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
        json.dump(invalid_data, tmp)
        tmp_path = tmp.name

    try:
        with pytest.raises(KeyError):
            load_data_from_json(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_empty_products_list() -> None:
    """Тест работы с пустым списком товаров."""
    category = Category("Категория", "Описание", [])
    assert len(category.add_product) == 0


def test_multiple_products():
    """Тест работы с несколькими товарами в категории."""
    p1 = Product("Товар1", "Описание1", 100, 1)
    p2 = Product("Товар2", "Описание2", 200, 2)
    category = Category("Категория", "Описание", [p1, p2])
    assert len(category.add_product) == 2
    assert "Товар1" in category.add_product[0]
    assert "Товар2" in category.add_product[1]


def test_product_price_setter() -> None:
    """Тест сеттера цены товара с различными сценариями."""
    product = Product("Тест", "Тест", 100, 1)

    product.price = -50
    assert product.price == 100

    import builtins

    original_input = builtins.input
    builtins.input = lambda _: "y"
    product.price = 90
    assert product.price == 90
    builtins.input = original_input


def test_new_product_method() -> None:
    """Тест фабричного метода создания/обновления товара."""
    existing_product = Product("Существующий", "Товар", 100, 5)
    new_data = {"name": "Существующий", "description": "Товар", "price": 120, "quantity": 3}

    updated = Product.new_product(new_data, [existing_product])
    assert updated.quantity == 8

    new_product = Product.new_product(new_data)
    assert new_product.name == "Существующий"
