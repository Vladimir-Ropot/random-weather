import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from models import Base


@pytest.fixture
def db_session(monkeypatch):
    engine = create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5433/random_weather_test"
    )

    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)

    monkeypatch.setattr(
        "app.SessionLocal",
        TestingSessionLocal,
    )

    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(db_session):
    app.config["TESTING"] = True

    return app.test_client()


@pytest.fixture
def mock_city_services(monkeypatch):
    def mock_get_random_city():
        return {
            "city": "London"
        }

    def mock_get_city_coordinates(city):
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
        "app.get_random_city",
        mock_get_random_city,
    )

    monkeypatch.setattr(
        "app.get_city_coordinates",
        mock_get_city_coordinates,
    )


@pytest.fixture
def mock_fetch_weather(monkeypatch):
    def mock_weather(city):
        return {
            "current": {
                "temperature_2m": 18.5,
                "wind_speed_10m": 7.2,
                "weather_code": 61,
                "time": "2026-09-20T15:00",
            }
        }

    monkeypatch.setattr(
        "app.fetch_weather",
        mock_weather,
    )
