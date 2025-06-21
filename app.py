from flask import Flask, request, Response, stream_with_context, render_template
from SREC_MODEL import FuzzyModel, IntentClassifier, SpeechTranscriber, TextToSpeech
import json, threading

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mic-stream", methods=["GET"])
def mic_stream():
    model = FuzzyModel()
    clf = IntentClassifier()
    tts = TextToSpeech()
    temp = int(request.args.get("temp", 25))
    humidity = int(request.args.get("humidity", 50))

    def generate():
        transcriber = SpeechTranscriber()
        for update in transcriber.transcribe():
            if update.get("status") == "transcribed":
                voice_text = update["text"]
                comfort = clf.classify_text(voice_text)
                result = model.calculate_fuzzy_output(comfort, temp, humidity)
                update.update({
                    "comfort": comfort,
                    "temp": result[0],
                    "fan": result[1],
                    "status": "done"
                })
                threading.Thread(target=tts.speak_adjustment, args=(result[0], result[1]), daemon=True).start()
            yield f"data: {json.dumps(update)}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)