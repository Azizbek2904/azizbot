"""
Foydalanuvchi tomonidagi handlerlar.
"""
import json
import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import (
    Message,
    CallbackQuery,
    InputMediaPhoto,
    FSInputFile,
)
from aiogram.exceptions import TelegramBadRequest

from config import config
from database import (
    get_or_create_user,
    get_user_by_telegram_id,
    update_user_language,
    toggle_notifications,
    get_active_ads,
    get_active_contests,
    get_contest_by_id,
    join_contest,
    get_participation,
    get_user_referral_count,
    get_user_referrals,
    get_contest_top,
    get_user_place_in_contest,
    create_referral,
    verify_referral,
    async_session,
    User,
)
from locales import t, TRANSLATIONS
from keyboards import (
    language_kb,
    subscription_kb,
    main_menu_kb,
    ad_post_kb,
    contest_post_kb,
    my_link_kb,
    top_contests_kb,
    settings_kb,
)
from utils import (
    check_user_subscription,
    generate_referral_link,
    parse_referral_code,
    format_link_url,
    format_datetime,
    is_admin,
)

logger = logging.getLogger(__name__)
user_router = Router()


# ════════════════════════════════════════════════════════
#                    /START
# ════════════════════════════════════════════════════════

@user_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    tg_user = message.from_user
    referrer_tg_id = parse_referral_code(command.args) if command.args else None

    user, is_new = await get_or_create_user(
        telegram_id=tg_user.id,
        username=tg_user.username,
        full_name=tg_user.full_name,
        referrer_telegram_id=referrer_tg_id,
    )

    # Agar yangi user va referrer bor bo'lsa — referral yaratish
    if is_new and user.referrer_id:
        await create_referral(
            referrer_id=user.referrer_id,
            referred_id=user.id,
            contest_id=None,  # umumiy referral, konkurs bilan bog'lanmagan
        )

    # Yangi user uchun avval til tanlash
    if is_new:
        await message.answer(
            t("choose_language", "uz"),
            reply_markup=language_kb(),
        )
        return

    # Aks holda majburiy obunani tekshirish va menyuga o'tkazish
    await proceed_to_main_menu(message, bot, user)


@user_router.callback_query(F.data.startswith("lang:"))
async def on_language_selected(call: CallbackQuery, bot: Bot):
    lang = call.data.split(":")[1]
    if lang not in ("uz", "ru"):
        return

    await update_user_language(call.from_user.id, lang)
    await call.answer(t("language_set", lang))

    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass

    user = await get_user_by_telegram_id(call.from_user.id)
    await proceed_to_main_menu(call.message, bot, user, is_callback=True)


async def proceed_to_main_menu(
    message: Message, bot: Bot, user: User, is_callback: bool = False
):
    """Obuna tekshiruvi va menyuga o'tish"""
    lang = user.language

    # Obunani tekshirish
    is_subscribed, not_subscribed = await check_user_subscription(bot, user.telegram_id)

    if not is_subscribed:
        await message.answer(
            t("subscription_required", lang),
            reply_markup=subscription_kb(not_subscribed, lang),
        )
        return

    # Referral tasdiqlash (agar pending bo'lsa)
    if user.referrer_id:
        ref = await verify_referral(user.id)
        if ref:
            # Referrerga xabar yuborish
            await notify_referrer(bot, ref.referrer_id)

    # Welcome xabar
    welcome_text = t("welcome", lang, name=user.full_name)
    await message.answer(welcome_text, reply_markup=main_menu_kb(lang))


async def notify_referrer(bot: Bot, referrer_user_id: int):
    """Referrerga yangi referral kelganligi haqida xabar"""
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == referrer_user_id))
        referrer = result.scalar_one_or_none()
        if not referrer or not referrer.notifications_enabled:
            return

        ref_count = await get_user_referral_count(referrer.id)
        try:
            await bot.send_message(
                referrer.telegram_id,
                t(
                    "new_referral_notification",
                    referrer.language,
                    name="🎉",
                    count=ref_count,
                ),
            )
        except Exception as e:
            logger.warning(f"Referrerga xabar yuborilmadi: {e}")


# ════════════════════════════════════════════════════════
#                MAJBURIY OBUNA TEKSHIRUV
# ════════════════════════════════════════════════════════

@user_router.callback_query(F.data == "check_subscription")
async def on_check_subscription(call: CallbackQuery, bot: Bot):
    user = await get_user_by_telegram_id(call.from_user.id)
    if not user:
        await call.answer("❌", show_alert=True)
        return

    lang = user.language
    is_subscribed, not_subscribed = await check_user_subscription(bot, user.telegram_id)

    if not is_subscribed:
        await call.answer(t("subscription_failed", lang), show_alert=True)
        return

    # Referral tasdiqlash
    if user.referrer_id:
        ref = await verify_referral(user.id)
        if ref:
            await notify_referrer(bot, ref.referrer_id)

    await call.answer(t("subscription_success", lang))
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass

    await call.message.answer(
        t("welcome", lang, name=user.full_name),
        reply_markup=main_menu_kb(lang),
    )


# ════════════════════════════════════════════════════════
#                FILTER YORDAMCHI — KO'P TILDA MATN
# ════════════════════════════════════════════════════════

def text_matches(key: str):
    """Reply tugma matnini ikkala tilda tekshirish uchun filter"""
    texts = [TRANSLATIONS[key]["uz"], TRANSLATIONS[key]["ru"]]
    return F.text.in_(texts)


# ════════════════════════════════════════════════════════
#                AKSIYALAR (USER)
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_ads"))
async def on_ads(message: Message, bot: Bot):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language

    # Obunani tekshirish
    is_subscribed, not_subscribed = await check_user_subscription(bot, user.telegram_id)
    if not is_subscribed:
        await message.answer(
            t("subscription_required", lang),
            reply_markup=subscription_kb(not_subscribed, lang),
        )
        return

    ads = await get_active_ads()
    if not ads:
        await message.answer(t("no_ads", lang))
        return

    await message.answer(t("ads_title", lang))

    ref_link = await generate_referral_link(bot, user.telegram_id)
    share_text = t("share_text", lang)

    for ad in ads:
        caption = f"<b>{ad.title}</b>\n\n{ad.description}"
        if ad.promo_text:
            caption += f"\n\n🔥 <i>{ad.promo_text}</i>"

        url = format_link_url(ad.link_type, ad.link_url)
        kb = ad_post_kb(ad.button_text, url, ref_link, share_text, lang)

        try:
            if ad.photo_file_id:
                await message.answer_photo(
                    photo=ad.photo_file_id, caption=caption, reply_markup=kb
                )
            else:
                await message.answer(caption, reply_markup=kb)
        except Exception as e:
            logger.error(f"Reklama yuborilmadi: {e}")


# ════════════════════════════════════════════════════════
#                KONKURSLAR (USER)
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_contests"))
async def on_contests(message: Message, bot: Bot):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language

    is_subscribed, not_subscribed = await check_user_subscription(bot, user.telegram_id)
    if not is_subscribed:
        await message.answer(
            t("subscription_required", lang),
            reply_markup=subscription_kb(not_subscribed, lang),
        )
        return

    contests = await get_active_contests()
    if not contests:
        await message.answer(t("no_contests", lang))
        return

    await message.answer(t("contests_title", lang))

    for contest in contests:
        caption = await format_contest_card(contest, lang)
        kb = contest_post_kb(contest.id, lang)
        try:
            if contest.photo_file_id:
                await message.answer_photo(
                    photo=contest.photo_file_id, caption=caption, reply_markup=kb
                )
            else:
                await message.answer(caption, reply_markup=kb)
        except Exception as e:
            logger.error(f"Konkurs yuborilmadi: {e}")


async def format_contest_card(contest, lang: str) -> str:
    """Konkurs kartochkasi matni"""
    try:
        prizes = json.loads(contest.prizes)
    except Exception:
        prizes = []

    prizes_text = "\n".join(prizes) if prizes else "—"

    # Ishtirokchilar soni
    from sqlalchemy import select, func
    from database import ContestParticipant

    async with async_session() as session:
        count = await session.scalar(
            select(func.count(ContestParticipant.id)).where(
                ContestParticipant.contest_id == contest.id
            )
        )

    text = (
        f"🏆 <b>{contest.title}</b>\n\n"
        f"{contest.description}\n\n"
        f"{t('contest_prizes', lang)}\n{prizes_text}\n\n"
        f"{t('contest_ends', lang)} <b>{format_datetime(contest.end_date)}</b>\n"
        f"{t('contest_participants', lang)} <b>{count or 0}</b>"
    )
    return text


@user_router.callback_query(F.data.startswith("contest_join:"))
async def on_contest_join(call: CallbackQuery, bot: Bot):
    contest_id = int(call.data.split(":")[1])
    user = await get_user_by_telegram_id(call.from_user.id)
    if not user:
        await call.answer("❌", show_alert=True)
        return
    lang = user.language

    # Obunani tekshirish
    is_subscribed, not_subscribed = await check_user_subscription(bot, user.telegram_id)
    if not is_subscribed:
        await call.message.answer(
            t("subscription_required", lang),
            reply_markup=subscription_kb(not_subscribed, lang),
        )
        await call.answer()
        return

    contest = await get_contest_by_id(contest_id)
    if not contest or contest.status != "active":
        await call.answer(t("error", lang), show_alert=True)
        return

    # Allaqachon ishtirok etganmi?
    existing = await get_participation(user.id, contest_id)
    if existing:
        await call.answer(
            t("already_in_contest", lang, count=existing.ref_count),
            show_alert=True,
        )
        return

    # Qo'shish
    await join_contest(user.id, contest_id)

    # Shaxsiy referral link
    ref_link = await generate_referral_link(bot, user.telegram_id)
    await call.message.answer(
        t("joined_contest", lang, link=ref_link),
    )
    await call.answer("✅")


@user_router.callback_query(F.data.startswith("contest_top:"))
async def on_contest_top(call: CallbackQuery):
    contest_id = int(call.data.split(":")[1])
    user = await get_user_by_telegram_id(call.from_user.id)
    if not user:
        return
    lang = user.language

    contest = await get_contest_by_id(contest_id)
    if not contest:
        return

    await send_contest_top(call.message, contest, lang)
    await call.answer()


async def send_contest_top(message: Message, contest, lang: str):
    """Konkurs TOP-10 ko'rsatish"""
    top = await get_contest_top(contest.id, limit=10)
    if not top:
        rows = t("no_participants", lang)
    else:
        medals = ["🥇", "🥈", "🥉"]
        lines = []
        for i, (u, p) in enumerate(top, start=1):
            medal = medals[i - 1] if i <= 3 else f"{i}."
            name = f"@{u.username}" if u.username else u.full_name[:15]
            lines.append(f"{medal} {name} — <b>{p.ref_count}</b> ball")
        rows = "\n".join(lines)

    text = t(
        "top_contest_results",
        lang,
        title=contest.title,
        rows=rows,
        end_date=format_datetime(contest.end_date),
    )
    await message.answer(text)


# ════════════════════════════════════════════════════════
#                MENING HAVOLAM
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_my_link"))
async def on_my_link(message: Message, bot: Bot):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language

    ref_link = await generate_referral_link(bot, user.telegram_id)
    count = await get_user_referral_count(user.id)

    text = t("my_link_title", lang, link=ref_link, count=count)
    share_text = t("share_text", lang)

    await message.answer(text, reply_markup=my_link_kb(ref_link, share_text, lang))


# ════════════════════════════════════════════════════════
#                MENING DO'STLARIM
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_my_friends"))
async def on_my_friends(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language

    total_count = await get_user_referral_count(user.id)

    # So'nggi 10 ta referral
    referrals = await get_user_referrals(user.id, limit=10)
    verified_count = sum(1 for r in referrals if r.status == "verified")

    if not referrals:
        list_text = t("no_friends_yet", lang)
    else:
        lines = []
        # User nomlarini olish
        from sqlalchemy import select
        async with async_session() as session:
            for i, r in enumerate(referrals, start=1):
                u_result = await session.execute(
                    select(User).where(User.id == r.referred_id)
                )
                u = u_result.scalar_one_or_none()
                if u:
                    name = f"@{u.username}" if u.username else u.full_name[:20]
                    status = "✅" if r.status == "verified" else "⏳"
                    lines.append(f"{i}. {name} {status}")
        list_text = "\n".join(lines) if lines else t("no_friends_yet", lang)

    await message.answer(
        t(
            "my_friends_title",
            lang,
            total=total_count,
            verified=verified_count,
            list=list_text,
        )
    )


# ════════════════════════════════════════════════════════
#                TOP REYTING
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_top"))
async def on_top(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language

    contests = await get_active_contests()
    if not contests:
        await message.answer(t("no_contests", lang))
        return

    await message.answer(
        t("top_title", lang), reply_markup=top_contests_kb(contests, lang)
    )


@user_router.callback_query(F.data.startswith("top_contest:"))
async def on_top_contest(call: CallbackQuery):
    contest_id = int(call.data.split(":")[1])
    user = await get_user_by_telegram_id(call.from_user.id)
    if not user:
        return
    lang = user.language

    contest = await get_contest_by_id(contest_id)
    if not contest:
        return

    await send_contest_top(call.message, contest, lang)
    await call.answer()


# ════════════════════════════════════════════════════════
#                MA'LUMOT
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_info"))
async def on_info(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language
    await message.answer(t("info_text", lang))


# ════════════════════════════════════════════════════════
#                SOZLAMALAR
# ════════════════════════════════════════════════════════

@user_router.message(text_matches("btn_settings"))
async def on_settings(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language
    await message.answer(t("settings_title", lang), reply_markup=settings_kb(lang))


@user_router.callback_query(F.data == "settings:lang")
async def on_settings_lang(call: CallbackQuery):
    await call.message.edit_text(
        t("choose_language", "uz"), reply_markup=language_kb()
    )
    await call.answer()


@user_router.callback_query(F.data == "settings:notif")
async def on_settings_notif(call: CallbackQuery):
    enabled = await toggle_notifications(call.from_user.id)
    user = await get_user_by_telegram_id(call.from_user.id)
    lang = user.language if user else "uz"
    msg = t("notifications_on" if enabled else "notifications_off", lang)
    await call.answer(msg, show_alert=True)


@user_router.callback_query(F.data == "settings:help")
async def on_settings_help(call: CallbackQuery):
    user = await get_user_by_telegram_id(call.from_user.id)
    lang = user.language if user else "uz"
    await call.message.answer(t("help_text", lang))
    await call.answer()


# ════════════════════════════════════════════════════════
#                ASOSIY MENYUGA QAYTISH (admin'dan)
# ════════════════════════════════════════════════════════

@user_router.message(F.text.startswith("🏠"))
async def on_back_to_main(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        return
    lang = user.language
    await message.answer(t("main_menu", lang), reply_markup=main_menu_kb(lang))
