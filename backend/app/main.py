import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.public import router as public_router
from app.routers.catalog import router as catalog_router

app = FastAPI(title="Voter Registration API", version="1.0.0")

# CORS (define CORS_ORIGINS en Render)
origins = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [o.strip() for o in origins.split(",")] if origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router)
app.include_router(catalog_router)

@app.get("/health")
def health():
    return {"ok": True}
