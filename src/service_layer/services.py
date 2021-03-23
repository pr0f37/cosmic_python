from src.repository.fake_repository import FakeSession
from src.repository.abstract_repository import AbstractRepository
from src.model.order_line import OrderLine
from src.model import OutOfStock


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(line: OrderLine, repo: AbstractRepository, session: FakeSession) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    try:
        batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))
    except StopIteration:
        raise OutOfStock(f"No batches available for sku {line.sku}")
    batch.allocate(line)
    session.commit()
    return str(batch)
