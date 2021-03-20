from datetime import date
from src.repository.sqlalchemy_repository import SqlAlchemyRepository
from src.main import allocate
from src.model.batch import Batch
from src.model.order_line import OrderLine
from src.orm.session import Session
from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    @app.route("/allocate")
    def allocate_endpoint():
        with Session() as session:
            # session = start_session()
            line = OrderLine("id1", "LAMP", 10)
            batch = Batch("ref1", "LAMP", 21, date.today())
            allocate(line, [batch])
            session.add(line)
            session.add(batch)
            session.commit()
        return jsonify({"message": "DONE!"}), 200

    @app.route("/repo")
    def allocate_with_repo():
        batches = []
        with Session() as session:
            repo = SqlAlchemyRepository(session)
            line = OrderLine("id2", "LAMP", 10)
            batches = repo.list()
            allocate(line, batches)
            session.commit()
            batches = session.query(Batch).all()
        return jsonify(batches), 200

    @app.route("/list")
    def list_batches():
        with Session() as session:
            return jsonify(session.query(Batch).all()), 200

    return app
