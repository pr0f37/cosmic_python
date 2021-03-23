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
            line = OrderLine(
                request.get_json()["orderid"],
                request.get_json()["sku"],
                request.get_json()["qty"],
            )
            repo = SqlAlchemyRepository(session)
            try:
                batchref = services.allocate(line, repo, session)
            except (OutOfStock, services.InvalidSku) as e:
                return (
                    {"message": str(e)},
                    400,
                )
        return {"batchref": str(batchref)}, 201

    return app
