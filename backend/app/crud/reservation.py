from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, func
from app.db.models import Reservation
from app.db.schema import ReservationCreate


def create_reservation(db: Session, data: ReservationCreate) -> Reservation:
    obj = Reservation(**data.model_dump())
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Não foi possível criar a reserva. Verifique os dados.") from e
    db.refresh(obj)
    return obj

def list_reservations(
    db: Session, 
) -> List[Reservation]:

    q = db.query(Reservation)
    
    return q.order_by(asc(Reservation.id)).all()
