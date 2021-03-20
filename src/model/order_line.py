from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

    def __add__(self, other):
        if self.sku == other.sku and self.orderid == other.orderid:
            qty = self.qty + other.qty
            return OrderLine(self.orderid, self.sku, qty)
        raise ValueError(f"Cannot add two OrderLines with different sku or orderid")

    def __radd__(self, other):
        return self.qty + other
