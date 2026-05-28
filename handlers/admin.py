"""
Admin tomonidagi handlerlar.
- /admin paneli
- Reklamalar boshqaruvi
- Konkurslar boshqaruvi
- Kanallar boshqaruvi
- Statistika
- Broadcast (ommaviy xabar)
- Foydalanuvchilarni boshqarish
"""
import asyncio
import json
import logging
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from sqlalchemy import select, func

from config import config
from database import (
    async_session,
    User,
    Channel,
    Ad,
    Contest,
    ContestParticipant,
    Referral,
    get_or_create_user,
    get_user_by_telegram_id,
    get_all_channels,
    get_active_contests,
    get_contest_by_id,
    get_contest_top,
    get_stats,
    get_all_user_ids,
    block_user,
    unblock_user,
    get_user_referral_count,
)
from locales import t, TRANSLATIONS
from keyboards import (
    admin_main_kb,
    admin_cancel_kb,
    admin_skip_cancel_kb,
    admin_ads_menu_kb,
    admin_contests_menu_kb,
    admin_channels_menu_kb,
    main_menu_kb,
    ad_link_type_kb,
    contest_type_kb,
    admin_ad_card_kb,
    admin_contest_card_kb,
    admin_channel_card_kb,
    admin_channels_select_kb,
    admin_user_actions_kb,
    confirm_inline_kb,
    yes_no_inline_kb,
)
from states import (
    AdCreation,
    ContestCreation,
    ChannelAdd,
    Broadcast,
    UserSearch,
)
from utils import is_admin, format_link_url, format_datetime

logger = logging.getLogger(__name__)
admin_router = Router()


# ════════════════════════════════════════════════════════
#               ADMIN FILTER (router darajasida)
# ════════════════════════════════════════════════════════

class IsAdmin(Filter):
    """Admin filteri — faqat admin user-larini o'tkazadi."""
    async def __call__(self, event) -> bool:
        if hasattr(event, "from_user") and event.from_user:
            return is_admin(event.from_user.id)
        return False


# Router darajasida filter — barcha handlerlar uchun bir marta
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


def text_matches_admin(key: str):
    texts = [TRANSLATIONS[key]["uz"], TRANSLATIONS[key]["ru"]]
    return F.text.in_(texts)


async def get_admin_lang(telegram_id: int) -> str:
    user = await get_user_by_telegram_id(telegram_id)
    return user.language if user else "uz"


# ════════════════════════════════════════════════════════
#                    /ADMIN BOSHLASH
# ════════════════════════════════════════════════════════

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    # Adminni bazaga ham qo'shamiz (agar yo'q bo'lsa)
    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(t("admin_welcome", lang), reply_markup=admin_main_kb(lang))


@admin_router.message(text_matches_admin("admin_back"))
async def on_admin_back(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(t("admin_welcome", lang), reply_markup=admin_main_kb(lang))


@admin_router.message(text_matches_admin("cancel"))
async def on_admin_cancel(message: Message, state: FSMContext):
    cur = await state.get_state()
    if cur is not None:
        await state.clear()
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(t("cancelled", lang), reply_markup=admin_main_kb(lang))


# ════════════════════════════════════════════════════════
#               📢 REKLAMALAR BO'LIMI
# ════════════════════════════════════════════════════════

@admin_router.message(text_matches_admin("admin_btn_ads"))
async def on_admin_ads(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(t("admin_ads_menu", lang), reply_markup=admin_ads_menu_kb(lang))


# ─── Yangi reklama yaratish (FSM) ───

@admin_router.message(text_matches_admin("admin_btn_new_ad"))
async def on_new_ad_start(message: Message, state: FSMContext):
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_photo)
    await message.answer(
        t("ad_step_photo", lang), reply_markup=admin_skip_cancel_kb(lang)
    )


@admin_router.message(AdCreation.waiting_photo, F.photo)
async def ad_photo_received(message: Message, state: FSMContext):
    await state.update_data(photo_file_id=message.photo[-1].file_id)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_title)
    await message.answer(t("ad_step_title", lang), reply_markup=admin_cancel_kb(lang))


@admin_router.message(AdCreation.waiting_photo, text_matches_admin("skip"))
async def ad_photo_skip(message: Message, state: FSMContext):
    await state.update_data(photo_file_id=None)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_title)
    await message.answer(t("ad_step_title", lang), reply_markup=admin_cancel_kb(lang))


@admin_router.message(AdCreation.waiting_title, F.text)
async def ad_title_received(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_description)
    await message.answer(t("ad_step_description", lang), reply_markup=admin_cancel_kb(lang))


@admin_router.message(AdCreation.waiting_description, F.text)
async def ad_desc_received(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_promo_text)
    await message.answer(
        t("ad_step_promo", lang), reply_markup=admin_skip_cancel_kb(lang)
    )


@admin_router.message(AdCreation.waiting_promo_text, text_matches_admin("skip"))
async def ad_promo_skip(message: Message, state: FSMContext):
    await state.update_data(promo_text=None)
    await ask_link_type(message, state)


@admin_router.message(AdCreation.waiting_promo_text, F.text)
async def ad_promo_received(message: Message, state: FSMContext):
    await state.update_data(promo_text=message.text)
    await ask_link_type(message, state)


async def ask_link_type(message: Message, state: FSMContext):
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_link_type)
    await message.answer(t("ad_step_link_type", lang), reply_markup=ad_link_type_kb(lang))


@admin_router.callback_query(AdCreation.waiting_link_type, F.data.startswith("adlink:"))
async def ad_link_type_selected(call: CallbackQuery, state: FSMContext):
    link_type = call.data.split(":")[1]
    await state.update_data(link_type=link_type)
    lang = await get_admin_lang(call.from_user.id)
    await state.set_state(AdCreation.waiting_link_url)
    await call.message.answer(t("ad_step_link_url", lang), reply_markup=admin_cancel_kb(lang))
    await call.answer()


@admin_router.message(AdCreation.waiting_link_url, F.text)
async def ad_url_received(message: Message, state: FSMContext):
    await state.update_data(link_url=message.text.strip())
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(AdCreation.waiting_button_text)
    await message.answer(t("ad_step_button", lang), reply_markup=admin_skip_cancel_kb(lang))


@admin_router.message(AdCreation.waiting_button_text, text_matches_admin("skip"))
async def ad_button_skip(message: Message, state: FSMContext):
    await state.update_data(button_text="🛒 Olish")
    await ad_show_preview(message, state)


@admin_router.message(AdCreation.waiting_button_text, F.text)
async def ad_button_received(message: Message, state: FSMContext):
    await state.update_data(button_text=message.text.strip())
    await ad_show_preview(message, state)


async def ad_show_preview(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = await get_admin_lang(message.from_user.id)

    caption = f"<b>{data['title']}</b>\n\n{data['description']}"
    if data.get("promo_text"):
        caption += f"\n\n🔥 <i>{data['promo_text']}</i>"
    caption += f"\n\n📋 Link: {data['link_url']}"

    # Preview
    if data.get("photo_file_id"):
        await message.answer_photo(
            photo=data["photo_file_id"],
            caption=caption,
        )
    else:
        await message.answer(caption)

    await state.set_state(AdCreation.confirm)
    await message.answer(
        t("ad_preview", lang), reply_markup=confirm_inline_kb("adconfirm", lang)
    )


@admin_router.callback_query(AdCreation.confirm, F.data == "adconfirm:yes")
async def ad_save(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = await get_admin_lang(call.from_user.id)

    async with async_session() as session:
        ad = Ad(
            photo_file_id=data.get("photo_file_id"),
            title=data["title"],
            description=data["description"],
            promo_text=data.get("promo_text"),
            link_type=data["link_type"],
            link_url=data["link_url"],
            button_text=data["button_text"],
            is_active=True,
        )
        session.add(ad)
        await session.commit()

    await state.clear()
    await call.message.answer(
        t("ad_saved", lang), reply_markup=admin_ads_menu_kb(lang)
    )
    await call.answer("✅")


@admin_router.callback_query(AdCreation.confirm, F.data == "adconfirm:no")
async def ad_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(call.from_user.id)
    await call.message.answer(t("cancelled", lang), reply_markup=admin_ads_menu_kb(lang))
    await call.answer()


# ─── Reklamalar ro'yxati ───

@admin_router.message(text_matches_admin("admin_btn_ads_list"))
async def on_ads_list(message: Message):
    lang = await get_admin_lang(message.from_user.id)
    async with async_session() as session:
        result = await session.execute(select(Ad).order_by(Ad.created_at.desc()))
        ads = list(result.scalars().all())

    if not ads:
        await message.answer(t("ads_list_empty", lang))
        return

    for ad in ads:
        caption = (
            f"<b>#{ad.id} — {ad.title}</b>\n\n"
            f"{ad.description[:200]}{'...' if len(ad.description) > 200 else ''}\n\n"
            f"🔗 {ad.link_url}\n"
            f"📅 {format_datetime(ad.created_at)}\n"
            f"📊 Ko'rilgan: {ad.views_count} | Bosilgan: {ad.clicks_count}"
        )
        kb = admin_ad_card_kb(ad.id, lang)
        try:
            if ad.photo_file_id:
                await message.answer_photo(photo=ad.photo_file_id, caption=caption, reply_markup=kb)
            else:
                await message.answer(caption, reply_markup=kb)
        except Exception as e:
            logger.error(f"Reklama ko'rsatilmadi: {e}")


@admin_router.callback_query(F.data.startswith("addel:"))
async def ad_delete(call: CallbackQuery):
    ad_id = int(call.data.split(":")[1])
    lang = await get_admin_lang(call.from_user.id)
    async with async_session() as session:
        result = await session.execute(select(Ad).where(Ad.id == ad_id))
        ad = result.scalar_one_or_none()
        if ad:
            await session.delete(ad)
            await session.commit()
    await call.answer(t("ad_deleted", lang))
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass


@admin_router.callback_query(F.data.startswith("adsend:"))
async def ad_send_to_channel(call: CallbackQuery):
    ad_id = int(call.data.split(":")[1])
    lang = await get_admin_lang(call.from_user.id)

    channels = await get_all_channels()
    if not channels:
        await call.answer(t("channels_list_empty", lang), show_alert=True)
        return

    await call.message.answer(
        t("ad_select_channel", lang),
        reply_markup=admin_channels_select_kb(channels, f"adsendto:{ad_id}", lang),
    )
    await call.answer()


@admin_router.callback_query(F.data.startswith("adsendto:"))
async def ad_send_to_channel_confirm(call: CallbackQuery, bot: Bot):
    parts = call.data.split(":")
    ad_id = int(parts[1])
    second = parts[2]
    lang = await get_admin_lang(call.from_user.id)

    if second == "cancel":
        await call.message.delete()
        await call.answer()
        return

    channel_id = int(second)

    async with async_session() as session:
        ad_res = await session.execute(select(Ad).where(Ad.id == ad_id))
        ad = ad_res.scalar_one_or_none()
        ch_res = await session.execute(select(Channel).where(Channel.id == channel_id))
        ch = ch_res.scalar_one_or_none()

    if not ad or not ch:
        await call.answer(t("error", lang), show_alert=True)
        return

    caption = f"<b>{ad.title}</b>\n\n{ad.description}"
    if ad.promo_text:
        caption += f"\n\n🔥 <i>{ad.promo_text}</i>"

    url = format_link_url(ad.link_type, ad.link_url)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=ad.button_text, url=url)]]
    )

    try:
        if ad.photo_file_id:
            await bot.send_photo(
                chat_id=ch.channel_id, photo=ad.photo_file_id, caption=caption, reply_markup=kb
            )
        else:
            await bot.send_message(chat_id=ch.channel_id, text=caption, reply_markup=kb)
        await call.answer(t("ad_sent_to_channel", lang), show_alert=True)
    except Exception as e:
        logger.error(f"Kanalga jo'natilmadi: {e}")
        await call.answer(f"❌ {e}", show_alert=True)


# ════════════════════════════════════════════════════════
#               🏆 KONKURSLAR BO'LIMI
# ════════════════════════════════════════════════════════

@admin_router.message(text_matches_admin("admin_btn_contests"))
async def on_admin_contests(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(
        t("admin_contests_menu", lang), reply_markup=admin_contests_menu_kb(lang)
    )


# ─── Yangi konkurs yaratish (FSM) ───

@admin_router.message(text_matches_admin("admin_btn_new_contest"))
async def on_new_contest_start(message: Message, state: FSMContext):
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_title)
    await message.answer(
        t("contest_step_title", lang), reply_markup=admin_cancel_kb(lang)
    )


@admin_router.message(ContestCreation.waiting_title, F.text)
async def contest_title_received(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_description)
    await message.answer(
        t("contest_step_description", lang), reply_markup=admin_cancel_kb(lang)
    )


@admin_router.message(ContestCreation.waiting_description, F.text)
async def contest_desc_received(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_photo)
    await message.answer(
        t("contest_step_photo", lang), reply_markup=admin_skip_cancel_kb(lang)
    )


@admin_router.message(ContestCreation.waiting_photo, F.photo)
async def contest_photo_received(message: Message, state: FSMContext):
    await state.update_data(photo_file_id=message.photo[-1].file_id)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_type)
    await message.answer(t("contest_step_type", lang), reply_markup=contest_type_kb(lang))


@admin_router.message(ContestCreation.waiting_photo, text_matches_admin("skip"))
async def contest_photo_skip(message: Message, state: FSMContext):
    await state.update_data(photo_file_id=None)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_type)
    await message.answer(t("contest_step_type", lang), reply_markup=contest_type_kb(lang))


@admin_router.callback_query(ContestCreation.waiting_type, F.data.startswith("ctype:"))
async def contest_type_received(call: CallbackQuery, state: FSMContext):
    ctype = call.data.split(":")[1]
    await state.update_data(contest_type=ctype)
    lang = await get_admin_lang(call.from_user.id)

    if ctype == "first_n":
        # Avval — nechta obunachi kerakligini so'rash
        await state.set_state(ContestCreation.waiting_required_refs)
        await call.message.answer(
            t("contest_step_required_refs", lang), reply_markup=admin_cancel_kb(lang)
        )
    else:
        await state.update_data(required_refs=0)
        await state.set_state(ContestCreation.waiting_prizes)
        await call.message.answer(
            t("contest_step_prizes", lang), reply_markup=admin_cancel_kb(lang)
        )
    await call.answer()


@admin_router.message(ContestCreation.waiting_required_refs, F.text)
async def contest_required_refs_received(message: Message, state: FSMContext):
    try:
        n = int(message.text.strip())
        if n < 1:
            raise ValueError
    except ValueError:
        await message.answer("❌ Faqat 1 dan katta son kiriting / Введите число больше 1")
        return
    await state.update_data(required_refs=n)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_prizes)
    await message.answer(
        t("contest_step_prizes", lang), reply_markup=admin_cancel_kb(lang)
    )


@admin_router.message(ContestCreation.waiting_prizes, F.text)
async def contest_prizes_received(message: Message, state: FSMContext):
    prizes_list = [line.strip() for line in message.text.split("\n") if line.strip()]
    await state.update_data(prizes=prizes_list)
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ContestCreation.waiting_end_date)
    await message.answer(
        t("contest_step_end_date", lang), reply_markup=admin_cancel_kb(lang)
    )


@admin_router.message(ContestCreation.waiting_end_date, F.text)
async def contest_end_date_received(message: Message, state: FSMContext):
    try:
        end_date = datetime.strptime(message.text.strip(), "%d.%m.%Y")
        # Soatlar — kunning oxiri
        end_date = end_date.replace(hour=23, minute=59, second=59)
    except ValueError:
        await message.answer("❌ Format: DD.MM.YYYY (masalan: 30.06.2026)")
        return

    data = await state.get_data()
    lang = await get_admin_lang(message.from_user.id)

    async with async_session() as session:
        contest = Contest(
            title=data["title"],
            description=data["description"],
            photo_file_id=data.get("photo_file_id"),
            contest_type=data["contest_type"],
            prizes=json.dumps(data["prizes"], ensure_ascii=False),
            required_refs=data.get("required_refs", 0),
            end_date=end_date,
            status="active",
        )
        session.add(contest)
        await session.commit()

    await state.clear()
    await message.answer(
        t("contest_saved", lang), reply_markup=admin_contests_menu_kb(lang)
    )


# ─── Konkurslar ro'yxati ───

@admin_router.message(text_matches_admin("admin_btn_contests_list"))
async def on_contests_list(message: Message):
    lang = await get_admin_lang(message.from_user.id)
    async with async_session() as session:
        result = await session.execute(select(Contest).order_by(Contest.created_at.desc()))
        contests = list(result.scalars().all())

    if not contests:
        await message.answer(t("no_contests", lang))
        return

    for c in contests:
        try:
            prizes = json.loads(c.prizes)
        except Exception:
            prizes = []
        prizes_text = "\n".join(prizes) if prizes else "—"

        # Ishtirokchilar soni
        async with async_session() as session:
            count = await session.scalar(
                select(func.count(ContestParticipant.id)).where(
                    ContestParticipant.contest_id == c.id
                )
            )

        caption = (
            f"🏆 <b>#{c.id} — {c.title}</b>\n"
            f"📅 Tugaydi: {format_datetime(c.end_date)}\n"
            f"👥 Ishtirokchilar: {count or 0}\n"
            f"📊 Status: {c.status}\n\n"
            f"🎁 Sovg'alar:\n{prizes_text}"
        )
        kb = admin_contest_card_kb(c.id, c.status, lang)
        if c.photo_file_id:
            try:
                await message.answer_photo(c.photo_file_id, caption=caption, reply_markup=kb)
                continue
            except Exception:
                pass
        await message.answer(caption, reply_markup=kb)


@admin_router.callback_query(F.data.startswith("cend:"))
async def contest_end(call: CallbackQuery):
    contest_id = int(call.data.split(":")[1])
    lang = await get_admin_lang(call.from_user.id)
    async with async_session() as session:
        result = await session.execute(select(Contest).where(Contest.id == contest_id))
        contest = result.scalar_one_or_none()
        if contest:
            contest.status = "ended"
            await session.commit()
    await call.answer(t("contest_ended", lang), show_alert=True)


@admin_router.callback_query(F.data.startswith("cwinners:"))
async def contest_announce_winners(call: CallbackQuery, bot: Bot):
    contest_id = int(call.data.split(":")[1])
    lang = await get_admin_lang(call.from_user.id)

    contest = await get_contest_by_id(contest_id)
    if not contest:
        await call.answer(t("error", lang), show_alert=True)
        return

    try:
        prizes = json.loads(contest.prizes)
    except Exception:
        prizes = []

    # G'oliblarni aniqlash
    if contest.contest_type == "top3":
        top = await get_contest_top(contest_id, limit=3)
        winners_lines = []
        async with async_session() as session:
            for i, (u, p) in enumerate(top, start=1):
                prize = prizes[i - 1] if i <= len(prizes) else "—"
                name = f"@{u.username}" if u.username else u.full_name
                winners_lines.append(f"{['🥇','🥈','🥉'][i-1]} {name} — {prize} ({p.ref_count} ball)")

                # Bazada is_winner belgilash
                part_res = await session.execute(
                    select(ContestParticipant).where(
                        ContestParticipant.contest_id == contest_id,
                        ContestParticipant.user_id == u.id,
                    )
                )
                part = part_res.scalar_one_or_none()
                if part:
                    part.is_winner = True
                    part.winner_place = i
            await session.commit()
        winners_text = "\n".join(winners_lines) if winners_lines else "—"
    else:
        # first_n turi
        top = await get_contest_top(contest_id, limit=10)
        required = contest.required_refs
        winners_lines = []
        async with async_session() as session:
            for u, p in top:
                if p.ref_count >= required:
                    name = f"@{u.username}" if u.username else u.full_name
                    winners_lines.append(f"✅ {name} — {p.ref_count} ball")
                    part_res = await session.execute(
                        select(ContestParticipant).where(
                            ContestParticipant.contest_id == contest_id,
                            ContestParticipant.user_id == u.id,
                        )
                    )
                    part = part_res.scalar_one_or_none()
                    if part:
                        part.is_winner = True
            await session.commit()
        winners_text = "\n".join(winners_lines) if winners_lines else "—"

    # Konkursni yakunlash
    async with async_session() as session:
        result = await session.execute(select(Contest).where(Contest.id == contest_id))
        c = result.scalar_one_or_none()
        if c:
            c.status = "ended"
            await session.commit()

    text = t("winners_announced", lang, title=contest.title, winners=winners_text)
    await call.message.answer(text)

    # Barcha ishtirokchilarga xabar yuborish
    async with async_session() as session:
        parts_res = await session.execute(
            select(User, ContestParticipant)
            .join(ContestParticipant, ContestParticipant.user_id == User.id)
            .where(ContestParticipant.contest_id == contest_id)
        )
        parts = list(parts_res.all())

    for u, _p in parts:
        if not u.notifications_enabled:
            continue
        try:
            msg = t("winners_announced", u.language, title=contest.title, winners=winners_text)
            await bot.send_message(u.telegram_id, msg)
        except Exception as e:
            logger.debug(f"User {u.telegram_id}ga xabar yuborilmadi: {e}")

    await call.answer("✅")


# ════════════════════════════════════════════════════════
#               📡 KANALLAR BO'LIMI
# ════════════════════════════════════════════════════════

@admin_router.message(text_matches_admin("admin_btn_channels"))
async def on_admin_channels(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(
        t("admin_channels_menu", lang), reply_markup=admin_channels_menu_kb(lang)
    )


@admin_router.message(text_matches_admin("admin_btn_add_channel"))
async def on_add_channel_start(message: Message, state: FSMContext):
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(ChannelAdd.waiting_channel)
    await message.answer(
        t("channel_add_instruction", lang), reply_markup=admin_cancel_kb(lang)
    )


@admin_router.message(ChannelAdd.waiting_channel)
async def channel_received(message: Message, state: FSMContext, bot: Bot):
    lang = await get_admin_lang(message.from_user.id)
    channel_id = None
    title = None
    username = None

    # 1) Forward qilingan xabar
    if message.forward_from_chat:
        chat = message.forward_from_chat
        channel_id = chat.id
        title = chat.title
        username = chat.username

    # 2) @username yoki link
    elif message.text:
        text = message.text.strip()
        if text.startswith("@"):
            text = text[1:]
        elif text.startswith("https://t.me/"):
            text = text.replace("https://t.me/", "").split("/")[0].replace("+", "")
        elif text.startswith("t.me/"):
            text = text.replace("t.me/", "").split("/")[0].replace("+", "")

        try:
            chat = await bot.get_chat(f"@{text}")
            channel_id = chat.id
            title = chat.title
            username = chat.username
        except Exception as e:
            logger.error(f"Kanal topilmadi: {e}")
            await message.answer(t("channel_error", lang))
            return

    if not channel_id:
        await message.answer(t("channel_error", lang))
        return

    # Bot kanalda admin ekanligini tekshirish
    try:
        bot_info = await bot.get_me()
        member = await bot.get_chat_member(channel_id, bot_info.id)
        if member.status not in ("administrator", "creator"):
            await message.answer(
                "❌ Bot kanalda admin emas / Бот не админ в канале"
            )
            return
    except Exception as e:
        logger.error(f"Tekshirish xato: {e}")
        await message.answer(t("channel_error", lang))
        return

    # Invite link
    try:
        if username:
            invite_link = f"https://t.me/{username}"
        else:
            invite_link = await bot.export_chat_invite_link(channel_id)
    except Exception:
        invite_link = f"https://t.me/c/{str(channel_id)[4:]}"  # private channel placeholder

    await state.update_data(
        channel_id=channel_id, title=title, username=username, invite_link=invite_link
    )
    await state.set_state(ChannelAdd.waiting_mandatory)
    await message.answer(
        t("channel_mandatory_q", lang),
        reply_markup=yes_no_inline_kb("chmand", lang),
    )


@admin_router.callback_query(ChannelAdd.waiting_mandatory, F.data.startswith("chmand:"))
async def channel_mandatory_received(call: CallbackQuery, state: FSMContext):
    is_mandatory = call.data.split(":")[1] == "yes"
    data = await state.get_data()
    lang = await get_admin_lang(call.from_user.id)

    async with async_session() as session:
        # Allaqachon bormi?
        existing = await session.execute(
            select(Channel).where(Channel.channel_id == data["channel_id"])
        )
        existing_ch = existing.scalar_one_or_none()
        if existing_ch:
            existing_ch.is_active = True
            existing_ch.is_mandatory = is_mandatory
            existing_ch.title = data["title"]
            existing_ch.invite_link = data["invite_link"]
            await session.commit()
        else:
            ch = Channel(
                channel_id=data["channel_id"],
                channel_username=data.get("username"),
                title=data["title"],
                invite_link=data["invite_link"],
                is_mandatory=is_mandatory,
                is_active=True,
            )
            session.add(ch)
            await session.commit()

    await state.clear()
    await call.message.answer(
        t("channel_added", lang, title=data["title"]),
        reply_markup=admin_channels_menu_kb(lang),
    )
    await call.answer("✅")


@admin_router.message(text_matches_admin("admin_btn_channels_list"))
async def on_channels_list(message: Message):
    lang = await get_admin_lang(message.from_user.id)
    channels = await get_all_channels()
    if not channels:
        await message.answer(t("channels_list_empty", lang))
        return

    for ch in channels:
        mandatory = "✅ Majburiy" if ch.is_mandatory else "⚪️ Ixtiyoriy"
        text = (
            f"📡 <b>{ch.title}</b>\n"
            f"ID: <code>{ch.channel_id}</code>\n"
            f"Username: @{ch.channel_username or '—'}\n"
            f"Status: {mandatory}"
        )
        await message.answer(text, reply_markup=admin_channel_card_kb(ch.id, lang))


@admin_router.callback_query(F.data.startswith("chremove:"))
async def channel_remove(call: CallbackQuery):
    ch_id = int(call.data.split(":")[1])
    lang = await get_admin_lang(call.from_user.id)
    async with async_session() as session:
        result = await session.execute(select(Channel).where(Channel.id == ch_id))
        ch = result.scalar_one_or_none()
        if ch:
            ch.is_active = False
            await session.commit()
    await call.answer(t("channel_removed", lang))
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass


@admin_router.callback_query(F.data.startswith("chtoggle:"))
async def channel_toggle(call: CallbackQuery):
    ch_id = int(call.data.split(":")[1])
    lang = await get_admin_lang(call.from_user.id)
    async with async_session() as session:
        result = await session.execute(select(Channel).where(Channel.id == ch_id))
        ch = result.scalar_one_or_none()
        if ch:
            ch.is_mandatory = not ch.is_mandatory
            await session.commit()
            status = "✅ Majburiy" if ch.is_mandatory else "⚪️ Ixtiyoriy"
            await call.answer(status, show_alert=True)


# ════════════════════════════════════════════════════════
#               📊 STATISTIKA
# ════════════════════════════════════════════════════════

@admin_router.message(text_matches_admin("admin_btn_stats"))
async def on_admin_stats(message: Message):
    lang = await get_admin_lang(message.from_user.id)
    stats = await get_stats()
    await message.answer(t("admin_stats_text", lang, **stats))


# ════════════════════════════════════════════════════════
#               📨 OMMAVIY XABAR (BROADCAST)
# ════════════════════════════════════════════════════════

@admin_router.message(text_matches_admin("admin_btn_broadcast"))
async def on_broadcast_start(message: Message, state: FSMContext):
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(Broadcast.waiting_message)
    await message.answer(
        t("broadcast_instruction", lang), reply_markup=admin_cancel_kb(lang)
    )


@admin_router.message(Broadcast.waiting_message)
async def broadcast_message_received(message: Message, state: FSMContext):
    await state.update_data(
        chat_id=message.chat.id, message_id=message.message_id
    )
    lang = await get_admin_lang(message.from_user.id)

    user_ids = await get_all_user_ids()
    await state.set_state(Broadcast.confirm)
    await message.answer(
        t("broadcast_confirm", lang, count=len(user_ids)),
        reply_markup=confirm_inline_kb("bcast", lang),
    )


@admin_router.callback_query(Broadcast.confirm, F.data == "bcast:yes")
async def broadcast_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    lang = await get_admin_lang(call.from_user.id)
    await call.message.answer(t("broadcast_started", lang))
    await state.clear()
    await call.answer()

    user_ids = await get_all_user_ids()
    success = 0
    failed = 0

    for tg_id in user_ids:
        try:
            await bot.copy_message(
                chat_id=tg_id,
                from_chat_id=data["chat_id"],
                message_id=data["message_id"],
            )
            success += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1
            # Bloklangan userlarni belgilash
            await block_user(tg_id)
        except Exception as e:
            failed += 1
            logger.warning(f"Broadcast xato {tg_id}: {e}")
        # Telegram limiti: 30 xabar/soniya
        await asyncio.sleep(0.04)

    await bot.send_message(
        call.from_user.id,
        t("broadcast_finished", lang, success=success, failed=failed),
    )


@admin_router.callback_query(Broadcast.confirm, F.data == "bcast:no")
async def broadcast_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(call.from_user.id)
    await call.message.answer(t("cancelled", lang), reply_markup=admin_main_kb(lang))
    await call.answer()


# ════════════════════════════════════════════════════════
#               👥 FOYDALANUVCHILAR
# ════════════════════════════════════════════════════════

@admin_router.message(text_matches_admin("admin_btn_users"))
async def on_admin_users(message: Message, state: FSMContext):
    lang = await get_admin_lang(message.from_user.id)
    await state.set_state(UserSearch.waiting_query)
    await message.answer(t("users_menu", lang), reply_markup=admin_cancel_kb(lang))


@admin_router.message(UserSearch.waiting_query, F.text)
async def user_search(message: Message, state: FSMContext):
    query = message.text.strip()
    lang = await get_admin_lang(message.from_user.id)
    await state.clear()

    user = None
    async with async_session() as session:
        if query.isdigit():
            result = await session.execute(
                select(User).where(User.telegram_id == int(query))
            )
            user = result.scalar_one_or_none()
        else:
            uname = query.lstrip("@")
            result = await session.execute(
                select(User).where(User.username == uname)
            )
            user = result.scalar_one_or_none()

    if not user:
        await message.answer(
            t("user_not_found", lang), reply_markup=admin_main_kb(lang)
        )
        return

    refs = await get_user_referral_count(user.id)
    status = t("status_blocked", lang) if user.is_blocked else t("status_active", lang)

    info = t(
        "user_info",
        lang,
        tg_id=user.telegram_id,
        name=user.full_name,
        username=user.username or "—",
        lang=user.language,
        status=status,
        joined=format_datetime(user.joined_at),
        refs=refs,
    )
    await message.answer(
        info,
        reply_markup=admin_user_actions_kb(user.telegram_id, user.is_blocked, lang),
    )


@admin_router.callback_query(F.data.startswith("ublock:"))
async def on_user_block(call: CallbackQuery):
    tg_id = int(call.data.split(":")[1])
    await block_user(tg_id)
    lang = await get_admin_lang(call.from_user.id)
    await call.answer(t("user_blocked", lang), show_alert=True)


@admin_router.callback_query(F.data.startswith("uunblock:"))
async def on_user_unblock(call: CallbackQuery):
    tg_id = int(call.data.split(":")[1])
    await unblock_user(tg_id)
    lang = await get_admin_lang(call.from_user.id)
    await call.answer(t("user_unblocked", lang), show_alert=True)


# ════════════════════════════════════════════════════════
#               ASOSIY MENYUGA (USER PANEL)
# ════════════════════════════════════════════════════════

@admin_router.message(F.text.startswith("🏠"))
async def on_admin_back_to_main(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_admin_lang(message.from_user.id)
    await message.answer(t("main_menu", lang), reply_markup=main_menu_kb(lang))
