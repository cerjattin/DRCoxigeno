import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.public import router as public_router
from app.routers.catalog import router as catalog_router

import logging
from fastapi.responses import JSONResponse
from starlette.requests import Request


app = FastAPI(title="Voter Registration API", version="1.0.0")

logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# 🔐 CORS
ALLOWED_ORIGINS = [
    "https://frontend-registro-drc.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router)
app.include_router(catalog_router)

@app.get("/health")
def health():
    return {"ok": True}
