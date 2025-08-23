from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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