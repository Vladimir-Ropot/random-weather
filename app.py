from datetime import datetime

from flask import Flask, jsonify, render_template, request
from sqlalchemy import select

from constants import HISTORY_LIMIT, MAX_CITY_ATTEMPTS
from db import SessionLocal
from models import Favourite, WeatherHistory
from weather import (
    WeatherServiceError,
    fetch_weather,
    format_weather_data,
    get_city_coordinates,
    get_random_city,
)

app = Flask(__name__)

REQUIRED_FAVORITE_FIELDS = {
    "city",
    "country",
    "latitude",
    "longitude",
}


def serialize_favorite(favorite):
    return {
        "id": favorite.id,
        "city": favorite.city,
        "country": favorite.country,
        "latitude": favorite.latitude,
        "longitude": favorite.longitude,
    }


def serialize_history(record):
    return {
        "id": record.id,
        "city": record.city,
        "country": record.country,
        "temperature": record.temperature,
        "wind_speed": record.wind_speed,
        "weather": record.weather,
        "created_at": record.created_at.isoformat(),
    }


def get_random_location():
    for _ in range(MAX_CITY_ATTEMPTS):
        city_data = get_random_city()
        city_name = city_data["city"]

        location_data = get_city_coordinates(city_name)
        results = location_data.get("results")

        if results:
            location = results[0]

            return {
                "city": location["name"],
                "country": location["country"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
            }
    return None


def save_weather_history(result):
    with SessionLocal() as session:
        history = WeatherHistory(
            city=result["city"],
            country=result["country"],
            temperature=result["temperature"],
            wind_speed=result["wind_speed"],
            weather=result["weather"],
            time=datetime.fromisoformat(result["time"]),
        )

        session.add(history)
        session.commit()

        return history.id


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return "This is a random Weather!"


@app.route("/api/weather")
def weather():
    try:
        city = get_random_location()

        if city is None:
            return jsonify({
                "error": "City not found"
            }), 404

        data = fetch_weather(city)

    except WeatherServiceError:
        return jsonify({
            "error": "Weather service is unavailable"
        }), 503

    result = format_weather_data(city, data)

    result["id"] = save_weather_history(result)

    return jsonify(result)


@app.route("/api/history")
def get_history():
    current_id = request.args.get("current_id", type=int)

    with SessionLocal() as session:
        statement = (
            select(WeatherHistory)
            .where(WeatherHistory.id != current_id)
            .order_by(WeatherHistory.created_at.desc())
            .offset(1)
            .limit(HISTORY_LIMIT)
        )

        records = session.scalars(statement).all()
    
    result = [
        serialize_history(record)
        for record in records
    ]

    return jsonify(result)


@app.route("/api/favorites", methods=["POST"])
def add_favorite():
    data = request.json

    if not data or not REQUIRED_FAVORITE_FIELDS.issubset(data):
        return jsonify({
            "error": "Missing required fields"
        }), 400

    session = SessionLocal()

    try:
        existing_favorite = session.scalar(
            select(Favourite).where(
                Favourite.city == data["city"]
            )
        )

        if existing_favorite:
            return jsonify(
                serialize_favorite(existing_favorite)
            ), 200

        favorite = Favourite(
            city=data["city"],
            country=data["country"],
            latitude=data["latitude"],
            longitude=data["longitude"],
        )

        session.add(favorite)
        session.commit()

        return jsonify(
            serialize_favorite(favorite)
        ), 201

    finally:
        session.close()


@app.route("/api/favorites")
def get_favorites():
    with SessionLocal() as session:
        favorites = session.scalars(
            select(Favourite).order_by(Favourite.city)
        ).all()

        result = [
            serialize_favorite(favorite)
            for favorite in favorites
        ]

        return jsonify(result)


@app.route("/api/favorites/<int:favorite_id>", methods=["DELETE"])
def delete_favorite(favorite_id):
    with SessionLocal() as session:
        favorite = session.get(Favourite, favorite_id)

        if favorite is None:
            return jsonify({
                "error": "Favorite not found"
            }), 404

        session.delete(favorite)
        session.commit()

        return jsonify({
            "message": "Favorite deleted"
        })
