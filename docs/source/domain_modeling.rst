###############
Domain Modeling
###############
Correct Domain Driven Design should result in domain object representation reflected in minimal yet complete set of class definitions.
Classes should be reflecting the behavior and possible states of the objects of business model.
Their characteristics should directly explain their behavior.

Data Classes
------------
They should be used to represent static objects with no behavior.

* ``@dataclass`` decorator in python introduces several optimizations for class objects. For example it automatically adds ``__init__()`` method initializing all the class fields
* ``@dataclass(frozen=True)`` makes the class fields immutable


Initial Domain Model
--------------------
The first idea of the model is as follows:

.. mermaid::

    classDiagram
        Batch o-- OrderLine
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
            allocations: set[OrderLine]
            can_allocate(order_line: OrderLine)
            allocate(order_line: OrderLine)
            deallocate(order_line: OrderLine)
        }

OrderLine data class which is static (immutable) and serves only and the data aggregate.
Batch class is a standard mutable object which references multiple OrderLine objects to reflect allocation state.
Flaw of the current implementation is that class fields change every time allocation is successful - quantity values are being decremented and saved.
This adds unneeded update operations and changes the class state making its state history untraceable and calculation correctness unverifiable.

Domain Model Evolution
----------------------
In order to keep allocation history and simplify the code following changes has been introduced.
Previously constantly updated *current* ``available_quantity`` field
has been changed to private static ``_allocated_quantity`` field which is set  only once - during class initialization.
The available quantity is now a dynamically calculated ``@property`` field. The ``OrderLine`` ``__radd__()`` operator method has been overloaded allowing us to simply
call ``sum()`` method on the ``_allocations`` set to simplify the code responsible for dynamic
quantity calculation in ``Batch`` class.

.. mermaid::

    classDiagram
        Batch o-- OrderLine
        class OrderLine{
            orderid: str
            sku: str
            qty: int
        }
        class Batch{
            reference: str
            sku: str
            eta: date
            _allocated_quantity: int
            _allocations: set[OrderLine]
            available_quantity: int
            can_allocate(order_line: OrderLine)
            allocate(order_line: OrderLine)
            deallocate(order_line: OrderLine)
        }
