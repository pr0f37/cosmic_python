from src.model.order_line import OrderLine
from datetime import date


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty
        self.orders = list()

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self.available_quantity -= order_line.qty
            self.orders.append(order_line)

    def can_allocate(self, order_line: OrderLine):
        return (
            order_line not in self.orders
            and self.available_quantity >= order_line.qty
            and self.sku == order_line.sku
        )
