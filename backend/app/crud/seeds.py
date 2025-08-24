# app/services/seed_service.py
from datetime import date
from decimal import Decimal
from typing import Dict, List, Tuple

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.models import Property, Reservation  # ajuste se seu path for diferente


# ---------- DADOS DO SEED ----------

def seed_properties_data() -> List[dict]:
    """Retorna exatamente 5 propriedades do seed."""
    return [
        {  # A: 2 reservas
            "title": "Casa da Mae Joana",
            "address_street": "Rua do Michael",
            "address_number": "2020",
            "address_neighborhood": "Centro",
            "address_city": "Luquetinha",
            "address_state": "MG",
            "country": "BRA",
            "rooms": 4,
            "capacity": 8,
            "price_per_night": Decimal("300.00"),
        },
        {  # B: 2 reservas
            "title": "Refúgio das Palmeiras",
            "address_street": "Av. Brasil",
            "address_number": "1500",
            "address_neighborhood": "Centro",
            "address_city": "Januária",
            "address_state": "MG",
            "country": "BRA",
            "rooms": 3,
            "capacity": 6,
            "price_per_night": Decimal("220.00"),
        },
        {  # C: 1 reserva
            "title": "Pouso do Cedro",
            "address_street": "Rua das Flores",
            "address_number": "88",
            "address_neighborhood": "Jardim",
            "address_city": "Montes Claros",
            "address_state": "MG",
            "country": "BRA",
            "rooms": 2,
            "capacity": 4,
            "price_per_night": Decimal("180.00"),
        },
        {  # D: 0 reservas
            "title": "Lagoa Serena",
            "address_street": "Rua da Lagoa",
            "address_number": "12",
            "address_neighborhood": "Lagoa",
            "address_city": "Pirapora",
            "address_state": "MG",
            "country": "BRA",
            "rooms": 5,
            "capacity": 10,
            "price_per_night": Decimal("350.00"),
        },
        {  # E: 0 reservas
            "title": "Vista do Vale",
            "address_street": "Alameda das Araucárias",
            "address_number": "501",
            "address_neighborhood": "Serra Verde",
            "address_city": "Diamantina",
            "address_state": "MG",
            "country": "BRA",
            "rooms": 3,
            "capacity": 5,
            "price_per_night": Decimal("260.00"),
        },
    ]


def seed_reservations_data() -> List[dict]:
    """
    Retorna 5 reservas na distribuição:
      - 2 na Casa da Mae Joana
      - 2 no Refúgio das Palmeiras
      - 1 no Pouso do Cedro
      - Lagoa Serena e Vista do Vale ficam sem reserva
    Cada item referencia a propriedade por 'property_title'.
    """
    return [
        # 2 reservas - Casa da Mae Joana
        {
            "property_title": "Casa da Mae Joana",
            "client_name": "Rian M",
            "client_email": "rian@example.com",
            "start_date": date(2025, 7, 28),
            "end_date": date(2025, 7, 30),
            "guests_quantity": 4,
        },
        {
            "property_title": "Casa da Mae Joana",
            "client_name": "Alice S",
            "client_email": "alice@example.com",
            "start_date": date(2025, 8, 10),
            "end_date": date(2025, 8, 12),
            "guests_quantity": 2,
        },

        # 2 reservas - Refúgio das Palmeiras
        {
            "property_title": "Refúgio das Palmeiras",
            "client_name": "João P",
            "client_email": "joao@example.com",
            "start_date": date(2025, 9, 5),
            "end_date": date(2025, 9, 8),
            "guests_quantity": 3,
        },
        {
            "property_title": "Refúgio das Palmeiras",
            "client_name": "Carla M",
            "client_email": "carla@example.com",
            "start_date": date(2025, 10, 1),
            "end_date": date(2025, 10, 3),
            "guests_quantity": 2,
        },

        # 1 reserva - Pouso do Cedro
        {
            "property_title": "Pouso do Cedro",
            "client_name": "Diego L",
            "client_email": "diego@example.com",
            "start_date": date(2025, 11, 15),
            "end_date": date(2025, 11, 17),
            "guests_quantity": 2,
        },
    ]


# ---------- CHECAGENS / REGRAS ----------

def _any_seed_property_exists(db: Session, titles: List[str]) -> List[str]:
    """Retorna títulos já existentes dentre os títulos do seed."""
    rows = db.query(Property).filter(Property.title.in_(titles)).all()
    return [r.title for r in rows]


def _any_seed_reservation_exists(db: Session, res_data: List[dict]) -> List[Tuple[str, str, date, date]]:
    """
    Checa se alguma reserva do seed já existe.
    Considera um 'match' por (property_id, client_email, start_date, end_date).
    Retorna uma lista de tuplas (property_title, client_email, start_date, end_date) já existentes.
    """
    duplicates = []

    # Precisamos mapear titles -> ids existentes no banco
    titles = sorted({r["property_title"] for r in res_data})
    props = db.query(Property).filter(Property.title.in_(titles)).all()
    prop_by_title = {p.title: p for p in props}

    for r in res_data:
        p = prop_by_title.get(r["property_title"])
        if not p:
            # se a property ainda não existe, essa reserva ainda não pode existir (ok)
            continue

        found = db.query(Reservation).filter(
            and_(
                Reservation.property_id == p.id,
                Reservation.client_email == r["client_email"],
                Reservation.start_date == r["start_date"],
                Reservation.end_date == r["end_date"],
            )
        ).first()
        if found:
            duplicates.append((r["property_title"], r["client_email"], r["start_date"], r["end_date"]))

    return duplicates


def _assert_seed_not_applied(db: Session):
    """Se QUALQUER item do seed já existir, lança 409 e não cria nada."""
    prop_titles = [p["title"] for p in seed_properties_data()]
    prop_dupes = _any_seed_property_exists(db, prop_titles)

    res_dupes = _any_seed_reservation_exists(db, seed_reservations_data())

    if prop_dupes or res_dupes:
        detail = {
            "message": "Seed já aplicada (foram encontrados dados do seed no banco).",
            "properties_duplicated": prop_dupes,
            "reservations_duplicated": [
                {
                    "property_title": t,
                    "client_email": email,
                    "start_date": sd.isoformat(),
                    "end_date": ed.isoformat(),
                }
                for (t, email, sd, ed) in res_dupes
            ],
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


# ---------- CRIAÇÃO ----------

def seed_5_properties(db: Session) -> Dict[str, Property]:
    """Cria exatamente 5 propriedades e retorna dict title -> Property."""
    created_map: Dict[str, Property] = {}
    for data in seed_properties_data():
        obj = Property(**data)
        db.add(obj)
        db.flush()  # garante ID após INSERT
        created_map[obj.title] = obj
    return created_map


def seed_5_reservations(db: Session, props_by_title: Dict[str, Property]) -> List[Reservation]:
    """Cria exatamente 5 reservas na distribuição definida em seed_reservations_data()."""
    created: List[Reservation] = []
    for r in seed_reservations_data():
        p = props_by_title.get(r["property_title"])
        if not p:
            # Como o orquestrador sempre cria as 5 props antes, isso não deve ocorrer.
            raise HTTPException(status_code=500, detail=f"Property '{r['property_title']}' não foi criada.")
        obj = Reservation(
            property_id=p.id,
            client_name=r["client_name"],
            client_email=r["client_email"],
            start_date=r["start_date"],
            end_date=r["end_date"],
            guests_quantity=r["guests_quantity"],
        )
        db.add(obj)
        db.flush()
        created.append(obj)
    return created


# ---------- ORQUESTRADOR ----------

def apply_full_seed(db: Session) -> dict:
    """
    Orquestra o seed:
      1) Falha com 409 se já existe qualquer dado do seed
      2) Cria 5 propriedades
      3) Cria 5 reservas (2 na A, 2 na B, 1 na C; D e E sem reservas)
      4) Commita e retorna resumo
    """
    _assert_seed_not_applied(db)

    try:
        props_by_title = seed_5_properties(db)
        res_created = seed_5_reservations(db, props_by_title)
        db.commit()
    except Exception:
        db.rollback()
        raise

    # resumo para resposta
    created_props = list(props_by_title.keys())
    # contabiliza reservas por propriedade (por título)
    counts: Dict[str, int] = {t: 0 for t in created_props}
    tit_by_id = {p.id: t for t, p in props_by_title.items()}
    for r in res_created:
        counts[tit_by_id[r.property_id]] += 1

    return {
        "message": "Seed aplicada com sucesso.",
        "created_properties": created_props,
        "reservations_distribution": counts,
        "reservations_total": len(res_created),
    }
