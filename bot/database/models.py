from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from sqlalchemy import select


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    platform_nick = Column(String, nullable=False)
    language = Column(String, default="ru")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.telegram_id"),
        nullable=False,
        index=True
    )

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)

    location = Column(String, nullable=False)

    @staticmethod
    async def get_active_shift(session, user_id):

        result = await session.execute(
            select(Shift).where(
                Shift.user_id == user_id,
                Shift.end_time.is_(None)
            )
        )

        return result.scalar_one_or_none()
