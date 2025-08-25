from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.db.schema import ReservationCreate, ReservationOut, ReservationCreateResponse
from app.crud.reservation import (
    create_reservation,
    list_reservations,
    deactivate_reservation,
)
from app.crud.property import check_availability

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("", response_model=List[ReservationOut])
def list_reservations_endpoint(
    db: Session = Depends(get_db),
    client_email: str = Query(None, description="Email do cliente"),
    property_id: int = Query(None, description="Id da propiedade"),
):
    return list_reservations(db, client_email, property_id)


@router.post(
    "", response_model=ReservationCreateResponse, status_code=status.HTTP_201_CREATED
)
def create_reservation_endpoint(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
):
    check_availability(
        db,
        property_id=payload.property_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        guests_quantity=payload.guests_quantity,
    )

    try:
        return create_reservation(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{reservation_id}/cancel", response_model=ReservationOut)
def deactivate_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    res = deactivate_reservation(db, reservation_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return res
