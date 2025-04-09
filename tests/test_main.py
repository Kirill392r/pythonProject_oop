import json
import os
import tempfile

import pytest

from src.main import Category, Product, load_data_from_json


@pytest.fixture
def sample_json_file():
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


def test_load_data_success(sample_json_file):
    categories = load_data_from_json(sample_json_file)

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert len(categories[0].products) == 1
    assert categories[0].products[0].name == "Тестовый товар"
    assert categories[0].products[0].price == 100.0
    assert categories[0].products[0].quantity == 5


def test_load_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load_data_from_json("nonexistent.json")


def test_load_invalid_json():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
        tmp.write("invalid json")
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError):
            load_data_from_json(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_missing_required_field():
    invalid_data = [{"name": "Категория", "products": []}]

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
        json.dump(invalid_data, tmp)
        tmp_path = tmp.name

    try:
        with pytest.raises(KeyError):
            load_data_from_json(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_empty_products_list():
    category = Category("Категория", "Описание", [])
    assert "Товары:\n" in str(category)


def test_multiple_products():
    p1 = Product("Товар1", "Описание1", 100, 1)
    p2 = Product("Товар2", "Описание2", 200, 2)
    category = Category("Категория", "Описание", [p1, p2])
    assert len(category.products) == 2
    assert "Товар1" in str(category)
    assert "Товар2" in str(category)
