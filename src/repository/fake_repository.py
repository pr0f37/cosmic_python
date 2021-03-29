from typing import List
from src.model.batch import Batch
from src.repository.abstract_repository import AbstractRepository


class FakeRepository(AbstractRepository):
    @staticmethod
    def for_batch(ref, sku, qty, eta=None):
        return FakeRepository([Batch(ref, sku, qty, eta)])

    def __init__(self, batches: List[Batch]):
        self._batches = set(batches)

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, reference: str) -> Batch:
        return next(batch for batch in self._batches if batch.reference == reference)

    def list(self):
        return sorted(list(self._batches))


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True
