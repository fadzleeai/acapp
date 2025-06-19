from flask import Flask, jsonify, request, render_template
from SREC_MODEL import FuzzyModel, IntentClassifier

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # looks inside /templates

@app.route("/mic", methods=["POST"])
def mic_route():
    model = FuzzyModel()
    clf = IntentClassifier()
    
    voice_text = clf.mic()
    temp = request.json.get("temp", 25)
    humidity = request.json.get("humidity", 50)

    result = model.calculate_fuzzy_output(voice_text, temp, humidity)
    return jsonify({
        "voice": voice_text,
        "temp": result[0],
        "fan": result[1]
    })

if __name__ == "__main__":
    app.run(debug=True)
