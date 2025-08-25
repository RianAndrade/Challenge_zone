from datetime import date
from decimal import Decimal
from app.db.models import Property


def _persist_property(db, **overrides) -> Property:
    data = {
        "title": "Casa Bacana",
        "address_street": "Rua A",
        "address_number": "123",
        "address_neighborhood": "Centro",
        "address_city": "Januária",
        "address_state": "MG",
        "country": "BR",
        "rooms": 3,
        "capacity": 6,
        "price_per_night": Decimal("100.00"),
    }
    data.update(overrides)
    obj = Property(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def test_create_reservation__201_persiste_total_price(client, db_session):
   
    prop = _persist_property(db_session, price_per_night=Decimal("120.00"), capacity=4)

    payload = {
        "property_id": prop.id,
        "client_name": "Fulana de Tal",
        "client_email": "fulana@example.com",
        "start_date": str(date(2025, 9, 1)),
        "end_date": str(date(2025, 9, 4)),  # 3 noites
        "guests_quantity": 2,
    }

    resp = client.post("/reservations", json=payload)
    assert resp.status_code == 201, resp.text

    body = resp.json()
    assert "message" in body and "valor total" in body["message"]
    assert "reservation" in body

    res = body["reservation"]
    assert res["property_id"] == prop.id
    assert res["client_email"] == "fulana@example.com"
    assert res["is_active"] is True

    #  3 * 120.00 = 360.00
    total = Decimal(str(res["total_price"]))
    assert total == Decimal("360.00")


    list_resp = client.get("/reservations")
    assert list_resp.status_code == 200
    arr = list_resp.json()
    assert isinstance(arr, list) and len(arr) == 1
    assert arr[0]["id"] == res["id"]


def test_create_reservation__409_datas_invalidas(client, db_session):
    prop = _persist_property(db_session)

  
    payload = {
        "property_id": prop.id,
        "client_name": "Erro Datas",
        "client_email": "erro@example.com",
        "start_date": "2025-09-05",
        "end_date": "2025-09-05",
        "guests_quantity": 1,
    }
    resp = client.post("/reservations", json=payload)
    assert resp.status_code == 409
    assert "data final" in resp.json()["detail"].lower()

def test_list_reservations__filtros_por_email_e_property(client, db_session):
    http = client 

    p1 = _persist_property(db_session, price_per_night=Decimal("80.00"))
    p2 = _persist_property(db_session, price_per_night=Decimal("200.00"))

    r1 = http.post(
        "/reservations",
        json={
            "property_id": p1.id,
            "client_name": "A",
            "client_email": "a@x.com",
            "start_date": "2025-09-10",
            "end_date": "2025-09-12",
            "guests_quantity": 1,
        },
    )
    r2 = http.post(
        "/reservations",
        json={
            "property_id": p2.id,
            "client_name": "B",
            "client_email": "b@y.com",
            "start_date": "2025-09-15",
            "end_date": "2025-09-18",
            "guests_quantity": 2,
        },
    )
    assert r1.status_code == 201 and r2.status_code == 201

    all_resp = http.get("/reservations")
    assert all_resp.status_code == 200
    all_items = all_resp.json()
    assert len(all_items) == 2

    email_resp = http.get("/reservations", params={"client_email": "a@x.com"})
    assert email_resp.status_code == 200
    email_items = email_resp.json()
    assert len(email_items) == 1
    assert email_items[0]["client_email"] == "a@x.com"

    pid_resp = http.get("/reservations", params={"property_id": p2.id})
    assert pid_resp.status_code == 200
    pid_items = pid_resp.json()
    assert len(pid_items) == 1
    assert pid_items[0]["property_id"] == p2.id

def test_cancel_reservation__200_e_reflete_inativacao(client, db_session):
    prop = _persist_property(db_session)

    create = client.post(
        "/reservations",
        json={
            "property_id": prop.id,
            "client_name": "Cancelar",
            "client_email": "cancel@example.com",
            "start_date": "2025-09-20",
            "end_date": "2025-09-22",
            "guests_quantity": 2,
        },
    )
    assert create.status_code == 201
    res_id = create.json()["reservation"]["id"]


    cancel = client.put(f"/reservations/{res_id}/cancel")
    assert cancel.status_code == 200
    data = cancel.json()
    assert data["id"] == res_id
    assert data["is_active"] is False

   
    listed = client.get("/reservations").json()
    [item] = [x for x in listed if x["id"] == res_id]
    assert item["is_active"] is False


def test_cancel_reservation__404_nao_existe(client):
    resp = client.put("/reservations/999999/cancel")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Reservation not found"
