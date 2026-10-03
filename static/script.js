function displayError(errorKey) {
    city.textContent = 
        translations[currentLanguage][errorKey];

    country.textContent = "";
    temperature.textContent = "";
    wind.textContent = "";
    weather.textContent = "";
    time.textContent = "";
}


button.addEventListener("click", async function () {

    button.textContent = "Loading...";
    button.disabled = true;

    try {
        const data = await getWeather();
        currentWeather =data;

        const favorites = await getFavorites();

        const currentFavorite = favorites.find(
            (favorite) => favorite.city === currentWeather.city
        );

        favoriteButton.textContent = currentFavorite ? "❤️" : "⭐";

        const history = await getHistory();
        currentHistory = history;

        displayWeather(data);
        displayHistory(history);

    } catch (error) {

        console.error(error);

        displayError(error.message);

    } finally {
        button.textContent = "Get Weather";
        button.disabled = false;
    }
});


favoriteButton.addEventListener("click", async () => {
    if (!currentWeather) {
        return;
    }

    try {
        const favorites = await getFavorites();
        const currentFavorite = favorites.find(
            (favorite) => favorite.city === currentWeather.city
        );

        if (currentFavorite) {
            await deleteFavorite(currentFavorite.id);
            favoriteButton.textContent = "⭐"
        } else {
            await addFavorite();
            favoriteButton.textContent = "❤️";
        }
        await loadFavorites();
    } catch (error) {
        console.error(error);
    }
});


setLanguage(currentLanguage);
loadHistory();
loadFavorites();
