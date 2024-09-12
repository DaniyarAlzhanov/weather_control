import asyncio
import os
import ssl

import aiohttp
from aiohttp import ClientSession
from dotenv import load_dotenv

from database import async_session
from database import init_db
from export import export
from models import WeatherData


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

load_dotenv()
LATITUDE = os.getenv("LATITUDE", "55.684")
LONGITUDE = os.getenv("LONGITUDE", "37.342")
PARAMETERS_FOR_FORECAST = os.getenv(
    "PARAMETERS_FOR_FORECAST",
    "temperature_2m,precipitation,"
    "rain,showers,snowfall,"
    "pressure_msl,surface_pressure,"
    "wind_speed_10m,wind_direction_10m",
)
SAVING_TIME = os.getenv("SAVING_TIME", 180)


async def fetch_weather_data():
    """Функция сбора данных о погоде в заданном регионе."""

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": PARAMETERS_FOR_FORECAST,
    }
    async with ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            precipitation_type = ""
            if data["current"].get("rain"):
                precipitation_type += "rain"
            if data["current"].get("showers"):
                precipitation_type += "showers"
            if data["current"].get("snowfall"):
                precipitation_type += "snowfall"
            weather_data = {
                "temperature": data["current"]["temperature_2m"],
                "wind_direction": data["current"]["wind_direction_10m"],
                "wind_speed": data["current"]["wind_speed_10m"],
                "pressure": data["current"]["pressure_msl"],
                "precipitation_type": precipitation_type,
                "precipitation_amount": data["current"].get("precipitation"),
            }
            return weather_data


async def save_weather_data():
    """Функция сохранения данных о погоде в базу данных."""

    async with async_session() as session:
        data = await fetch_weather_data()
        if data:  # Проверяем, что данные не пустые
            async with session.begin():
                new_entry = WeatherData(
                    temperature=data["temperature"],
                    wind_direction=data["wind_direction"],
                    wind_speed=data["wind_speed"],
                    pressure=data["pressure"],
                    precipitation_type=data["precipitation_type"],
                    precipitation_amount=data["precipitation_amount"],
                )
                session.add(new_entry)
                await session.commit()


async def periodic_weather_update():
    """Функция, задающая интервал сохранения данных о погоде в БД."""

    while True:
        await save_weather_data()
        await asyncio.sleep(SAVING_TIME)


async def main():
    await init_db()
    asyncio.create_task(periodic_weather_update())
    asyncio.create_task(export())
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
