from src.model.order_line import OrderLine
from src.config import get_postgres_uri
from pytest import fixture, raises
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.service_layer.services import add_batch
from time import time


@fixture
def session_factory():
    return sessionmaker(bind=create_engine(get_postgres_uri()))


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        add_batch("batch1", "MEDIUM-PLINTH", 100, None, uow)

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        with raises(MyException):
            add_batch("batch1", "LARGE-FORK", 100, None, uow)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []


def try_to_allocate(orderid, sku, exceptions):
    line = OrderLine(orderid, sku, 10)
    try:
        with SqlAlchemyUnitOfWork() as uow:
            product = uow.product.get(sku=sku)
            product.allocate(line)
            time.sleep(0.2)
            uow.commit()
    except Exception as e:
        print(e)
