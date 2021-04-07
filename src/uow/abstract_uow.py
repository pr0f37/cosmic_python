from abc import ABC, abstractmethod
from src.repository.abstract_repository import AbstractRepository


class AbstractUnitOfWork(ABC):
    batches: AbstractRepository

    @abstractmethod
    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
