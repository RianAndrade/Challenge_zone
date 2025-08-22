from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schema import PropertyCreate, PropertyOut
from app.crud.property import create_property
from app.session import get_db

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(payload: PropertyCreate, db: Session = Depends(get_db)):
    try:
        return create_property(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
