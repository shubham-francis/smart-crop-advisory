from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# -----------------------------
# Load trained ML model
# -----------------------------
with open("crop_model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# Fertilizer Recommendation Logic
# -----------------------------
def recommend_fertilizer(N, P, K):
    recommendations = []

    if N < 50:
        recommendations.append("Urea (Nitrogen rich)")
    if P < 40:
        recommendations.append("DAP (Phosphorus rich)")
    if K < 40:
        recommendations.append("MOP (Potassium rich)")

    if not recommendations:
        return "Soil nutrients are balanced. No additional fertilizer required."
    else:
        return ", ".join(recommendations)

# -----------------------------
# Health check route (important)
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Backend is running",
        "message": "Smart Crop Advisory API"
    })

# -----------------------------
# Prediction API
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Read inputs from frontend
    N = data["N"]
    P = data["P"]
    K = data["K"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    ph = data["ph"]
    rainfall = data["rainfall"]

    # ML prediction
    input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    crop = model.predict(input_data)[0]

    # Fertilizer recommendation
    fertilizer = recommend_fertilizer(N, P, K)

    return jsonify({
        "recommended_crop": crop,
        "fertilizer": fertilizer
    })

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
