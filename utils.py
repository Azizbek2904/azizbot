"""
Yordamchi funksiyalar:
- Kanallarga obuna tekshiruvi
- Referral linklar yaratish
- Admin tekshiruvi
"""
import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from config import config
from database import get_mandatory_channels, Channel

logger = logging.getLogger(__name__)


def is_admin(telegram_id: int) -> bool:
    """User adminmi tekshirish"""
    return telegram_id in config.ADMIN_IDS


async def check_user_subscription(bot: Bot, telegram_id: int) -> tuple[bool, list[Channel]]:
    """
    Foydalanuvchining barcha majburiy kanallarga obuna bo'lganini tekshirish.
    Qaytaradi: (hammasiga obunami, obuna bo'lmagan kanallar ro'yxati)
    """
    channels = await get_mandatory_channels()
    if not channels:
        return True, []

    not_subscribed = []
    for channel in channels:
        try:
            member = await bot.get_chat_member(
                chat_id=channel.channel_id, user_id=telegram_id
            )
            if member.status in ("left", "kicked"):
                not_subscribed.append(channel)
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            logger.warning(f"Kanal {channel.channel_id} tekshirilmadi: {e}")
            # Agar bot kanaldan chiqarib yuborilgan yoki kanal o'chirilgan bo'lsa
            not_subscribed.append(channel)
        except Exception as e:
            logger.error(f"Kutilmagan xato: {e}")
            not_subscribed.append(channel)

    return len(not_subscribed) == 0, not_subscribed


async def get_bot_username(bot: Bot) -> str:
    """Bot username olish (cache qilinadi)"""
    if not hasattr(get_bot_username, "_cache"):
        me = await bot.get_me()
        get_bot_username._cache = me.username
    return get_bot_username._cache


async def generate_referral_link(bot: Bot, user_telegram_id: int) -> str:
    """Foydalanuvchi uchun referral link yaratish"""
    username = await get_bot_username(bot)
    return f"https://t.me/{username}?start=ref_{user_telegram_id}"


def parse_referral_code(args: str) -> int | None:
    """
    /start komandasidan referral kodni ajratib olish.
    'ref_12345' → 12345
    """
    if not args:
        return None
    args = args.strip()
    if args.startswith("ref_"):
        try:
            return int(args[4:])
        except ValueError:
            return None
    return None


def format_link_url(link_type: str, url: str) -> str:
    """Link turiga qarab URL formatlash"""
    url = url.strip()
    if link_type == "mobile":
        # Mobile deep linklar uchun
        return url
    elif link_type == "telegram":
        # Telegram linklar
        if not url.startswith("http"):
            if url.startswith("@"):
                url = f"https://t.me/{url[1:]}"
            elif not url.startswith("t.me"):
                url = f"https://t.me/{url}"
            else:
                url = f"https://{url}"
        return url
    else:  # web
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        return url


def format_datetime(dt) -> str:
    """Sanani chiroyli formatlash"""
    if not dt:
        return "—"
    return dt.strftime("%d.%m.%Y")
