from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.schema import PropertyCreate, PropertyOut
from app.crud.property import create_property, list_properties, delete_property_by_id
from app.db.session import get_db

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(payload: PropertyCreate, db: Session = Depends(get_db)):
    try:
        return create_property(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))



@router.get("/list", response_model=List[PropertyOut])
def list_properties_endpoint(
    address_neighborhood: Optional[str] = Query(None, description="Filtro por Estado"),
    address_city: Optional[str] = Query(None, description="Filtro por cidade"),
    address_state: Optional[str] = Query(None, description="Filtro por estado"),
    capacity: Optional[int] = Query(None, ge=0, description="Capacidade maxima de pessoas"),
    price_per_night: Optional[int] = Query(None, ge=0, description="Valor maximo"),
    db: Session = Depends(get_db),
):
    return list_properties(
        db, 
        address_neighborhood=address_neighborhood, 
        address_city=address_city,
        address_state=address_state, 
        capacity=capacity,
        price_per_night=price_per_night
        )

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_endpoint(property_id: int, db: Session = Depends(get_db)):
    try:
        ok = delete_property_by_id(db, property_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    if not ok:
        raise HTTPException(status_code=404, detail="Property not found")
    return
