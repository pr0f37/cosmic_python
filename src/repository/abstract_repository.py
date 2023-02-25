from abc import ABC, abstractmethod
from typing import List
from src.allocation.domain.model import Product


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def get(self, sku) -> Product:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Product]:
        raise NotImplementedError
