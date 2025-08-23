from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.db.schema import ReservationCreate, ReservationOut
from app.crud.reservation import create_reservation, list_reservations

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("", response_model=List[ReservationOut])
def list_reservations_endpoint(
    db: Session = Depends(get_db),
):
    return list_reservations(
        db, 
        )


@router.post("", response_model=ReservationOut, status_code=status.HTTP_201_CREATED,)
def create_reservation_endpoint(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_reservation(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


