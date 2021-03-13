###############
Domain Modeling
###############
Correct Domain Driven Desing should result in domain object representation reflected in minimal yet complete set of class definitions.
Classes should be reflecting the behavior and possible states of the objects of business model.
Their characteristics should directly explain their behavior.

Data Classes
------------
They should be used to represent static objects with no behavior.

* ``@dataclass`` decorator in python introduces several optimizations for class objects. For example it automatically adds ``__init__()`` method initializing all the class fields.
* ``@dataclass(frozen=True)`` makes the class fields immutable


Domain Model
------------
This is the domain model right now

.. mermaid::

    classDiagram
        Batch --> OrderLine
        class OrderLine{
            orderid: str
            sku: str
            qty: int
        }
        class Batch{
            reference: str
            sku: str
            eta: date
            available_quantity: int
            can_allocate(order_line: OrderLine)
            allocate(order_line: OrderLine)
        }
