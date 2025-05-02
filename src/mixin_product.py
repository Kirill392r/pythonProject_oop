class ProductMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Создан объект {self.__class__.__name__} с параметрами: {args}")
