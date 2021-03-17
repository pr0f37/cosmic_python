from sqlalchemy.orm import sessionmaker, clear_mappers, scoped_session
from sqlalchemy import create_engine
from src.orm import metadata, start_mappers


class Session:
    def __init__(self):
        engine = create_engine("sqlite:///:memory:")
        metadata.create_all(engine)
        start_mappers()
        self.session = scoped_session(sessionmaker(bind=engine))

    def __enter__(self):
        return self.session()

    def __exit__(self, type, value, traceback):
        clear_mappers()
