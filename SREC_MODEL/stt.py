import speech_recognition as sr

class SpeechTranscriber:
    def __init__(self, save_to_file=True, file_path="transcription.txt"):
        self.recognizer = sr.Recognizer()
        self.save_to_file = save_to_file
        self.file_path = file_path

    def transcribe(self):
        """
        Generator: yields mic status and transcription.
        """
        with sr.Microphone() as source:
            yield {"status": "mic_ready", "message": "Speak now..."}
            self.recognizer.adjust_for_ambient_noise(source)

            while True:
                yield {"status": "listening", "message": "Listening..."}
                audio = self.recognizer.listen(source)

                try:
                    text = self.recognizer.recognize_google(audio)
                    yield {"status": "transcribed", "text": text}

                    if self.save_to_file:
                        with open(self.file_path, "a", encoding="utf-8") as f:
                            f.write(text + "\n")

                    return  # Done after one transcription

                except sr.UnknownValueError:
                    yield {"status": "error", "message": "Could not understand. Try again..."}
                except sr.RequestError:
                    yield {"status": "error", "message": "API unavailable."}
                    return