from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import traceback 

app = Flask(__name__)
CORS(app)

# ---- Load your trained model pipeline ----
MODEL_PATH = "model.joblib"
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Loaded model from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400

        # Predict using your trained pipeline
        prediction = model.predict([text])[0]
        probas = model.predict_proba([text])[0]
        confidence = float(max(probas))

        # Optional: Simple sentiment estimation from text (demo)
        sentiment = "Negative" if any(w in text.lower() for w in ["sad", "hopeless", "tired"]) else "Neutral"

        return jsonify({
            "label": str(prediction),
            "confidence": confidence,
            "sentiment": sentiment
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)