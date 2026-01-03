from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.db.session import get_db
from app.db.models import LoadVoter, Neighborhood, Leader,Coordinator
from app.schemas import RegisterVoterIn, RegisterVoterOut, LinkResolveOut
from app.core.captcha import verify_turnstile

import os

router = APIRouter(prefix="/public", tags=["public"])


def get_client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def validate_numeric(value: str, field: str):
    if not value.isdigit():
        raise HTTPException(status_code=422, detail=f"El campo '{field}' debe contener solo números")


def should_bypass_captcha() -> bool:
    return os.getenv("PYTEST_CURRENT_TEST") is not None or os.getenv("TURNSTILE_TEST_BYPASS") == "1"

@router.get("/link/resolve", response_model=LinkResolveOut)
def resolve_link(
    leader: int = Query(..., description="ID del líder (leaderCode)"),
    coord: int = Query(..., description="ID del coordinador (coordinatorCode)"),
    db: Session = Depends(get_db),
):
    # 1) Validar que el líder exista
    leader_obj = db.query(Leader).filter(Leader.id == leader).first()
    if not leader_obj:
        return LinkResolveOut(valid=False, message="Líder no encontrado.")

    # 2) Validar que el coordinador exista
    coord_obj = db.query(Coordinator).filter(Coordinator.id == coord).first()
    if not coord_obj:
        return LinkResolveOut(valid=False, message="Coordinador no encontrado.")

    # 3) Validar relación líder -> coordinador
    if leader_obj.coordinator_id != coord_obj.id:
        return LinkResolveOut(
            valid=False,
            message="El líder no pertenece a este coordinador.",
        )

    # 4) OK: devolvemos info para UI
    return LinkResolveOut(
        valid=True,
        leaderCode=leader_obj.id,
        coordinatorCode=coord_obj.id,
        leaderName=leader_obj.name,
        coordinatorName=coord_obj.name,
    )

@router.post(
    "/voters/register",
    response_model=RegisterVoterOut,
    summary="Registro público de simpatizantes"
)
def register_voter(
    payload: RegisterVoterIn,
    request: Request,
    mode: str = Query(default="public", pattern="^(public|brigadista|leader_link)$"),
    db: Session = Depends(get_db),
):
    # 1) Validaciones básicas
    validate_numeric(payload.document, "document")
    validate_numeric(payload.phone.replace("+", "").replace(" ", ""), "phone")

    if payload.consent is not True:
        raise HTTPException(status_code=422, detail="Debes aceptar el consentimiento para continuar")

    # 2) Validar leader existe (y por extensión su coordinator)
    leader = db.query(Leader).filter(Leader.id == payload.leader_id).first()
    if not leader:
        raise HTTPException(status_code=422, detail="Líder inválido")
    
    if payload.coordinator_id is not None:
        coord = db.query(Coordinator).filter(Coordinator.id == payload.coordinator_id).first()
        if not coord:
            raise HTTPException(status_code=422, detail="Coordinador inválido")

        if leader.coordinator_id != coord.id:
            raise HTTPException(
                status_code=422,
                detail="El líder no pertenece al coordinador indicado",
            )

    # 3) Validación relacional municipio -> barrio
    neighborhood = db.query(Neighborhood).filter(Neighborhood.id == payload.neighborhood_id).first()
    if not neighborhood:
        raise HTTPException(status_code=422, detail="Barrio inválido")

    if neighborhood.id_municipality != payload.municipality_id:
        raise HTTPException(status_code=422, detail="El barrio no pertenece al municipio seleccionado")

    # 4) Duplicado (document) para mensaje
    existing_voter = db.query(LoadVoter.id).filter(LoadVoter.document == payload.document).first()
    was_existing = existing_voter is not None

    # 5) Captcha (bypass en tests / TURNSTILE_TEST_BYPASS=1)
    client_ip = get_client_ip(request)
    if not should_bypass_captcha():
        verify_turnstile(token=payload.captcha_token, ip=client_ip)

    now = datetime.utcnow()
    user_agent = request.headers.get("user-agent", "unknown")

    # 6) UPSERT (ON CONFLICT document)
    stmt = insert(LoadVoter).values(
        cluster=1,
        id_leader=payload.leader_id,
        document=payload.document,
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        address=payload.address.strip(),
        phone=payload.phone.strip(),
        id_municipality=payload.municipality_id,
        id_neighborhood=payload.neighborhood_id,
        mode=mode,
        consent=True,
        consent_at=now,
        consent_ip=client_ip,
        consent_user_agent=user_agent,
        created_at=now,
        updated_at=now,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=[LoadVoter.document],
        set_={
            "id_leader": stmt.excluded.id_leader,
            "first_name": stmt.excluded.first_name,
            "last_name": stmt.excluded.last_name,
            "address": stmt.excluded.address,
            "phone": stmt.excluded.phone,
            "id_municipality": stmt.excluded.id_municipality,
            "id_neighborhood": stmt.excluded.id_neighborhood,
            "mode": stmt.excluded.mode,
            "consent": stmt.excluded.consent,
            "consent_at": stmt.excluded.consent_at,
            "consent_ip": stmt.excluded.consent_ip,
            "consent_user_agent": stmt.excluded.consent_user_agent,
            "updated_at": now,
        },
    )

    try:
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error guardando el registro") from e

    if was_existing:
        return RegisterVoterOut(status="updated", message="Ya estabas registrado, actualizamos tu información.")

    return RegisterVoterOut(status="created")
