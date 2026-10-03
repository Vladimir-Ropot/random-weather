import requests

from constants import weather_codes

RANDOM_CITY_URL = (
    "https://random-city-api.vercel.app/api/random-city"
)
GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)
OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
)
REQUEST_TIMEOUT = 5


class WeatherServiceError(Exception):
    pass


def get_weather_description(code: int) -> str:
    return weather_codes.get(code, "Unknown weather")


def _get_json(
    url: str,
    params: dict | None = None,
) -> dict:
    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise WeatherServiceError() from error

    return response.json()


def fetch_weather(city: dict) -> dict:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }

    return _get_json(
        OPEN_METEO_URL,
        params=params,
    )


def format_weather_data(city: dict, data: dict) -> dict:
    current = data["current"]
    weather_code = current["weather_code"]

    return {
        "city": city["city"],
        "country": city["country"],
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
        "weather": get_weather_description(weather_code),
        "weather_code": weather_code,
        "time": current["time"],
        "latitude": city["latitude"],
        "longitude": city["longitude"],
    }


def get_random_city() -> dict:
    return _get_json(RANDOM_CITY_URL)


def get_city_coordinates(city_name: str) -> dict:
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    return _get_json(
        GEOCODING_URL,
        params=params,
    )
