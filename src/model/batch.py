from src.model.order_line import OrderLine
from datetime import date
from typing import Set


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    def __hash__(self):
        return hash(self.reference)

    def __eq__(self, o: object) -> bool:
        try:
            return self.reference == o.reference
        except AttributeError:
            return False

    def __repr__(self) -> str:
        return f"{self.reference}"

    def __lt__(self, o: object) -> bool:
        try:
            return self.eta < o.eta
        except (AttributeError, TypeError):
            return False

    @property
    def available_quantity(self):
        return self._purchased_quantity - sum(self._allocations)

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.pop(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            order_line not in self._allocations
            and self.available_quantity >= order_line.qty
            and self.sku == order_line.sku
        )
