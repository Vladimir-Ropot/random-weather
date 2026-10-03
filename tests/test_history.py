from datetime import UTC, datetime

from models import WeatherHistory


def test_get_history(client, db_session):
    current_record = WeatherHistory(
        city="Berlin",
        country="Germany",
        temperature=20.0,
        wind_speed=5.0,
        weather="Clear sky",
        time=datetime(2026, 9, 24, 16, 0, tzinfo=UTC),
        created_at=datetime(2026, 9, 24, 16, 0, tzinfo=UTC),
    )

    history_record = WeatherHistory(
        city="London",
        country="United Kingdom",
        temperature=18.5,
        wind_speed=7.2,
        weather="Rain",
        time=datetime(2026, 9, 24, 15, 0, tzinfo=UTC),
        created_at=datetime(2026, 9, 24, 15, 0, tzinfo=UTC),
    )

    db_session.add_all([current_record, history_record])
    db_session.commit()

    response = client.get("/api/history")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["city"] == "London"
    assert data[0]["country"] == "United Kingdom"
    assert data[0]["temperature"] == 18.5
    assert data[0]["wind_speed"] == 7.2
    assert data[0]["weather"] == "Rain"


def test_get_history_excludes_current(client, db_session):
    current_record = WeatherHistory(
        city="Berlin",
        country="Germany",
        temperature=20.0,
        wind_speed=5.0,
        weather="Clear sky",
        time=datetime(2026, 9, 24, 16, 0, tzinfo=UTC),
        created_at=datetime(2026, 9, 24, 16, 0, tzinfo=UTC),
    )

    history_record = WeatherHistory(
        city="London",
        country="United Kingdom",
        temperature=18.5,
        wind_speed=7.2,
        weather="Rain",
        time=datetime(2026, 9, 24, 15, 0, tzinfo=UTC),
        created_at=datetime(2026, 9, 24, 15, 0, tzinfo=UTC),
    )

    db_session.add_all([current_record, history_record])
    db_session.commit()

    response = client.get(
        f"/api/history?current_id={current_record.id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 0


def test_get_history_returns_three_latest(client, db_session):
    records = [
        WeatherHistory(
            city="Berlin",
            country="Germany",
            temperature=20.0,
            wind_speed=5.0,
            weather="Clear sky",
            time=datetime(2026, 9, 24, 19, 0, tzinfo=UTC),
            created_at=datetime(2026, 9, 24, 19, 0, tzinfo=UTC),
        ),
        WeatherHistory(
            city="London",
            country="United Kingdom",
            temperature=18.5,
            wind_speed=7.2,
            weather="Rain",
            time=datetime(2026, 9, 24, 18, 0, tzinfo=UTC),
            created_at=datetime(2026, 9, 24, 18, 0, tzinfo=UTC),
        ),
        WeatherHistory(
            city="Paris",
            country="France",
            temperature=21.0,
            wind_speed=4.0,
            weather="Mainly clear",
            time=datetime(2026, 9, 24, 17, 0, tzinfo=UTC),
            created_at=datetime(2026, 9, 24, 17, 0, tzinfo=UTC),
        ),
        WeatherHistory(
            city="Rome",
            country="Italy",
            temperature=25.0,
            wind_speed=3.0,
            weather="Clear sky",
            time=datetime(2026, 9, 24, 16, 0, tzinfo=UTC),
            created_at=datetime(2026, 9, 24, 16, 0, tzinfo=UTC),
        ),
        WeatherHistory(
            city="Madrid",
            country="Spain",
            temperature=27.0,
            wind_speed=2.0,
            weather="Clear sky",
            time=datetime(2026, 9, 24, 15, 0, tzinfo=UTC),
            created_at=datetime(2026, 9, 24, 15, 0, tzinfo=UTC),
        ),
    ]

    db_session.add_all(records)
    db_session.commit()

    response = client.get("/api/history")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 3

    assert data[0]["city"] == "London"
    assert data[1]["city"] == "Paris"
    assert data[2]["city"] == "Rome"