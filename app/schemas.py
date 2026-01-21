from pydantic import BaseModel, Field
from typing import Optional


class RegisterLeaderIn(BaseModel):
    """Registro de líderes desde el Panel de Líder.

    Nota: el coordinador NO se envía desde el frontend; queda fijado por
    configuración del backend (COORDINATOR_DEFAULT_ID).
    """

    name: str = Field(min_length=2, max_length=120)


class RegisterLeaderOut(BaseModel):
    status: str
    leaderCode: int
    coordinatorCode: int
    leaderName: str
    coordinatorName: str | None = None
    message: str | None = None

class RegisterVoterIn(BaseModel):
    # document es TEXT pero lo quieres numérico
    document: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=200)
    phone: str = Field(min_length=7, max_length=20)
    coordinator_id: Optional[int] = None
    municipality_id: int
    neighborhood_id: int

    # ✅ Solo leader
    leader_id: int

    consent: bool
    captcha_token: str


class RegisterVoterOut(BaseModel):
    status: str
    message: str | None = None

class LinkResolveOut(BaseModel):
    valid: bool
    leaderCode: int | None = None
    coordinatorCode: int | None = None
    leaderName: str | None = None
    coordinatorName: str | None = None
    message: str | None = None