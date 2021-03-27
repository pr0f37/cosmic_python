from datetime import datetime
from src.repository.sqlalchemy_repository import SqlAlchemyRepository

from src.model.order_line import OrderLine
from src.model import OutOfStock
from src.orm.session import Session
from flask import Flask, request
import src.config as config
import src.service_layer.services as services


def create_app():
    app = Flask(__name__)

    @app.route("/allocate", methods=["POST"])
    def allocate_with_repo():
        with Session(config.get_postgres_uri()) as session:
            repo = SqlAlchemyRepository(session)
            try:
                batchref = services.allocate(
                    request.json["orderid"],
                    request.json["sku"],
                    request.json["qty"],
                    repo,
                    session,
                )
            except (OutOfStock, services.InvalidSku) as e:
                return (
                    {"message": str(e)},
                    400,
                )
        return {"batchref": str(batchref)}, 201

    @app.route("/add_batch", methods=["POST"])
    def add_batch():
        with Session(config.get_postgres_uri()) as session:
            repo = SqlAlchemyRepository(session)
            eta = request.json.get("eta")
            if eta:
                eta = datetime.fromisoformat(eta).date()
            services.add_batch(
                request.json["ref"],
                request.json["sku"],
                request.json["qty"],
                eta,
                repo,
                session,
            )

        return {"message": "Batch added"}, 201

    return app
