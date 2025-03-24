from flask import Flask, request, jsonify
import joblib
import numpy as np
from transformers import pipeline

app = Flask(__name__)

# Load the trained churn model (ensure train_churn_model.py has been run)
model = joblib.load("model.joblib")

# Initialize a generative text pipeline with a lightweight model
generator = pipeline('text-generation', model='distilgpt2')

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        features = np.array([[float(data['feature1']), float(data['feature2']), float(data['feature3'])]])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input. Provide feature1, feature2, and feature3 as numbers."}), 400

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].tolist()
    return jsonify({
        "churn_prediction": int(prediction),
        "probabilities": probability
    })

@app.route("/recommend", methods=["GET"])
def recommend():
    recommendations = [
        {"product": "Square POS System", "reason": "Enhance in-store payments"},
        {"product": "Square Online Store", "reason": "Expand your online presence"},
        {"product": "Square Appointments", "reason": "Streamline booking management"}
    ]
    return jsonify(recommendations)

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    generated = generator(prompt, max_length=50, num_return_sequences=1)
    return jsonify(generated[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
