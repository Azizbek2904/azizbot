"""
Ma'lumotlar bazasi modellari va yordamchi funksiyalar.
SQLAlchemy 2.0 async style ishlatilgan.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    BigInteger, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, select, func
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import config


class Base(DeclarativeBase):
    pass


# ──────────────── MODELLAR ────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(5), default="uz")
    referrer_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    channel_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    invite_link: Mapped[str] = mapped_column(String(500))
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    photo_file_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    promo_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    link_type: Mapped[str] = mapped_column(String(20))  # web / telegram / mobile
    link_url: Mapped[str] = mapped_column(String(1000))
    button_text: Mapped[str] = mapped_column(String(100), default="🛒 Olish")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    clicks_count: Mapped[int] = mapped_column(Integer, default=0)


class Contest(Base):
    __tablename__ = "contests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    photo_file_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    contest_type: Mapped[str] = mapped_column(String(20), default="top3")  # top3 / first_n / per_n
    prizes: Mapped[str] = mapped_column(Text)  # JSON ko'rinishida
    required_refs: Mapped[int] = mapped_column(Integer, default=0)  # first_n type uchun
    end_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active / ended / paused
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ContestParticipant(Base):
    __tablename__ = "contest_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contest_id: Mapped[int] = mapped_column(Integer, ForeignKey("contests.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    ref_count: Mapped[int] = mapped_column(Integer, default=0)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_winner: Mapped[bool] = mapped_column(Boolean, default=False)
    winner_place: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    referred_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    contest_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("contests.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


# ──────────────── DB ENGINE ────────────────

engine = create_async_engine(config.DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    """Bazani yaratish (birinchi marta ishga tushganda)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ──────────────── YORDAMCHI FUNKSIYALAR ────────────────

async def get_or_create_user(
    telegram_id: int,
    username: Optional[str],
    full_name: str,
    referrer_telegram_id: Optional[int] = None,
) -> tuple[User, bool]:
    """Userni topish yoki yaratish. (user, is_new) qaytaradi."""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            # Username yangilangan bo'lishi mumkin
            if user.username != username or user.full_name != full_name:
                user.username = username
                user.full_name = full_name
                await session.commit()
            return user, False

        # Yangi user
        referrer_id = None
        if referrer_telegram_id and referrer_telegram_id != telegram_id:
            ref_result = await session.execute(
                select(User).where(User.telegram_id == referrer_telegram_id)
            )
            referrer = ref_result.scalar_one_or_none()
            if referrer:
                referrer_id = referrer.id

        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            referrer_id=referrer_id,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user, True


async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


async def update_user_language(telegram_id: int, language: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.language = language
            await session.commit()


async def toggle_notifications(telegram_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.notifications_enabled = not user.notifications_enabled
            await session.commit()
            return user.notifications_enabled
        return False


async def get_mandatory_channels() -> list[Channel]:
    async with async_session() as session:
        result = await session.execute(
            select(Channel).where(
                Channel.is_active == True, Channel.is_mandatory == True
            )
        )
        return list(result.scalars().all())


async def get_all_channels() -> list[Channel]:
    async with async_session() as session:
        result = await session.execute(
            select(Channel).where(Channel.is_active == True)
        )
        return list(result.scalars().all())


async def get_active_ads() -> list[Ad]:
    async with async_session() as session:
        result = await session.execute(
            select(Ad).where(Ad.is_active == True).order_by(Ad.created_at.desc())
        )
        return list(result.scalars().all())


async def get_ad_by_id(ad_id: int) -> Optional[Ad]:
    async with async_session() as session:
        result = await session.execute(select(Ad).where(Ad.id == ad_id))
        return result.scalar_one_or_none()


async def get_active_contests() -> list[Contest]:
    async with async_session() as session:
        result = await session.execute(
            select(Contest)
            .where(Contest.status == "active")
            .order_by(Contest.created_at.desc())
        )
        return list(result.scalars().all())


async def get_contest_by_id(contest_id: int) -> Optional[Contest]:
    async with async_session() as session:
        result = await session.execute(select(Contest).where(Contest.id == contest_id))
        return result.scalar_one_or_none()


async def join_contest(user_id: int, contest_id: int) -> bool:
    """Foydalanuvchini konkursga qo'shish"""
    async with async_session() as session:
        # Allaqachon ishtirok etganmi
        result = await session.execute(
            select(ContestParticipant).where(
                ContestParticipant.user_id == user_id,
                ContestParticipant.contest_id == contest_id,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            return False

        participant = ContestParticipant(user_id=user_id, contest_id=contest_id)
        session.add(participant)
        await session.commit()
        return True


async def get_participation(user_id: int, contest_id: int) -> Optional[ContestParticipant]:
    async with async_session() as session:
        result = await session.execute(
            select(ContestParticipant).where(
                ContestParticipant.user_id == user_id,
                ContestParticipant.contest_id == contest_id,
            )
        )
        return result.scalar_one_or_none()


async def get_user_referral_count(user_id: int, contest_id: Optional[int] = None) -> int:
    """Foydalanuvchining taklif qilganlar sonini olish"""
    async with async_session() as session:
        query = select(func.count(Referral.id)).where(
            Referral.referrer_id == user_id,
            Referral.status == "verified",
        )
        if contest_id:
            query = query.where(Referral.contest_id == contest_id)
        result = await session.execute(query)
        return result.scalar() or 0


async def get_user_referrals(user_id: int, limit: int = 10) -> list[Referral]:
    """Userning so'nggi taklif qilganlari"""
    async with async_session() as session:
        result = await session.execute(
            select(Referral)
            .where(Referral.referrer_id == user_id)
            .order_by(Referral.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


async def create_referral(referrer_id: int, referred_id: int, contest_id: Optional[int] = None):
    """Referral yaratish"""
    async with async_session() as session:
        # Bu user allaqachon kimnindir referrali bo'lganmi?
        result = await session.execute(
            select(Referral).where(Referral.referred_id == referred_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return None

        ref = Referral(
            referrer_id=referrer_id,
            referred_id=referred_id,
            contest_id=contest_id,
            status="pending",
        )
        session.add(ref)
        await session.commit()
        await session.refresh(ref)
        return ref


async def verify_referral(referred_id: int):
    """Referralni tasdiqlash (obuna bo'lgandan keyin)"""
    async with async_session() as session:
        result = await session.execute(
            select(Referral).where(
                Referral.referred_id == referred_id, Referral.status == "pending"
            )
        )
        ref = result.scalar_one_or_none()
        if not ref:
            return None

        ref.status = "verified"
        ref.verified_at = datetime.utcnow()

        # Konkurs ishtirokchisining ballini oshirish
        if ref.contest_id:
            part_result = await session.execute(
                select(ContestParticipant).where(
                    ContestParticipant.user_id == ref.referrer_id,
                    ContestParticipant.contest_id == ref.contest_id,
                )
            )
            participant = part_result.scalar_one_or_none()
            if participant:
                participant.ref_count += 1

        await session.commit()
        await session.refresh(ref)
        return ref


async def get_contest_top(contest_id: int, limit: int = 10) -> list[tuple[User, ContestParticipant]]:
    """Konkursdagi TOP ishtirokchilar"""
    async with async_session() as session:
        result = await session.execute(
            select(User, ContestParticipant)
            .join(ContestParticipant, ContestParticipant.user_id == User.id)
            .where(ContestParticipant.contest_id == contest_id)
            .order_by(ContestParticipant.ref_count.desc())
            .limit(limit)
        )
        return list(result.all())


async def get_user_place_in_contest(user_id: int, contest_id: int) -> Optional[int]:
    """Userning konkursdagi o'rni"""
    async with async_session() as session:
        result = await session.execute(
            select(ContestParticipant)
            .where(ContestParticipant.contest_id == contest_id)
            .order_by(ContestParticipant.ref_count.desc())
        )
        participants = list(result.scalars().all())
        for i, p in enumerate(participants, start=1):
            if p.user_id == user_id:
                return i
        return None


async def get_stats() -> dict:
    """Umumiy statistika"""
    async with async_session() as session:
        total_users = await session.scalar(select(func.count(User.id)))
        active_users = await session.scalar(
            select(func.count(User.id)).where(User.is_blocked == False)
        )
        total_referrals = await session.scalar(
            select(func.count(Referral.id)).where(Referral.status == "verified")
        )
        total_ads = await session.scalar(select(func.count(Ad.id)))
        total_contests = await session.scalar(select(func.count(Contest.id)))
        active_contests = await session.scalar(
            select(func.count(Contest.id)).where(Contest.status == "active")
        )
        return {
            "total_users": total_users or 0,
            "active_users": active_users or 0,
            "total_referrals": total_referrals or 0,
            "total_ads": total_ads or 0,
            "total_contests": total_contests or 0,
            "active_contests": active_contests or 0,
        }


async def get_all_user_ids() -> list[int]:
    """Barcha bloklanmagan userlarning telegram_id ro'yxati (broadcast uchun)"""
    async with async_session() as session:
        result = await session.execute(
            select(User.telegram_id).where(User.is_blocked == False)
        )
        return [row[0] for row in result.all()]


async def block_user(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.is_blocked = True
            await session.commit()


async def unblock_user(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.is_blocked = False
            await session.commit()
