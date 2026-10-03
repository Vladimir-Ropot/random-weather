const favoritesToggle = document.getElementById("favorites-toggle");
const favoritesClose = document.getElementById("favorites-close");
const favoritesPanel = document.getElementById("favorites");


function displayFavorites(favorites) {
    const favoritesContainer = document.getElementById("favorites-list");

    favoritesContainer.innerHTML = "";

    favorites.forEach((favorite) => {
        const favoriteItem = document.createElement("div");

        favoriteItem.classList.add("favorite-item");

        favoriteItem.innerHTML = `
            <div>
                <span>${favorite.city}, ${favorite.country}</span>
                <button class="favorite-delete">×</button>
            </div>
        `;

        const deleteButton = favoriteItem.querySelector(".favorite-delete");

        deleteButton.addEventListener("click", async (event) => {
            event.stopPropagation();

            try {
                await deleteFavorite(favorite.id);
                await loadFavorites();
            } catch (error) {
                console.error(error);
            }
        });

        favoriteItem.addEventListener("click", () => {
            console.log("Selected favorites", favorite);
        });

        favoritesContainer.appendChild(favoriteItem);
    });
}


favoritesToggle.addEventListener("click", () => {
    favoritesPanel.classList.add("open")
})


favoritesClose.addEventListener("click", () => {
    favoritesPanel.classList.remove("open")
})


async function loadFavorites() {
    try {
        const favorites = await getFavorites();

        console.log("FAVORITES", favorites);

        displayFavorites(favorites);
    } catch (error) {
        console.error(error)
    }
}