from src.model.batch import Batch
from src.repository.abstract_repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        return self.session.add(batch)

    def get(self, reference) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).first()

    def list(self):
        return self.session.query(Batch).all()
