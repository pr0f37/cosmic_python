from datetime import date
from src.model.order_line import OrderLine
from src.model.batch import Batch

from src.repository.sqlalchemy_repository import SqlAlchemyRepository


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        OrderLine("order1", "RED-CHAIR", 12),
        OrderLine("order1", "RED-TABLE", 13),
        OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    newline = OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(newline)
    session.commit()

    row = session.execute("Select orderid, sku, qty FROM order_lines").first()
    assert OrderLine(*row) == newline


def test_sqlachelmy_repo(session):
    repo = SqlAlchemyRepository(session)
    batch = Batch("ref_id1", "LAMP", 20, date.today())
    repo.add(batch)
    batch2 = repo.get("ref_id1")
    assert batch == batch2


def insert_order_line(session):
    session.execute(
        "INSERT into order_lines (orderid, sku, qty)"
        "VALUES ('order1', 'GENERIC-SOFA', 12)"
    )
    [[orderline_id]] = session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


def insert_batch(session, reference):
    session.execute(
        "INSERT INTO batches (reference, sku,  _purchased_quantity)"
        "VALUES (:reference, 'GENERIC-SOFA', 100)",
        dict(reference=reference),
    )
    [[batch_id]] = session.execute(
        "SELECT id FROM batches WHERE reference=:reference",
        dict(reference=reference),
    )
    return batch_id


def insert_allocation(session, order_line_id, batch_id):
    session.execute(
        "INSERT INTO allocations (batch_id, order_line_id)"
        "VALUES (:batch_id, :order_line_id) ",
        dict(batch_id=batch_id, order_line_id=order_line_id),
    )


def test_a_repository_can_retrieve_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")
    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {OrderLine("order1", "GENERIC-SOFA", 12)}
