# app/tests/factories.py
from datetime import date
from decimal import Decimal
from app.db.models import Property, Reservation

def make_property(**overrides) -> Property:
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
    return Property(**data)

def persist_property(db, **overrides) -> Property:
    prop = make_property(**overrides)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

def make_reservation(**overrides) -> Reservation:
    data = {
        "property_id": 1,
        "client_name": "Fulano",
        "client_email": "fulano@example.com",
        "start_date": date(2025, 9, 1),
        "end_date": date(2025, 9, 4),
        "guests_quantity": 2,
        "is_active": True,
        "total_price": None,
    }
    data.update(overrides)
    return Reservation(**data)

def persist_reservation(db, **overrides) -> Reservation:
    res = make_reservation(**overrides)
    db.add(res)
    db.commit()
    db.refresh(res)
    return res
