from fastapi import APIRouter

from service.api.endpoints.auth import router as auth_endpoint
from service.api.endpoints.predictions import router as predictions_endpoint
from service.api.endpoints.dev import router as dev_endpoint


routers = [auth_endpoint, predictions_endpoint, dev_endpoint]

api_router = APIRouter(prefix="/api")

for router in routers:
    api_router.include_router(router)
