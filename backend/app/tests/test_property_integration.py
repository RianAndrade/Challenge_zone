from datetime import date
from app.tests.conftest import _mk_property, _mk_reservation


def test_list_properties_endpoint__sem_filtros(client, db_session):
    p1 = _mk_property(db_session, address_city="Florianópolis", address_state="SC")
    p2 = _mk_property(db_session, address_city="São Paulo", address_state="SP")

    r = client.get("/properties/list")
    assert r.status_code == 200
    data = r.json()
    ids = [item["id"] for item in data]
    assert p1.id in ids and p2.id in ids


def test_list_properties_endpoint__filtros(client, db_session):
    p1 = _mk_property(db_session, address_city="Florianópolis", address_state="SC", address_neighborhood="Centro")
    _mk_property(db_session, address_city="São Paulo", address_state="SP", address_neighborhood="Bela Vista")

    r = client.get("/properties/list", params={"address_city": "Florianópolis"})
    assert r.status_code == 200
    data = r.json()
    assert [x["id"] for x in data] == [p1.id]


def test_list_properties_endpoint__capacidade_preco(client, db_session):
    _mk_property(db_session, capacity=2, price_per_night=300)
    p_ok = _mk_property(db_session, capacity=5, price_per_night=150)
    _mk_property(db_session, capacity=8, price_per_night=400)

    r = client.get("/properties/list", params={"capacity": 4, "price_per_night": 200})
    assert r.status_code == 200
    data = r.json()
    assert [x["id"] for x in data] == [p_ok.id]

def test_availability_endpoint__ok(client, db_session):
    p = _mk_property(db_session, capacity=4)

    _mk_reservation(db_session, property_id=p.id, start_date=date(2025, 8, 10), end_date=date(2025, 8, 12))

    r = client.get("/properties/availability", params={
        "property_id": p.id,
        "start_date": "2025-08-13",
        "end_date": "2025-08-15",
        "guests_quantity": 3
    })
    assert r.status_code == 200
    assert r.json()["message"]


def test_availability_endpoint__faltando_parametros(client):
    r = client.get("/properties/availability", params={
        "property_id": 1,
        "start_date": "2025-08-13",
        # end_date 
        "guests_quantity": 2
    })
    assert r.status_code == 400
    assert "Todos os dados" in r.json()["detail"]


def test_create_property_endpoint__201(client):
    payload = {
        "title": "Casa Nova",
        "address_street": "Rua Beta",
        "address_number": "55",
        "address_neighborhood": "Centro",
        "address_city": "Florianópolis",
        "address_state": "SC",
        "country": "BRA", 
        "rooms": 2,
        "capacity": 4,
        "price_per_night": 200
    }
    r = client.post("/properties", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Casa Nova"
    assert body["id"] > 0


def test_delete_property_endpoint__204_e_404(client, db_session):
    p = _mk_property(db_session)
    r = client.delete(f"/properties/{p.id}")
    assert r.status_code == 204

    r2 = client.delete(f"/properties/{p.id}")  
    assert r2.status_code == 404
