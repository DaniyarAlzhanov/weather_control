import aioconsole
from openpyxl import Workbook
from sqlalchemy import select

from database import async_session
from models import WeatherData


async def export_to_excel():
    """Функция экспорта данных о погоде в xlsx файл."""

    async with async_session() as session:
        result = await session.execute(
            select(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10)
        )
        data = result.scalars().all()
        wb = Workbook()
        ws = wb.active
        ws.append(
            [
                "Timestamp",
                "Temperature",
                "Wind Direction",
                "Wind Speed",
                "Pressure",
                "Precipitation Type",
                "Precipitation Amount",
            ]
        )
        for entry in data:
            ws.append(
                [
                    entry.timestamp,
                    entry.temperature,
                    entry.wind_direction,
                    entry.wind_speed,
                    entry.pressure,
                    entry.precipitation_type,
                    entry.precipitation_amount,
                ]
            )
        wb.save("weather_data.xlsx")


async def export():
    while True:
        command = await aioconsole.ainput("Введите команду (export): ")
        if command == "export":
            await export_to_excel()
