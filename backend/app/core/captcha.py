import requests
from fastapi import HTTPException
from app.core.config import TURNSTILE_SECRET_KEY

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

def verify_turnstile(token: str, ip: str):
    """
    Verifica captcha Cloudflare Turnstile
    """
    if not token:
        raise HTTPException(status_code=400, detail="Captcha faltante")

    data = {
        "secret": TURNSTILE_SECRET_KEY,
        "response": token,
        "remoteip": ip,
    }

    try:
        response = requests.post(TURNSTILE_VERIFY_URL, data=data, timeout=5)
        result = response.json()
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Error validando captcha"
        )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail="Captcha inválido"
        )
