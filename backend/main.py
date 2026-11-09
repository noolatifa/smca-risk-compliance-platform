from fastapi import FastAPI

from backend.core.config import settings
from backend.referentiel.router import router as referentiel_router
from backend.bia.router import router as bia_router
from backend.risques.router import router as risques_router

app = FastAPI(title=settings.app_name)

app.include_router(referentiel_router, prefix=settings.api_prefix)
app.include_router(bia_router, prefix=settings.api_prefix)
app.include_router(risques_router, prefix=settings.api_prefix)

@app.get("/health")
def health():
    return {"status": "healthy"}
