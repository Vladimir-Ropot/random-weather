from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
    )

    country: Mapped[str] = mapped_column(
        String(100),
    )

    temperature: Mapped[float] = mapped_column(
        Float,
    )

    wind_speed: Mapped[float] = mapped_column(
        Float,
    )

    weather: Mapped[str] = mapped_column(
        String(100),
    )

    time: Mapped[datetime] = mapped_column(
        DateTime,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )


class Favourite(Base):
    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city: Mapped[str] = mapped_column(String(100), unique=True)
    country: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
