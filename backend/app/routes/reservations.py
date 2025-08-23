from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.schema import ReservationCreate, ReservationOut
from app.crud.reservation import create_reservation

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("", response_model=ReservationOut, status_code=status.HTTP_201_CREATED,)

def create_reservation_endpoint(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_reservation(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
