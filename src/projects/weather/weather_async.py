import argparse
import asyncio
import time
from datetime import datetime

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    51: "Морось",
    61: "Дождь",
    71: "Снег",
    95: "Гроза",
}


async def get_coordinates(client, city, lang, timeout):
    params = {"name": city, "count": 1, "language": lang}
    response = await client.get(GEOCODING_URL, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if "results" not in data:
        raise ValueError(f"Город '{city}' не найден")

    first = data["results"][0]
    return first["latitude"], first["longitude"], first["name"]


async def get_weather(client, lat, lon, timeout):
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    response = await client.get(WEATHER_URL, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()["current_weather"]


async def get_city_weather(client, city, lang, timeout):
    """Координаты + погода для одного города. Возвращает (name, weather) или бросает."""
    lat, lon, name = await get_coordinates(client, city, lang, timeout)
    weather = await get_weather(client, lat, lon, timeout)
    return name, weather


def describe_error(exc) -> str:
    if isinstance(exc, httpx.HTTPStatusError):
        return f"HTTP {exc.response.status_code}"
    return type(exc).__name__


def display_weather(name, weather):
    city_time = datetime.fromisoformat(weather["time"]).strftime("%d.%m.%Y %H:%M")
    day_part = "день" if weather.get("is_day") == 1 else "ночь"
    condition = WEATHER_CODES.get(weather["weathercode"], "Неизвестно")

    print(f"Город: {name}")
    print(f"Время: {city_time}")
    print(f"Температура: {weather['temperature']}")
    print(f"Скорость ветра: {weather['windspeed']}")
    print(f"Время суток: {day_part}")
    print(f"Погода: {condition}")
    print("-" * 40)


def parse_args():
    parser = argparse.ArgumentParser(description="Погода по городам")
    parser.add_argument(
        "-c",
        "--cities",
        nargs="+",
        required=True,
        help="Города через пробел",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="ru",
        choices=["ru", "en"],
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=5,
    )
    return parser.parse_args()


async def main():
    args = parse_args()
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *(
                get_city_weather(client, city, args.lang, args.timeout)
                for city in args.cities
            ),
            return_exceptions=True,
        )

    for city, result in zip(args.cities, results):
        if isinstance(result, Exception):
            print(f"{city}: {describe_error(result)}")
        else:
            name, weather = result
            display_weather(name, weather)

    print(f"Время: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
