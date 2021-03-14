from typing import List

from src.model.batch import Batch
from src.model.order_line import OrderLine


class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(batch for batch in batches if batch.can_allocate(line))
        batch.allocate(line)
        return batch
    except StopIteration:
        raise OutOfStock("No batches available for sku {line.sku}")
