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
  statusText.textContent = "Initializing mic...";

  // First: Get slider values
  const temp = parseInt(tempSlider.value);
  const humidity = parseInt(humSlider.value);

  // Create a dynamic SSE request using query parameters (since EventSource only supports GET)
  const url = `/mic-stream?temp=${temp}&humidity=${humidity}`;
  const evtSource = new EventSource(url);

  evtSource.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.status === "mic_ready") {
      statusText.textContent = data.message; // Speak now...
    } else if (data.status === "listening") {
      statusText.textContent = data.message; // Listening...
    } else if (data.status === "transcribed") {
      statusText.textContent = "Transcribed. Running fuzzy logic...";
    } else if (data.status === "done") {
      statusText.textContent = "Result received!";
      voiceResult.textContent = `"${data.text}"`;
      acTemp.textContent = `${data.temp.toFixed(1)}°C`;
      fanSpeed.textContent = `${data.fan * 20}%`;

      micIcon.classList.remove("text-red-400");
      micIcon.classList.add("text-orange-600");
      wave.classList.add("hidden");
      evtSource.close(); // 🔚 Done
    } else if (data.status === "error") {
      statusText.textContent = data.message;
      micIcon.classList.remove("text-red-400");
      micIcon.classList.add("text-orange-600");
      wave.classList.add("hidden");
      evtSource.close();
    }
  };
});


tempSlider.addEventListener("input", () => {
  tempVal.textContent = tempSlider.value;
});

humSlider.addEventListener("input", () => {
  humVal.textContent = humSlider.value;
});
