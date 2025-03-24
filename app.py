from flask import Flask, request, jsonify
import joblib
import numpy as np
from transformers import pipeline, GenerationConfig

app = Flask(__name__)

# Load the trained churn model (ensure train_churn_model.py has been run)
model = joblib.load("model.joblib")

# Initialize a generative text pipeline with a lightweight model
generator = pipeline('text-generation', model='distilgpt2')

# Define a generation configuration
generation_config = GenerationConfig(
    max_length=50,
    temperature=0.1,  # Further reduce randomness
    top_p=0.98,       # Focus even more on the most probable words
    pad_token_id=50256  # Ensure proper padding
)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Square ML Demo API!",
        "endpoints": {
            "POST /predict": "Predict churn based on feature1, feature2, and feature3.",
            "GET /recommend": "Get product recommendations.",
            "POST /generate": "Generate text based on a prompt."
        }
    })

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

    # Use the generation configuration
    generated = generator(prompt, generation_config=generation_config)

    # Post-process the generated text to remove excessive newlines
    cleaned_text = generated[0]["generated_text"].replace("\n", " ").strip()

    return jsonify({"generated_text": cleaned_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Ensure the app listens on all interfaces
