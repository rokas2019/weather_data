from sqlalchemy import Column, String, Float, Date, Integer, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CityDailyWeather(Base):
    __tablename__ = 'city_daily_weather'
    city = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    maxtemp_c = Column(Float)
    mintemp_c = Column(Float)
    avgtemp_c = Column(Float)

    # Relationship to CityHourlyWeather
    hourly_weather = relationship('CityHourlyWeather', back_populates='daily_weather', cascade="all, delete-orphan")


class CityHourlyWeather(Base):
    __tablename__ = 'city_hourly_weather'
    city = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    hour = Column(Integer, primary_key=True)
    temp_celsius = Column(Float)
    condition = Column(String)
    wind_speed_kph = Column(Float)
    wind_direction = Column(String)
    humidity = Column(Integer)
    will_it_rain = Column(Boolean)

    # Composite Foreign Key
    __table_args__ = (
        ForeignKeyConstraint(
            ['city', 'date'],
            ['city_daily_weather.city', 'city_daily_weather.date']
        ),
    )

    # Relationship to CityDailyWeather
    daily_weather = relationship('CityDailyWeather', back_populates='hourly_weather')
