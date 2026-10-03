function setLanguage(language) {
    currentLanguage = language;
    localStorage.setItem("language", language);
    
    button.textContent = 
        translations[language].getWeather;

    if (currentWeather) {
        displayWeather(currentWeather);
    }

    if (currentHistory.length > 0) {
        displayHistory(currentHistory);
    }
}


langRU.addEventListener("click", () => {
    setLanguage("ru");
});


langEN.addEventListener("click", () => {
    setLanguage("en");
});


unitCelsius.addEventListener("click", () => {
    currentUnit = "C";
    localStorage.setItem("unit", "C");

    if (currentWeather) {
        displayWeather(currentWeather);
    }

    if (currentHistory.length > 0) {
        displayHistory(currentHistory);
    }
});


unitFahrenheit.addEventListener("click", () => {
    currentUnit = "F";
    localStorage.setItem("unit", "F");

    if (currentWeather) {
        displayWeather(currentWeather);
    }

    if (currentHistory.length > 0) {
        displayHistory(currentHistory);
    }
});
