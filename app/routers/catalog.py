from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Department, Municipality, Neighborhood, Coordinator, Leader

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/departments")
def get_departments(db: Session = Depends(get_db)):
    rows = db.query(Department).order_by(Department.name).all()
    return [{"id": r.id, "name": r.name} for r in rows]


@router.get("/municipalities")
def get_municipalities(
    department_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    q = db.query(Municipality)
    if department_id is not None:
        q = q.filter(Municipality.department_id == department_id)

    rows = q.order_by(Municipality.name).all()
    return [{"id": r.id, "name": r.name} for r in rows]


@router.get("/neighborhoods")
def get_neighborhoods(municipality_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(Neighborhood)
        .filter(Neighborhood.id_municipality == municipality_id)
        .order_by(Neighborhood.name)
        .all()
    )
    return [{"id": r.id, "name": r.name} for r in rows]


@router.get("/coordinators")
def get_coordinators(search: str | None = Query(default=None), db: Session = Depends(get_db)):
    q = db.query(Coordinator)
    if search:
        q = q.filter(Coordinator.name.ilike(f"%{search}%"))
    rows = q.order_by(Coordinator.name).limit(50).all()
    return [{"id": r.id, "name": r.name} for r in rows]


@router.get("/leaders")
def get_leaders(
    search: str | None = Query(default=None),
    coordinator_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    q = db.query(Leader)

    # ✅ cascada opcional (recomendado)
    if coordinator_id is not None:
        q = q.filter(Leader.coordinator_id == coordinator_id)

    if search:
        q = q.filter(Leader.name.ilike(f"%{search}%"))

    rows = q.order_by(Leader.name).limit(50).all()
    return [{"id": r.id, "name": r.name, "coordinator_id": r.coordinator_id} for r in rows]
