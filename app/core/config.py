import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Neon connection string
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está definido en el entorno")

TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY")

# ID del coordinador "pre-cargado" para registros de líderes desde el panel.
# Esto permite que el frontend NO solicite ni exponga el coordinador.
COORDINATOR_DEFAULT_ID = int(os.getenv("COORDINATOR_DEFAULT_ID", "1"))

def should_bypass_captcha() -> bool:
    return os.getenv("PYTEST_CURRENT_TEST") is not None or os.getenv("TURNSTILE_TEST_BYPASS") == "1"

# En producción, exigir TURNSTILE_SECRET_KEY (si no hay bypass)
if not TURNSTILE_SECRET_KEY and not should_bypass_captcha():
    raise RuntimeError("TURNSTILE_SECRET_KEY no definido (y no hay bypass activo)")
