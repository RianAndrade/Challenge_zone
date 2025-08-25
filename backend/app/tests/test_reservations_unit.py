import pytest
from datetime import date
from decimal import Decimal

from app.service.reservation import (
    _get_property_price,
    calculate_days_reserved,
    create_reservation,
    list_reservations,
    deactivate_reservation,
)
from app.db.schema import ReservationCreate
from app.tests.factories import persist_property, persist_reservation


def test_calculate_days_reserved_ok():
    days = calculate_days_reserved(date(2025, 9, 1), date(2025, 9, 4))
    assert days == 3

def test_calculate_days_reserved_erro():
    with pytest.raises(ValueError):
        calculate_days_reserved(date(2025, 9, 4), date(2025, 9, 4))
    with pytest.raises(ValueError):
        calculate_days_reserved(date(2025, 9, 5), date(2025, 9, 4))

def test_get_property_price_ok(db_session):
    p = persist_property(db_session, price_per_night=Decimal("150.00"))
    price = _get_property_price(db_session, p.id)
    assert price == 150

def test_get_property_price_not_found(db_session):
    with pytest.raises(ValueError):
        _get_property_price(db_session, 999)

def test_create_reservation_calcula_total_e_persiste(db_session):
    p = persist_property(db_session, price_per_night=Decimal("80.00"))

    payload = ReservationCreate(
        property_id=p.id,
        client_name="Ciclano",
        client_email="ciclano@example.com",
        start_date=date(2025, 9, 10),
        end_date=date(2025, 9, 13),  # 3 
        guests_quantity=2,
    )

    resp = create_reservation(db_session, payload)
    obj = resp["reservation"]
    assert resp["message"].startswith("Reserva Feita com Sucesso")
    # 3 * 80 = 240.00
    assert Decimal(obj.total_price) == Decimal("240.00")
    assert obj.is_active is True

def test_list_reservations_filtros(db_session):
    p1 = persist_property(db_session)
    p2 = persist_property(db_session, title="Chalé", price_per_night=Decimal("200.00"))

    persist_reservation(db_session, property_id=p1.id, client_email="a@x.com")
    persist_reservation(db_session, property_id=p2.id, client_email="b@y.com")

    all_res = list_reservations(db_session)
    assert len(all_res) == 2

    only_a = list_reservations(db_session, client_email="a@x.com")
    assert len(only_a) == 1
    assert only_a[0].client_email == "a@x.com"

    only_p2 = list_reservations(db_session, property_id=p2.id)
    assert len(only_p2) == 1
    assert only_p2[0].property_id == p2.id

def test_deactivate_reservation_ok(db_session):
    p = persist_property(db_session)
    res = persist_reservation(db_session, property_id=p.id, is_active=True)
    out = deactivate_reservation(db_session, res.id)
    assert out.is_active is False

def test_deactivate_reservation_inexistente(db_session):
    out = deactivate_reservation(db_session, 999)
    assert out is None

def test_deactivate_reservation_ja_inativa(db_session):
    p = persist_property(db_session)
    res = persist_reservation(db_session, property_id=p.id, is_active=False)
    out = deactivate_reservation(db_session, res.id)
    assert out.is_active is False


def _noop_check_availability(*args, **kwargs):
    return None


def test_create_reservation_endpoint__201(client, db_session, monkeypatch):

    import app.routes.reservations as reservations_router
    monkeypatch.setattr(reservations_router, "check_availability", _noop_check_availability)

    p = persist_property(db_session, price_per_night=Decimal("100.00"))

    payload = {
        "property_id": p.id,
        "client_name": "Fulana",
        "client_email": "fulana@example.com",
        "start_date": str(date(2025, 9, 1)),
        "end_date": str(date(2025, 9, 4)),  
        "guests_quantity": 2
    }

    r = client.post("/reservations", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert "message" in data and "valor total" in data["message"]
    assert "reservation" in data
    assert data["reservation"]["is_active"] is True
   
    total = Decimal(str(data["reservation"]["total_price"]))
    assert total == Decimal("300.00")


def test_create_reservation_endpoint__409_property_nao_existe(client, db_session, monkeypatch):
    import app.routes.reservations as reservations_router
    monkeypatch.setattr(reservations_router, "check_availability", _noop_check_availability)

    payload = {
        "property_id": 9999,
        "client_name": "Zé",
        "client_email": "ze@example.com",
        "start_date": "2025-09-01",
        "end_date": "2025-09-02",
        "guests_quantity": 1
    }
    r = client.post("/reservations", json=payload)
    assert r.status_code == 409
    assert "Propriedade" in r.json()["detail"]


def test_list_reservations_endpoint__sem_filtros(client, db_session):
    p = persist_property(db_session)
    persist_reservation(db_session, property_id=p.id, client_email="a@x.com")
    persist_reservation(db_session, property_id=p.id, client_email="b@y.com")

    r = client.get("/reservations")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_list_reservations_endpoint__filtro_email(client, db_session):
    p = persist_property(db_session)
    persist_reservation(db_session, property_id=p.id, client_email="alfa@ex.com")
    persist_reservation(db_session, property_id=p.id, client_email="beta@ex.com")

    r = client.get("/reservations", params={"client_email": "alfa@ex.com"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["client_email"] == "alfa@ex.com"


def test_deactivate_reservation_endpoint__200(client, db_session):
    p = persist_property(db_session)
    res = persist_reservation(db_session, property_id=p.id, is_active=True)

    r = client.put(f"/reservations/{res.id}/cancel")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == res.id
    assert data["is_active"] is False


def test_deactivate_reservation_endpoint__404(client):
    r = client.put("/reservations/999999/cancel")
    assert r.status_code == 404
    assert r.json()["detail"] == "Reservation not found"
