from src.model.batch import Batch
from src.model.order_line import OrderLine
from src.main import allocate
from datetime import date


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, qty=batch_qty, eta=date.today()),
        OrderLine("order-ref", sku, line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", batch_qty=20, line_qty=2)
    batch.allocate(line)

    assert batch.available_quantity == 18


def test_cannot_allocate_more_quantity_than_available():
    batch, line = make_batch_and_line("BLUE-CUSHION", batch_qty=1, line_qty=2)
    batch.allocate(line)

    assert batch.available_quantity == 1


def test_allocating_the_same_orderline_twice():
    batch, line = make_batch_and_line("BLUE-VASE", batch_qty=10, line_qty=2)
    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 8


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


def test_allocate_orderline_to_batches_set():
    batch, line = make_batch_and_line("DECORATIVE-TRINKET", 20, 22)
    allocateable_batch = Batch("ref00001", "DECORATIVE-TRINKET", 30, date.today())
    allocated_batch = allocate(line, [batch, allocateable_batch])
    assert allocated_batch == allocateable_batch
