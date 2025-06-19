// main.js

const micBtn = document.getElementById("micBtn");
const micIcon = document.getElementById("micIcon");
const wave = document.getElementById("wave");
const statusText = document.getElementById("statusText");

const tempSlider = document.getElementById("tempSlider");
const humSlider = document.getElementById("humSlider");
const tempVal = document.getElementById("tempVal");
const humVal = document.getElementById("humVal");

const voiceResult = document.getElementById("voiceResult");
const acTemp = document.getElementById("acTemp");
const fanSpeed = document.getElementById("fanSpeed");

micBtn.addEventListener("click", async () => {
  micIcon.classList.add("text-red-400");
  micIcon.classList.remove("text-orange-600");
  wave.classList.remove("hidden");
  statusText.textContent = "Listening...";

  try {
    const response = await fetch("/mic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        temp: parseInt(tempSlider.value),
        humidity: parseInt(humSlider.value)
      })
    });

    const data = await response.json();

    voiceResult.textContent = `"${data.voice}"`;
    acTemp.textContent = `${data.temp.toFixed(1)}°C`;
    fanSpeed.textContent = `${data.fan * 20}%`;

    statusText.textContent = "Result received!";
  } catch (error) {
    console.error("Mic error:", error);
    statusText.textContent = "Error processing voice input.";
  }

  micIcon.classList.remove("text-red-400");
  micIcon.classList.add("text-orange-600");
  wave.classList.add("hidden");
});

tempSlider.addEventListener("input", () => {
  tempVal.textContent = tempSlider.value;
});

humSlider.addEventListener("input", () => {
  humVal.textContent = humSlider.value;
});
