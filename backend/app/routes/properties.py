from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schema import PropertyCreate, PropertyOut
from app.crud.property import create_property, list_properties, delete_property_by_id
from app.session import get_db

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(payload: PropertyCreate, db: Session = Depends(get_db)):
    try:
        return create_property(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/list", response_model=list[PropertyOut])
def list_properties_all_endpoint(db: Session = Depends(get_db)):
    return list_properties(db)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_endpoint(property_id: int, db: Session = Depends(get_db)):
    try:
        ok = delete_property_by_id(db, property_id)
    except ValueError as e:
        # se seu CRUD levantar ValueError (ex.: FK impede deleção)
        raise HTTPException(status_code=409, detail=str(e))
    if not ok:
        raise HTTPException(status_code=404, detail="Property not found")
    return  # 204 No Content
