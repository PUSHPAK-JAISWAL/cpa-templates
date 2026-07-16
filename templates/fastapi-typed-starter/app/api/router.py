"""Application API router.

Feature routers are mounted here so `app/main.py` stays focused on app setup.
"""

from fastapi import APIRouter

from app.features.health.router import router as health_router

router = APIRouter()
router.include_router(health_router)
