MAX_CITY_ATTEMPTS = 3
HISTORY_LIMIT = 3

cities = [
    {
        "city": "Tokyo",
        "country": "Japan",
        "latitude": 35.6762,
        "longitude": 139.6503
    },
    {
        "city": "Moscow",
        "country": "Russia",
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    {
        "city": "Paris",
        "country": "France",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    {
        "city": "New York",
        "country": "USA",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
]


weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}

weatherIcons = {
    "Clear sky": "☀️",
    "Mainly clear": "🌤️",
    "Partly cloudy": "⛅",
    "Overcast": "☁️",
    "Fog": "🌫️",
    "Light drizzle": "🌦️",
    "Moderate drizzle": "🌦️",
    "Dense drizzle": "🌧️",
    "Slight rain": "🌦️",
    "Moderate rain": "🌧️",
    "Heavy rain": "🌧️",
    "Slight snow": "🌨️",
    "Moderate snow": "❄️",
    "Heavy snow": "❄️",
    "Thunderstorm": "⛈️"
};
