import argparse
import sys
from datetime import datetime

import requests

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


def get_coordinates(city: str, lang: str, timeout: int) -> tuple[float, float, str]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": lang}

    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if "results" not in data:
        raise ValueError(f"Город '{city}' не найден")

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    name = data["results"][0]["name"]
    return (lat, lon, name)


def get_weather(lat: float, lon: float, timeout) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": True}

    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    return data["current_weather"]


def main():
    parser = argparse.ArgumentParser(description="Программа для получения погоды по городу")

    parser.add_argument("city", help="Город, погоду которого вы хотите узнать")
    parser.add_argument("-l", "--lang", default="ru", choices=["ru", "en"], help="Язык (по умолчанию ru)")
    parser.add_argument("-t", "--timeout", type=int, default=3, help="Время ожидания ответа")

    args = parser.parse_args()

    try:
        lat, lon, name = get_coordinates(args.city, args.lang, args.timeout)
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            print(e.response.status_code)
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)

    try:
        meteo = get_weather(lat, lon, args.timeout)
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            print(e.response.status_code)
        print(e)
        sys.exit(1)

    print(f"Город: {name}")
    time = datetime.fromisoformat(meteo["time"]).strftime("%d.%m.%Y %H:%M")
    print(f"Время: {time}")
    print(f"Температура: {meteo['temperature']}")
    print(f"Скорость ветра: {meteo['windspeed']}")
    print(f"Время суток: {'день' if meteo.get('is_day') == 1 else 'ночь'}")
    weather = WEATHER_CODES.get(meteo["weathercode"], "Неизвестно")
    print(f"Погода: {weather}")


if __name__ == "__main__":
    main()
