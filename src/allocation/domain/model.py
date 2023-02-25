from src.model.order_line import OrderLine
from src.model.batch import Batch
from src.model import OutOfStock
from typing import List, Optional


class Product:
    def __init__(
        self, sku: str, batches: List[Batch], version_number: Optional[int] = 0
    ) -> None:
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> None:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {line.sku}")
