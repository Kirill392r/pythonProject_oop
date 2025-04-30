from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный класс для класса продуктов"""

    @classmethod
    @abstractmethod
    def __init__(cls, *args, **kwargs):
        pass


class BaseEntity(ABC):
    """Абстрактный класс для сущностей с общей функциональностью"""

    @classmethod
    @abstractmethod
    def calculate_total(cls, *args, **kwargs) -> float:
        """Абстрактный метод для расчета общей стоимости"""
        pass
