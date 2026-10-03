function displayHistory(history) {
    const historyContainer = document.getElementById("history");

    historyContainer.innerHTML = 
        `<h2>${translations[currentLanguage].history}</h2>`;

    history.forEach((item, index) => {
        const historyItem = document.createElement("div");
        historyItem.classList.add("history-item");

        historyItem.innerHTML = `
            <p>${item.city}, ${item.country}</p>
            <p>
                ${translations[currentLanguage].temperature}:
                ${convertTemperature(item.temperature).toFixed(1)}
                °${currentUnit}
            </p>
            <p>${translations[currentLanguage].wind}: ${item.wind_speed} km/h</p>
            <p>${weatherTranslations[currentLanguage][item.weather] || item.weather}</p>
            <p>${translations[currentLanguage].time}: ${formatDate(item.created_at)}</p>
        `;
        historyContainer.appendChild(historyItem);

        if (index < history.length -1) {
            const separator = document.createElement("hr");
            historyContainer.appendChild(separator)
        }

    });
}


function formatDate(dateString) {
    const date = new Date(dateString);

    return date.toLocaleString(
        currentLanguage === "ru" ? "ru-RU" : "en-US"
    );
}


async function loadHistory() {
    try {
        const history = await getHistory();
        currentHistory = history;
        displayHistory(history);
    } catch (error) {
        console.error(error);
    }
}