"""
Bot konfiguratsiyasi.
.env faylidan barcha sozlamalarni o'qiydi.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    DATABASE_URL: str


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
        raise ValueError(
            "❌ BOT_TOKEN topilmadi! .env faylida BOT_TOKEN ni to'g'ri kiriting."
        )

    admin_ids_str = os.getenv("ADMIN_IDS", "").strip()
    if not admin_ids_str or admin_ids_str == "YOUR_ADMIN_TELEGRAM_ID_HERE":
        raise ValueError(
            "❌ ADMIN_IDS topilmadi! .env faylida ADMIN_IDS ni to'g'ri kiriting."
        )

    try:
        admin_ids = [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
    except ValueError:
        raise ValueError("❌ ADMIN_IDS noto'g'ri formatda! Faqat raqamlar va vergul.")

    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot_database.db")

    return Config(
        BOT_TOKEN=bot_token,
        ADMIN_IDS=admin_ids,
        DATABASE_URL=database_url,
    )


config = load_config()
