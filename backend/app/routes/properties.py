from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session
from app.db.schema import PropertyCreate, PropertyOut,PropertyMessageResponse
from app.service.property import (
    create_property,
    list_properties,
    delete_property_by_id,
    check_availability,
)
from app.db.session import get_db

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/list", response_model=List[PropertyOut])
def list_properties_endpoint(
    address_neighborhood: Optional[str] = Query(None, description="Filtro por Bairro"),
    address_city: Optional[str] = Query(None, description="Filtro por cidade"),
    address_state: Optional[str] = Query(None, description="Filtro por estado"),
    capacity: Optional[int] = Query(
        None, ge=0, description="Capacidade maxima de pessoas"
    ),
    price_per_night: Optional[int] = Query(None, ge=0, description="Valor maximo"),
    db: Session = Depends(get_db),
):
    return list_properties(
        db,
        address_neighborhood=address_neighborhood,
        address_city=address_city,
        address_state=address_state,
        capacity=capacity,
        price_per_night=price_per_night,
    )


@router.get("/availability", response_model=PropertyMessageResponse)
def check_availability_endpoint(
    property_id: int = Query(None, description="Id da propriedade"),
    start_date: date = Query(
        None, description="Data de início da reserva (YYYY-MM-DD)"
    ),
    end_date: date = Query(None, description="Data final da reserva (YYYY-MM-DD)"),
    guests_quantity: int = Query(
        None, description="Quantidade de pessoas para a reserva"
    ),
    db: Session = Depends(get_db),
):
    if not all([property_id, start_date, end_date, guests_quantity]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todos os dados devem estar preenchidos",
        )
        
    check_availability(db, property_id, start_date, end_date, guests_quantity)
    
    return {"message": "A propriedade encontra-se disponível para as datas verificadas."}



@router.post("", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(payload: PropertyCreate, db: Session = Depends(get_db)):
    try:
        return create_property(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_endpoint(property_id: int, db: Session = Depends(get_db)):
    try:
        ok = delete_property_by_id(db, property_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    if not ok:
        raise HTTPException(status_code=404, detail="Property not found")
    return
