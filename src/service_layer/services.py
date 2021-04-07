from src.uow.abstract_uow import AbstractUnitOfWork
from typing import Optional
from src.model.batch import Batch
from src.repository.abstract_repository import AbstractRepository
from src.model.order_line import OrderLine
from src.model import OutOfStock
from datetime import date


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    batches = uow.batches.list()
    if not is_valid_sku(sku, batches):
        raise InvalidSku(f"Invalid sku {sku}")
    try:
        batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))
    except StopIteration:
        raise OutOfStock(f"No batches available for sku {line.sku}")
    batch.allocate(line)
    return str(batch)


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date], uow: AbstractUnitOfWork
):
    uow.batches.add(Batch(ref, sku, qty, eta))


def reallocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    batch = uow.batches.get(sku=line.sku)
    if batch is None:
        raise InvalidSku(f"Invalid sku {sku}")
    batch.deallocate(line)
    batchref = allocate(orderid, sku, qty, uow)
    return batchref
