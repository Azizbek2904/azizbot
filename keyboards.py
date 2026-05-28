"""
Barcha klaviaturalar (Reply va Inline).
"""
from urllib.parse import quote
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from locales import t
from database import Channel


# ──────────────── TIL TANLASH ────────────────

def language_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang:uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang:ru")
    builder.adjust(2)
    return builder.as_markup()


# ──────────────── MAJBURIY OBUNA ────────────────

def subscription_kb(channels: list[Channel], lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ch in channels:
        builder.button(text=f"📢 {ch.title}", url=ch.invite_link)
    builder.button(text=t("check_subscription", lang), callback_data="check_subscription")
    builder.adjust(1)
    return builder.as_markup()


# ──────────────── ASOSIY MENYU ────────────────

def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("btn_ads", lang))
    builder.button(text=t("btn_contests", lang))
    builder.button(text=t("btn_my_link", lang))
    builder.button(text=t("btn_my_friends", lang))
    builder.button(text=t("btn_top", lang))
    builder.button(text=t("btn_info", lang))
    builder.button(text=t("btn_settings", lang))
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


# ──────────────── AKSIYA POSTI ────────────────

def ad_post_kb(button_text: str, url: str, share_link: str, share_text: str, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=button_text, url=url)
    # Share URL
    share_url = f"https://t.me/share/url?url={quote(share_link)}&text={quote(share_text)}"
    builder.button(text=t("btn_share", lang), url=share_url)
    builder.adjust(2)
    return builder.as_markup()


# ──────────────── KONKURS POSTI ────────────────

def contest_post_kb(contest_id: int, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t("btn_participate", lang), callback_data=f"contest_join:{contest_id}"
    )
    builder.button(text="🏆 TOP", callback_data=f"contest_top:{contest_id}")
    builder.adjust(1, 1)
    return builder.as_markup()


# ──────────────── MENING HAVOLAM ────────────────

def my_link_kb(ref_link: str, share_text: str, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    share_url = f"https://t.me/share/url?url={quote(ref_link)}&text={quote(share_text)}"
    builder.button(text=t("btn_share_link", lang), url=share_url)
    builder.adjust(1)
    return builder.as_markup()


# ──────────────── TOP REYTING ────────────────

def top_contests_kb(contests, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for c in contests:
        builder.button(text=f"🏆 {c.title[:30]}", callback_data=f"top_contest:{c.id}")
    builder.adjust(1)
    return builder.as_markup()


# ──────────────── SOZLAMALAR ────────────────

def settings_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_change_lang", lang), callback_data="settings:lang")
    builder.button(text=t("btn_notifications", lang), callback_data="settings:notif")
    builder.button(text=t("btn_help", lang), callback_data="settings:help")
    builder.adjust(1)
    return builder.as_markup()


# ════════════════════════════════════════════════════════
#                    ADMIN KEYBOARDS
# ════════════════════════════════════════════════════════

def admin_main_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("admin_btn_ads", lang))
    builder.button(text=t("admin_btn_contests", lang))
    builder.button(text=t("admin_btn_channels", lang))
    builder.button(text=t("admin_btn_stats", lang))
    builder.button(text=t("admin_btn_broadcast", lang))
    builder.button(text=t("admin_btn_users", lang))
    builder.button(text="🏠 " + t("main_menu", lang))
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def admin_cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("cancel", lang))
    return builder.as_markup(resize_keyboard=True)


def admin_skip_cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("skip", lang))
    builder.button(text=t("cancel", lang))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def confirm_inline_kb(action: str, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("confirm", lang), callback_data=f"{action}:yes")
    builder.button(text=t("cancel", lang), callback_data=f"{action}:no")
    builder.adjust(2)
    return builder.as_markup()


def yes_no_inline_kb(action: str, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("yes", lang), callback_data=f"{action}:yes")
    builder.button(text=t("no", lang), callback_data=f"{action}:no")
    builder.adjust(2)
    return builder.as_markup()


# ─── Reklamalar ───

def admin_ads_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("admin_btn_new_ad", lang))
    builder.button(text=t("admin_btn_ads_list", lang))
    builder.button(text=t("admin_back", lang))
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def ad_link_type_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("ad_link_web", lang), callback_data="adlink:web")
    builder.button(text=t("ad_link_telegram", lang), callback_data="adlink:telegram")
    builder.button(text=t("ad_link_mobile", lang), callback_data="adlink:mobile")
    builder.adjust(1)
    return builder.as_markup()


def admin_ad_card_kb(ad_id: int, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("ad_btn_send_channel", lang), callback_data=f"adsend:{ad_id}")
    builder.button(text=t("ad_btn_delete", lang), callback_data=f"addel:{ad_id}")
    builder.adjust(1)
    return builder.as_markup()


def admin_channels_select_kb(channels: list[Channel], prefix: str, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ch in channels:
        builder.button(text=f"📡 {ch.title[:30]}", callback_data=f"{prefix}:{ch.id}")
    builder.button(text=t("cancel", lang), callback_data=f"{prefix}:cancel")
    builder.adjust(1)
    return builder.as_markup()


# ─── Konkurslar ───

def admin_contests_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("admin_btn_new_contest", lang))
    builder.button(text=t("admin_btn_contests_list", lang))
    builder.button(text=t("admin_back", lang))
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def contest_type_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("contest_type_top3", lang), callback_data="ctype:top3")
    builder.button(text=t("contest_type_first_n", lang), callback_data="ctype:first_n")
    builder.adjust(1)
    return builder.as_markup()


def admin_contest_card_kb(contest_id: int, status: str, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if status == "active":
        builder.button(
            text=t("contest_btn_winners", lang), callback_data=f"cwinners:{contest_id}"
        )
        builder.button(text=t("contest_btn_end", lang), callback_data=f"cend:{contest_id}")
    builder.button(text="📊 TOP", callback_data=f"top_contest:{contest_id}")
    builder.adjust(1)
    return builder.as_markup()


# ─── Kanallar ───

def admin_channels_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("admin_btn_add_channel", lang))
    builder.button(text=t("admin_btn_channels_list", lang))
    builder.button(text=t("admin_back", lang))
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def admin_channel_card_kb(channel_id: int, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t("channel_btn_toggle_mandatory", lang),
        callback_data=f"chtoggle:{channel_id}",
    )
    builder.button(
        text=t("channel_btn_remove", lang), callback_data=f"chremove:{channel_id}"
    )
    builder.adjust(1)
    return builder.as_markup()


# ─── User boshqaruvi ───

def admin_user_actions_kb(telegram_id: int, is_blocked: bool, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_blocked:
        builder.button(
            text=t("user_btn_unblock", lang), callback_data=f"uunblock:{telegram_id}"
        )
    else:
        builder.button(
            text=t("user_btn_block", lang), callback_data=f"ublock:{telegram_id}"
        )
    return builder.as_markup()
