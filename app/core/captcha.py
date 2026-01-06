import os
from typing import Tuple

import requests

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verify_turnstile(token: str, remoteip: str | None = None, ip: str | None = None) -> Tuple[bool, str]:
    """
    Verifica Cloudflare Turnstile.
    - Devuelve (ok, msg)
    - NUNCA debe tumbar el endpoint con 500
    - Acepta `ip` como alias de `remoteip` para compatibilidad
    """
    secret = os.getenv("TURNSTILE_SECRET_KEY")
    if not secret:
        return False, "TURNSTILE_SECRET_KEY no configurada"

    if ip and not remoteip:
        remoteip = ip

    if not token or not isinstance(token, str):
        return False, "captcha_token vacío"

    data = {"secret": secret, "response": token}
    if remoteip:
        data["remoteip"] = remoteip

    try:
        r = requests.post(TURNSTILE_VERIFY_URL, data=data, timeout=8)
        r.raise_for_status()
        payload = r.json()
    except Exception as e:
        # Nunca dejes que esto cause 500
        return False, f"Error verificando captcha: {type(e).__name__}"

    if payload.get("success") is True:
        return True, "ok"

    codes = payload.get("error-codes") or []
    return False, f"Captcha inválido ({','.join(codes)})"
