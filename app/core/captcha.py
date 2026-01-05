import requests
from typing import Tuple

from app.core.config import TURNSTILE_SECRET_KEY

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

def verify_turnstile(token: str, remoteip: str | None = None) -> Tuple[bool, str]:
    if not TURNSTILE_SECRET_KEY:
        return False, "TURNSTILE_SECRET_KEY no configurada"

    if not token or not isinstance(token, str):
        return False, "captcha_token vacío"

    data = {"secret": TURNSTILE_SECRET_KEY, "response": token}
    if remoteip:
        data["remoteip"] = remoteip

    try:
        r = requests.post(TURNSTILE_VERIFY_URL, data=data, timeout=8)
        r.raise_for_status()
        payload = r.json()
    except Exception as e:
        # Evita 500 por fallos de red/timeout/DNS/etc.
        return False, f"Error verificando captcha: {type(e).__name__}"

    if payload.get("success") is True:
        return True, "ok"

    codes = payload.get("error-codes") or []
    return False, f"Captcha inválido ({','.join(codes)})"
