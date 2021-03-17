from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey


from src.model.order_line import OrderLine
from src.model.batch import Batch

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderid", String(255)),
    Column(
        "sku",
        String(255),
    ),
    Column("qty", Integer, nullable=False),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "sku",
        String(255),
    ),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("reference", String(255)),
    Column("eta", Date()),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("batch_id", ForeignKey("batches.id")),
    Column("order_line_id", ForeignKey("order_lines.id")),
)


def start_mappers():
    lines_mapper = mapper(OrderLine, order_lines)
    mapper(
        Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set
            )
        },
    )
