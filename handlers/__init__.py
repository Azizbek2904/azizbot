from aiogram import Router

from .admin import router as admin_router
from .user import router as user_router

main_router = Router()

def setup_routers() -> Router:
    router = Router()

    router.include_router(admin_router)
    router.include_router(user_router)

    return router
