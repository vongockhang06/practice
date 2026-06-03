from typing import Optional
import datetime
import decimal

from sqlalchemy import Date, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class TwCities(Base):
    __tablename__ = 'tw_cities'
    __table_args__ = (
        PrimaryKeyConstraint('city_name', name='tw_cities_pkey'),
    )

    city_name: Mapped[str] = mapped_column(String(20), primary_key=True)
    latitude: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    longitude: Mapped[decimal.Decimal] = mapped_column(Numeric(7, 4), nullable=False)
    timezone_offset: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('28800'))

    weather_daily_forecasts: Mapped[list['WeatherDailyForecasts']] = relationship('WeatherDailyForecasts', back_populates='tw_cities')


class WeatherDailyForecasts(Base):
    __tablename__ = 'weather_daily_forecasts'
    __table_args__ = (
        ForeignKeyConstraint(['city_name'], ['tw_cities.city_name'], ondelete='CASCADE', name='weather_daily_forecasts_city_name_fkey'),
        PrimaryKeyConstraint('forecast_id', name='weather_daily_forecasts_pkey'),
        UniqueConstraint('city_name', 'forecast_date', name='unique_location_date'),
        Index('idx_forecast_date', 'forecast_date')
    )

    forecast_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    forecast_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    city_name: Mapped[Optional[str]] = mapped_column(String(20))
    temp_day: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    temp_min: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    temp_max: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    pressure: Mapped[Optional[int]] = mapped_column(Integer)
    humidity: Mapped[Optional[int]] = mapped_column(Integer)
    rain_volume: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 2), server_default=text('0.0'))

    tw_cities: Mapped[Optional['TwCities']] = relationship('TwCities', back_populates='weather_daily_forecasts')
