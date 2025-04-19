from fastapi import APIRouter

from app.api.endpoints import (charity_project_router, donation_router,
                               google_api_router, user_router)
from app.core.config import Constants

main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix=Constants.PROJECT_ENDPOINTS_PREFIX,
    tags=Constants.PROJECT_ENDPOINTS_TAGS
)

main_router.include_router(
    donation_router,
    prefix=Constants.DONATION_ENDPOINTS_PREFIX,
    tags=Constants.DONATION_ENDPOINTS_TAGS
)

main_router.include_router(user_router)

main_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)
