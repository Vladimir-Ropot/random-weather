async function getHistory() {
    const response = await fetch("/api/history");

    if (!response.ok) {
        throw new Error("Failed to fetch history");
    }

    return await response.json();
}


async function getWeather() {
    console.log("GET WEATHER: starting request");

    const response = await fetch("/api/weather", {
        signal: AbortSignal.timeout(10000)
    });

    console.log("GET WEATHER: response", response.status);

    if (!response.ok) {
        const errorData = await response.json();

        if (response.status === 503) {
            throw new Error("weatherServiceError");
        }

        throw new Error("weatherServiceError");
    }

    return await response.json();
}


async function addFavorite() {
    const response = await fetch("/api/favorites", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            city: currentWeather.city,
            country: currentWeather.country,
            latitude: currentWeather.latitude,
            longitude: currentWeather.longitude
        })
    });

    if (!response.ok) {
        throw new Error("Failed to add favorite");
    }

    return await response.json();
}


async function getFavorites() {
    const response = await fetch("/api/favorites");

    if (!response.ok) {
        throw new Error("Failed to fetch favorites");
    }

    return await response.json();
}

async function deleteFavorite(favoriteId) {
    const response = await fetch(`/api/favorites/${favoriteId}`, {
        method: "DELETE"
    });

    if (!response.ok) {
        throw new Error("Failed to delete favorite");
    }
}