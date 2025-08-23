from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, func, select
from app.db.models import Reservation, Property
from app.db.schema import ReservationCreate
from datetime import date

def _get_property_price(db: Session, property_id: int) -> int:
    stmt = select(Property.price_per_night).where(Property.id == property_id)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        raise ValueError("Price Property: Propriedade não encontrada")
    return int(result)

def calculate_days_reserved(start_date: date, end_date: date) -> int:

    if end_date <= start_date:
        raise ValueError("A data final deve ser maior que a data inicial")
    delta = end_date - start_date
    return delta.days




def create_reservation(db: Session, data: ReservationCreate) -> Reservation:
    obj = Reservation(**data.model_dump())
    db.add(obj)
    price = _get_property_price(db, data.property_id)
    days = calculate_days_reserved( data.start_date, data.end_date)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Não foi possível criar a reserva. Verifique os dados fornecidos.") from e
    db.refresh(obj)


    total = days * price
    message = f"Reserva Feita com Sucesso, o valor total será R${total:.2f}"
    return {
        "message": message,
        "reservation": obj,
    }


def list_reservations(
    db: Session, 
) -> List[Reservation]:

    q = db.query(Reservation)
    
    return q.order_by(asc(Reservation.id)).all()
