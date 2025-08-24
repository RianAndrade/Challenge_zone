from fastapi import HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, func, select
from datetime import date
from app.db.models import Property, Reservation
from app.db.schema import PropertyCreate


def list_properties(
    db: Session,
    location: Optional[str] = None,
    capacity: Optional[int] = None,
    address_neighborhood: Optional[str] = None,
    address_city: Optional[str] = None,
    address_state: Optional[str] = None,
    price_per_night: Optional[int] = None,
) -> List[Property]:

    q = db.query(Property)

    if address_state:
        q = q.filter(Property.address_state == address_state.strip())

    if address_neighborhood:
        q = q.filter(Property.address_neighborhood == address_neighborhood.strip())

    if address_city:
        q = q.filter(Property.address_city == address_city.strip())

    # esta maior ou igual para facilitar debug mudar para enviar

    if capacity:
        q = q.filter(Property.capacity >= capacity)

    if price_per_night:
        q = q.filter(Property.price_per_night <= price_per_night)

    return q.order_by(asc(Property.id)).all()


def find_conflicts(
    db: Session,
    property_id: int,
    start_date: date,
    end_date: date,
) -> List[int]:

    stmt = select(Reservation.id).where(
        Reservation.property_id == property_id,
        Reservation.start_date <= end_date,
        Reservation.end_date >= start_date,
    )
    return [row[0] for row in db.execute(stmt).all()]


def check_availability(
    db: Session,
    property_id: int,
    start_date: date,
    end_date: date,
    guests_quantity: int,
) -> List[Property]:

    prop = db.get(Property, property_id)

    if start_date == end_date:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A data de saída deve ser posterior à data de início (não podem ser iguais).",
        )

    if prop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propriedade não encontrada",
        )

    if guests_quantity > prop.capacity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Capacidade insuficiente para a quantidade de hóspedes solicitada",
        )

    if find_conflicts(db, property_id, start_date, end_date):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Período indisponível para esta propriedade",
        )

    return [prop]


def create_property(db: Session, data: PropertyCreate) -> Property:
    obj = Property(**data.model_dump())
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Já existe uma propriedade cadastrada nesse endereço.") from e
    db.refresh(obj)
    return obj


def delete_property_by_id(db: Session, prop_id: int) -> bool:
    obj = db.get(Property, prop_id)
    if not obj:
        return False
    db.delete(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("debub par FK delete") from e
    return True
