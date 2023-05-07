var countries = [
  { name: "Country 1", souvenirs: 0, emissions: 1000 },
  { name: "Country 2", souvenirs: 0, emissions: 1500 },
  { name: "Country 3", souvenirs: 0, emissions: 2000 },
  { name: "Country 4", souvenirs: 0, emissions: 800 },
  { name: "Country 5", souvenirs: 0, emissions: 1200 },
  { name: "Country 6", souvenirs: 0, emissions: 1800 },
  { name: "Country 7", souvenirs: 0, emissions: 1300 }
];

var currentCountryIndex = 0;
var totalEmissions = 0;

function travelToNextCountry() {
  // Update emissions
  totalEmissions += countries[currentCountryIndex].emissions;

  // Check if emissions exceed the limit
  if (totalEmissions > 10000) {
    alert("Game over! You exceeded the carbon dioxide emissions limit.");
    resetGame();
    return;
  }

  // Update souvenirs
  countries[currentCountryIndex].souvenirs++;

  // Display country name, souvenirs, and emissions
  document.getElementById("countryName").innerHTML = "Country: " + countries[currentCountryIndex].name;
  document.getElementById("souvenirs").innerHTML = "Souvenirs collected: " + countries[currentCountryIndex].souvenirs;
  document.getElementById("emissions").innerHTML = "Total emissions: " + totalEmissions;

  // Check if all countries have been visited
  if (currentCountryIndex === countries.length - 1) {
    alert("Congratulations! You visited all seven countries.");
    resetGame();
    return;
  }

  // Move to the next country
  currentCountryIndex++;
}

function resetGame() {
  currentCountryIndex = 0;
  totalEmissions = 0;
  document.getElementById("countryName").innerHTML = "";
  document.getElementById("souvenirs").innerHTML = "";
  document.getElementById("emissions").innerHTML = "";
}
