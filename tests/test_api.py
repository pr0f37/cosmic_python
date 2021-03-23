from uuid import uuid4
import src.config as config


def random_suffix():
    return uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


def test_api_returns_allocations(add_stock, app):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, othersku, 100, None),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()
    r = app.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.get_json()["batchref"] == earlybatch


def test_400_message_for_invalid_sku(app):
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = app.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.get_json()["message"] == f"Invalid sku {unknown_sku}"