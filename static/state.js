const button = document.getElementById("weather-button");

const langRU = document.getElementById("lang-ru");
const langEN = document.getElementById("lang-en");

const unitCelsius = document.getElementById("unit-celsius");
const unitFahrenheit = document.getElementById("unit-fahrenheit");

const favoriteButton = document.getElementById("favorite-button");

const city = document.getElementById("city");
const country = document.getElementById("country");
const temperature = document.getElementById("temperature");
const weather = document.getElementById("weather");
const wind = document.getElementById("wind");
const time = document.getElementById("time");

let currentLanguage = localStorage.getItem("language") || "en";
let currentWeather = null;
let currentHistory = [];
let currentUnit = localStorage.getItem("unit") || "C";