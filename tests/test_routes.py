from models import WeatherHistory
from weather import WeatherServiceError


def test_about(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert response.data.decode() == "This is a random Weather!"


def test_weather_endpoint(
    client,
    mock_city_services,
    mock_fetch_weather,
):
    response = client.get("/api/weather")

    assert response.status_code == 200

    data = response.get_json()

    assert data["city"] == "London"
    assert data["country"] == "United Kingdom"
    assert data["latitude"] == 51.5074
    assert data["longitude"] == -0.1278
    assert data["temperature"] == 18.5
    assert data["wind_speed"] == 7.2
    assert data["weather"] == "Slight rain"
    assert data["weather_code"] == 61
    assert data["time"] == "2026-09-20T15:00"


def test_weather_city_not_found(
    client,
    monkeypatch,
    mock_city_services,
):
    calls = 0

    def mock_get_city_coordinares(city):
        nonlocal calls
        calls += 1
        return {
            "results": []
        }

    monkeypatch.setattr(
        "app.get_city_coordinates",
        mock_get_city_coordinares,
    )

    response = client.get("/api/weather")
    assert response.status_code == 404
    data = response.get_json()

    assert data["error"] == "City not found"
    assert calls == 3


def test_weather_service_unavailable(
    client,
    monkeypatch,
    mock_city_services,
):
    def mock_fetch_weather(city):
        raise WeatherServiceError()

    monkeypatch.setattr(
        "app.fetch_weather",
        mock_fetch_weather,
    )
    response = client.get("/api/weather")

    assert response.status_code == 503

    data = response.get_json()

    assert data["error"] == "Weather service is unavailable"


def test_weather_endpoint_creates_history(
    client,
    db_session,
    mock_city_services,
    mock_fetch_weather,
):
    response = client.get("/api/weather")

    assert response.status_code == 200

    data = response.get_json()

    assert data["city"] == "London"
    assert "id" in data

    history = db_session.query(WeatherHistory).all()

    assert len(history) == 1
    assert history[0].city == "London"
    assert history[0].country == "United Kingdom"
    assert history[0].temperature == 18.5
    assert history[0].weather == "Slight rain"


def test_weather_city_found_not_second_attempt(
    client,
    monkeypatch,
    mock_fetch_weather
):
    attempts = 0

    def mock_get_random_city():
        return {
            "city": "London"
        }

    monkeypatch.setattr(
        "app.get_random_city",
        mock_get_random_city,
    )

    def mock_get_city_coordinates(city):
        nonlocal attempts

        attempts += 1

        if attempts == 1:
            return {
                "results": []
            }
        return {
            "results": [
                {
                    "name": "London",
                    "country": "United Kingdom",
                    "latitude": 51.5074,
                    "longitude": -0.1278,
                }
            ]
        }

    monkeypatch.setattr(
        "app.get_city_coordinates",
        mock_get_city_coordinates,
    )

    response = client.get("/api/weather")

    assert response.status_code == 200
    assert attempts == 2

    data = response.get_json()

    assert data["city"] == "London"
    assert data["weather_code"] == 61
