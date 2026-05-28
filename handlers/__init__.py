"""Handlers package"""
from aiogram import Router

from .user import user_router
from .admin import admin_router


def setup_routers() -> Router:
    """Barcha routerlarni birlashtirish"""
    main_router = Router()
    # Admin router birinchi (admin filterlari ko'pchilik user filterlardan oldin)
    main_router.include_router(admin_router)
    main_router.include_router(user_router)
    return main_router
