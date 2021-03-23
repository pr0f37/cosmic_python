import src.config as config
from sqlalchemy.orm import sessionmaker, clear_mappers, scoped_session
from sqlalchemy import create_engine
from src.orm import metadata, start_mappers
from app import create_app

from pytest import fixture
from pathlib import Path
import time


@fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@fixture
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    metadata.create_all(engine)
    return engine


@fixture
def postgres_session(postgres_db):
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@fixture
def add_stock(postgres_session):
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            postgres_session.execute(
                "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
                "values (:ref, :sku, :qty, :eta)",
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            [[batch_id]] = postgres_session.execute(
                "SELECT id FROM batches WHERE reference=:ref and sku=:sku",
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()

    clear_mappers()
    yield _add_stock
    start_mappers()
    for batch_id in batches_added:
        postgres_session.execute(
            "DELETE FROM allocations WHERE batch_id=:batch_id", dict(batch_id=batch_id)
        )
        postgres_session.execute(
            "DELETE FROM batches WHERE id=:batch_id", dict(batch_id=batch_id)
        )
    for sku in skus_added:
        postgres_session.execute(
            "DELETE FROM order_lines WHERE sku=:sku", dict(sku=sku)
        )
    postgres_session.commit()


@fixture
def app():
    app = create_app()
    app.testing = True
    return app.test_client()
