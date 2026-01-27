from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests

app = Flask(__name__)
CORS(app)


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
import requests

# To get weather data
def get_weather(lat, lon):
    API_KEY = "76fdf2bcd21a76d908f8aaeda66ada1e"
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url).json()

    temperature = response["main"]["temp"]
    humidity = response["main"]["humidity"]
    rainfall = response.get("rain", {}).get("1h", 0)

    return temperature, humidity, rainfall


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

    # Soil inputs
    N = data["N"]
    P = data["P"]
    K = data["K"]
    ph = data["ph"]

    # GPS coordinates from frontend
    lat = data["lat"]
    lon = data["lon"]

    # Fetch weather using GPS
    temperature, humidity, rainfall = get_weather(lat, lon)

    # ML prediction
    input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    crop = model.predict(input_data)[0]

    fertilizer = recommend_fertilizer(N, P, K)

    return jsonify({
        "recommended_crop": crop,
        "fertilizer": fertilizer,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        }
    })

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
