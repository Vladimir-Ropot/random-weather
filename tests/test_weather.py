from unittest.mock import Mock

import pytest
import requests

from weather import (
    WeatherServiceError,
    _get_json,
    format_weather_data,
    get_weather_description,
)


@pytest.mark.parametrize(
    "code, expected",
    [
        (0, "Clear sky"),
        (1, "Mainly clear"),
        (61, "Slight rain"),
    ],
)
def test_get_weather_description(code, expected):
    result = get_weather_description(code)

    assert result == expected


def test_get_weather_description_unknown_code():
    result = get_weather_description(999)

    assert result == "Unknown weather"


def test_format_weather_data():
    city = {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }

    data = {
        "current": {
            "temperature_2m": 18.5,
            "wind_speed_10m": 7.2,
            "weather_code": 61,
            "time": "2026-09-20T15:00",
        }
    }

    result = format_weather_data(city, data)

    assert result == {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "temperature": 18.5,
        "wind_speed": 7.2,
        "weather": "Slight rain",
        "weather_code": 61,
        "time": "2026-09-20T15:00",
    }


def test_get_json_success(monkeypatch):
    response = Mock()
    response.json.return_value = {
        "temperature": 20
    }

    monkeypatch.setattr(
        "weather.requests.get",
        lambda *args, **kwargs: response,
    )

    result = _get_json("https://example.com")

    assert result ==  {
        "temperature": 20
    }


def test_get_json_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException()

    monkeypatch.setattr(
        "weather.requests.get",
        mock_get,
    )

    with pytest.raises(WeatherServiceError):
        _get_json("https://example.com")


def test_get_json_http_error(monkeypatch):
    response = requests.Response()
    response.status_code = 500
    response.url = "https://example.com"

    monkeypatch.setattr(
        "weather.requests.get",
        lambda *args, **kwargs: response,
    )

    with pytest.raises(WeatherServiceError):
        _get_json("https://example.com")
