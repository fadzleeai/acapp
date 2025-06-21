import pyttsx3

class TextToSpeech:
    def __init__(self):
        # only store config, NOT the engine
        self.voice_id = None
        self.rate = 160
        self.volume = 0.9

        # Find a female voice once
        temp_engine = pyttsx3.init()
        voices = temp_engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.id.lower():
                self.voice_id = voice.id
                break
        temp_engine.stop()

    def speak_adjustment(self, temperature, fan_speed):
        engine = pyttsx3.init()  # Re-init every time

        if self.voice_id:
            engine.setProperty('voice', self.voice_id)
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)

        if temperature < 0:
            temp_action = "lowering"
            temperature = abs(temperature)
        else:
            temp_action = "raising"

        text = f"{temp_action.capitalize()} the temperature by {temperature} degrees, and setting the fan speed to {fan_speed}."
        engine.say(text)
        engine.runAndWait()
        engine.stop()
