import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.public import router as public_router
from app.routers.catalog import router as catalog_router

app = FastAPI(title="Voter Registration API", version="1.0.0")

# CORS (define CORS_ORIGINS en Render)
origins = os.getenv("CORS_ORIGINS", "*")
ALLOWED_ORIGINS = [
    "https://frontend-registro-drc.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,  # pon True solo si usas cookies/sesión
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router)
app.include_router(catalog_router)

@app.get("/health")
def health():
    return {"ok": True}
