import speech_recognition as sr

def listen_and_transcribe(save_to_file=True, file_path="transcription.txt"):
    """
    Listens to mic input, returns transcribed text.
    Optionally saves to file.
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Speak now...")
        r.adjust_for_ambient_noise(source)

        while True:
            print("Listening...")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                print("You said:", text)

                if save_to_file:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(text + "\n")

                return text  # Return text to caller

            except sr.UnknownValueError:
                print("❌ Could not understand. Try again...\n")
            except sr.RequestError:
                print("🚫 API unavailable.")
                return None
