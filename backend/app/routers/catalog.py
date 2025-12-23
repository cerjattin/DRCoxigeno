from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import distinct

from app.db.session import get_db
from app.db.models import Municipality, Neighborhood, Coordinator, Leader

router = APIRouter(prefix="/catalog", tags=["catalog"])

@router.get("/departments")
def get_departments(db: Session = Depends(get_db)):
    rows = db.query(distinct(Municipality.department)).order_by(Municipality.department).all()
    return [r[0] for r in rows]

@router.get("/municipalities")
def get_municipalities(department: str, db: Session = Depends(get_db)):
    rows = db.query(Municipality).filter(Municipality.department == department).order_by(Municipality.name).all()
    return [{"id": r.id, "name": r.name} for r in rows]

@router.get("/neighborhoods")
def get_neighborhoods(municipality_id: int, db: Session = Depends(get_db)):
    rows = db.query(Neighborhood).filter(Neighborhood.id_municipality == municipality_id).order_by(Neighborhood.name).all()
    return [{"id": r.id, "name": r.name} for r in rows]

@router.get("/coordinators")
def get_coordinators(search: str | None = Query(default=None), db: Session = Depends(get_db)):
    q = db.query(Coordinator)
    if search:
        q = q.filter(Coordinator.name.ilike(f"%{search}%"))
    rows = q.order_by(Coordinator.name).limit(50).all()
    return [{"id": r.id, "name": r.name} for r in rows]

@router.get("/leaders")
def get_leaders(search: str | None = Query(default=None), db: Session = Depends(get_db)):
    q = db.query(Leader)
    if search:
        q = q.filter(Leader.name.ilike(f"%{search}%"))
    rows = q.order_by(Leader.name).limit(50).all()
    return [{"id": r.id, "name": r.name} for r in rows]
