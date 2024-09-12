from datetime import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=dt.utcnow)
    temperature = Column(Float)
    wind_direction = Column(String)
    wind_speed = Column(Float)
    pressure = Column(Float)
    precipitation_type = Column(String)
    precipitation_amount = Column(Float)
