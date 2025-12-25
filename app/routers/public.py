from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.db.session import get_db
from app.db.models import LoadVoter, Neighborhood
from app.schemas import RegisterVoterIn, RegisterVoterOut
from app.core.captcha import verify_turnstile


import os
from fastapi import HTTPException

router = APIRouter(prefix="/public", tags=["public"])

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def get_client_ip(request: Request) -> str:
    """
    Obtiene IP real considerando proxies/CDN.
    """
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def validate_numeric(value: str, field: str):
    if not value.isdigit():
        raise HTTPException(
            status_code=422,
            detail=f"El campo '{field}' debe contener solo números"
        )


def verify_captcha(captcha_token: str):
    # ✅ bypass automático en pytest o cuando lo actives por env
    if os.getenv("PYTEST_CURRENT_TEST") is not None or os.getenv("TURNSTILE_TEST_BYPASS") == "1":
        return

    # ✅ en producción solo verificamos que exista (la validación real la hace Turnstile abajo)
    if not captcha_token:
        raise HTTPException(status_code=400, detail="Captcha inválido o faltante")

    """
    Placeholder de captcha.
    Aquí luego conectamos Turnstile o reCAPTCHA.
    """
    if not captcha_token or len(captcha_token) < 10:
        raise HTTPException(
            status_code=400,
            detail="Captcha inválido o faltante"
        )


# ---------------------------------------------------------
# Endpoint principal
# ---------------------------------------------------------

@router.post(
    "/voters/register",
    response_model=RegisterVoterOut,
    summary="Registro público de simpatizantes"
)
def register_voter(
    payload: RegisterVoterIn,
    request: Request,
    mode: str = Query(default="public", pattern="^(public|brigadista)$"),
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1) Validaciones de datos
    # -----------------------------------------------------

    validate_numeric(payload.document, "document")
    validate_numeric(payload.phone.replace("+", ""), "phone")

    if payload.consent is not True:
        raise HTTPException(
            status_code=422,
            detail="Debes aceptar el consentimiento para continuar"
        )

    verify_captcha(payload.captcha_token)

    # -----------------------------------------------------
    # 2) Validación relacional municipio -> barrio
    # -----------------------------------------------------

    neighborhood = (
        db.query(Neighborhood)
        .filter(Neighborhood.id == payload.neighborhood_id)
        .first()
    )

    if not neighborhood:
        raise HTTPException(status_code=422, detail="Barrio inválido")

    if neighborhood.id_municipality != payload.municipality_id:
        raise HTTPException(
            status_code=422,
            detail="El barrio no pertenece al municipio seleccionado"
        )

    # -----------------------------------------------------
    # 3) Detectar si el registro ya existe (EXACTO)
    # -----------------------------------------------------

    existing_voter = (
        db.query(LoadVoter.id)
        .filter(LoadVoter.document == payload.document)
        .first()
    )
    was_existing = existing_voter is not None

    # -----------------------------------------------------
    # 4) Evidencia de consentimiento
    # -----------------------------------------------------

    now = datetime.utcnow()
    client_ip = get_client_ip(request)
    verify_turnstile(token=payload.captcha_token, ip=client_ip)
    user_agent = request.headers.get("user-agent", "unknown")

    # -----------------------------------------------------
    # 5) UPSERT real (ON CONFLICT document)
    # -----------------------------------------------------

    stmt = insert(LoadVoter).values(
        cluster=1,
        id_coord=payload.coordinator_id,
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
            "id_coord": stmt.excluded.id_coord,
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
        raise HTTPException(
            status_code=500,
            detail="Error guardando el registro"
        ) from e

    # -----------------------------------------------------
    # 6) Respuesta contractual
    # -----------------------------------------------------

    if was_existing:
        return RegisterVoterOut(
            status="updated",
            message="Ya estabas registrado, actualizamos tu información."
        )

    return RegisterVoterOut(status="created")
