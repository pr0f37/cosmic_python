from datetime import date, timedelta
from pytest import fixture, raises
from src.service_layer.services import allocate, add_batch, InvalidSku
from src.repository.fake_repository import FakeRepository, FakeSession
from src.uow.abstract_uow import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.batches = FakeRepository([])
        self.commited = False

    def __enter__(self, *args):
        pass

    def __exit__(self, *args):
        return super().__exit__(*args)

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


def test_add_batch():
    uow = FakeUnitOfWork()
    add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.commited


def test_allocate_return_allocation():
    uow = FakeUnitOfWork()
    add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"


@fixture
def tomorrow():
    return date.today() + timedelta(days=1)


def test_prefers_current_stock_batches_to_shipments(tomorrow):
    repo, session = FakeRepository([]), FakeSession()
    add_batch("in-stock-batch", "RETRO-CLOCK", 100, None, repo, session)
    add_batch("shipment_batch", "RETRO-CLOCK", 100, tomorrow, repo, session)
    allocate("oref", "RETRO-CLOCK", 10, repo, session)
    [in_stock_batch, shipment_batch] = repo.list()
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
    result = allocate("oref", "COMPLICATED-LAMP", 10, repo, session)
    assert result == "batch1"


def test_returns_allocation_repo_factory_method():
    repo = FakeRepository.for_batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
    session = FakeSession()
    result = allocate("oref", "COMPLICATED-LAMP", 10, repo, session)
    assert result == "batch1"


def test_add_batches():
    repo, session = FakeRepository([]), FakeSession()
    add_batch("batch1", "ARMCHAIR", 100, None, repo, session)
    assert repo.get("batch1").reference == "batch1"
    assert session.committed


def test_allocate_errors_for_invalid_sku():
    repo, session = FakeRepository([]), FakeSession()
    add_batch("b1", "AREALSKU", 100, None, repo, session)

    with raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())
