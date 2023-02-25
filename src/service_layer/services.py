from src.allocation.domain.model import Product
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
    product = uow.products.get(sku=line.sku)
    if not product:
        raise InvalidSku(f"Invalid sku {sku}")
    batch = product.allocate(line)
    return str(batch)


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date], uow: AbstractUnitOfWork
):
    # uow.batches.add(Batch(ref, sku, qty, eta))
    product = uow.products.get(sku=sku)
    if not product:
        product = Product(sku=sku, batches=[])
        uow.products.add(product=product)
    product.batches.append(Batch(ref=ref, sku=sku, qty=qty, eta=eta))
    uow.commit()


def reallocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    product = uow.products.get(sku=line.sku)
    if product is None:
        raise InvalidSku(f"Invalid sku {sku}")
    product.deallocate(line)
    batch = product.allocate(line)
    return str(batch)
