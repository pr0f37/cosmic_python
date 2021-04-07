from src.orm import start_mappers
from src.repository.sqlalchemy_repository import SqlAlchemyRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from src.config import get_postgres_uri
from src.uow.abstract_uow import AbstractUnitOfWork

DEFAULT_SESION_FACTORY = sessionmaker(bind=create_engine(get_postgres_uri()))


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        start_mappers()
        self.session = self.session_factory()
        self.batches = SqlAlchemyRepository(self.session)
        return self.session

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
        clear_mappers()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
