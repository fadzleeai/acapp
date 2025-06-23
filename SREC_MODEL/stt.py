import speech_recognition as sr

def listen_and_transcribe(save_to_file=True, file_path="transcription.txt"):
    """
    Generator: yields mic status and transcription.
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        yield {"status": "mic_ready", "message": "🎤 Speak now..."}
        r.adjust_for_ambient_noise(source)

        while True:
            yield {"status": "listening", "message": "Listening..."}
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                yield {"status": "transcribed", "text": text}

                if save_to_file:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(text + "\n")

                return  # Done after one transcription

            except sr.UnknownValueError:
                yield {"status": "error", "message": "Could not understand. Try again..."}
            except sr.RequestError:
                yield {"status": "error", "message": "API unavailable."}
                return