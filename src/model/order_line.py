from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

    def __add__(self, other):
        if self.sku == other.sku and self.orderid == other.orderid:
            qty = self.qty + other.qty
            return OrderLine(self.orderid, self.sku, qty)
        return None

    def __radd__(self, other):
        return self.qty + other
