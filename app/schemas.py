from pydantic import BaseModel, Field


class RegisterVoterIn(BaseModel):
    # document es TEXT pero lo quieres numérico
    document: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=200)
    phone: str = Field(min_length=7, max_length=20)

    municipality_id: int
    neighborhood_id: int

    # ✅ Solo leader
    leader_id: int

    consent: bool
    captcha_token: str


class RegisterVoterOut(BaseModel):
    status: str
    message: str | None = None
