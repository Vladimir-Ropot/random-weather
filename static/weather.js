function convertTemperature(temperature) {
    if (currentUnit === "F") {
        return temperature * 9 /5 + 32;
    }

    return temperature
}


function displayWeather(data) {
    const date = new Date(data.time);
    const icon = weatherIcons[data.weather] || "🌡️";
    const weatherDescription = 
        weatherTranslations[currentLanguage][data.weather] || data.weather;
    const weatherCard = document.getElementById("weather-card");

    setWeatherBackground(data.weather_code);

    city.textContent = data.city;
    temperature.textContent = 
        `${translations[currentLanguage].temperature}:
        ${convertTemperature(data.temperature).toFixed(1)} °${currentUnit}`;
    country.textContent = 
        `${translations[currentLanguage].country}: ${data.country}`;
    wind.textContent = 
        `${translations[currentLanguage].wind}: ${data.wind_speed} km/h`;
    time.textContent =
        `${translations[currentLanguage].time}: ${date.toLocaleString(
            currentLanguage === "ru" ? "ru-RU" : "en-US"
        )}`;
    weatherCard.classList.remove("weather-card-visible");
    void weatherCard.offsetWidth;
    weatherCard.classList.add("weather-card-visible");
    weather.textContent = `${icon} ${weatherDescription}`;
}

function setWeatherBackground(weatherCode) {
    document.body.classList.remove(
        "weather-clear",
        "weather-cloudy",
        "weather-fog",
        "weather-drizzle",
        "weather-rain",
        "weather-snow",
        "weather-showers",
        "weather-storm",
    )

    let weatherClass;

    if (weatherCode === 0) {
        weatherClass = "weather-clear";
    } else if (weatherCode >= 1 && weatherCode <= 3) {
        weatherClass = "weather-cloudy";
    } else if (weatherCode === 45 || weatherCode === 48) {
        weatherClass = "weather-fog";
    } else if (weatherCode >= 51 && weatherCode <= 57) {
        weatherClass = "weather-drizzle";
    } else if (weatherCode >= 61 && weatherCode <= 67) {
        weatherClass = "weather-rain";
    } else if (weatherCode >= 71 && weatherCode <= 77) {
        weatherClass = "weather-snow";
    } else if (weatherCode >= 80 && weatherCode <= 82) {
        weatherClass = "weather-showers";
    } else if (weatherCode === 85 || weatherCode === 86) {
        weatherClass = "weather-snow";
    } else if (weatherCode >= 95 && weatherCode <= 99) {
        weatherClass = "weather-storm";
    } else {
        weatherClass = "weather-clear";
    }

    document.body.classList.add(weatherClass);

    if (weatherClass === "weather-rain") {
        createRainEffect();
    } else {
        removeRainEffect();
    }
}

function createRainEffect() {
    const background = document.getElementById("weather-background");

    const oldContainer = document.getElementById("rain-container");

    if (oldContainer) {
        oldContainer.remove();
    }

    const rainContainer = document.createElement("div");
    rainContainer.id = "rain-container";

    for (let i = 0; i < 120; i++) {
        const drop = document.createElement("div");

        drop.classList.add("rain-drop");

        const size = Math.random();

        drop.style.left = `${Math.random() * 100}%`;

        drop.style.width =
            `${1 + size * 2}px`;

        drop.style.height =
            `${12 + size * 32}px`;

        drop.style.opacity =
            `${0.15 + size * 0.6}`;

        drop.style.animationDuration =
            `${0.5 + Math.random() * 0.8}s`;

        drop.style.animationDelay =
            `${Math.random() * -2}s`;

        drop.style.setProperty(
            "--drift",
            `${-20 + Math.random() * 40}px`
        );

        drop.style.filter =
            `blur(${(1 - size) * 0.8}px)`;

        rainContainer.appendChild(drop);
    }

    background.appendChild(rainContainer);
}


function removeRainEffect() {
    const rainContainer =
        document.getElementById("rain-container");

    if (rainContainer) {
        rainContainer.remove();
    }
}
