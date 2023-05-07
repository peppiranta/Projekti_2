var attractions = [
  { name: "Colosseum", country: "Italy", code: "LIRF", souvenir: "Fridge Magnet" },
  { name: "Great Barrier Reef", country: "Australia", code: "YBMKY", souvenir: "Boomerang" },
  { name: "Teotihuacan", country: "Mexico", code: "MMSM", souvenir: "Wooden Pyramid Ornament" },
  { name: "Northern Lights in Rovaniemi", country: "Finland", code: "EFRO", souvenir: "Snowflake Reflector" },
  { name: "Taj Mahal", country: "India", code: "VIAG", souvenir: "Miniature Elephant Statue" },
  { name: "Christ the Redeemer", country: "Brazil", code: "SBRJ", souvenir: "Mini Christ Statue" },
  { name: "Victoria Falls", country: "Zambia", code: "FLLI", souvenir: "Glass Water Drop" }
];

var currentAttractionIndex = 0;
var totalEmissions = 0;

var gameContainer = document.getElementById("game-container");
var gameMessage = document.getElementById("game-message");
var nextButton = document.getElementById("next-button");

nextButton.addEventListener("click", function() {
  if (currentAttractionIndex === attractions.length) {
    endGame();
    return;
  }
  if (currentAttractionIndex === 0) {
    displayWelcomeMessage();
  } else {
    displayAttractionMessage();
  }
  currentAttractionIndex++;
});

function displayWelcomeMessage() {
  gameMessage.innerHTML = "Welcome to The Seven Wonders game! Your objective is to visit seven wonders while minimizing your carbon dioxide emissions. Let's start the game!";
}

function displayAttractionMessage() {
  var currentAttraction = attractions[currentAttractionIndex - 1];
  var attractionName = currentAttraction.name;
  var countryName = currentAttraction.country;
  var emissions = Math.random() * 0.2 + 0.1;
  totalEmissions += emissions;
  var transportOptions = ["Taxi", "Hiking", "Walking"];
  var transportIndex = Math.floor(Math.random() * transportOptions.length);
  var chosenTransport = transportOptions[transportIndex];
  var transportEmissions = 0;
  var souvenir = currentAttraction.souvenir;

  if (
