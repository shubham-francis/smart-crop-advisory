from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import requests

app = FastAPI(
    title="Smart Crop Advisory API",
    description="Crop & Fertilizer Recommendation using ML + GPS Weather",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load trained ML model
# -----------------------------
with open("crop_model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# Input schema (auto validation)
# -----------------------------
class CropInput(BaseModel):
    lat: float
    lon: float
    N: float
    P: float
    K: float
    ph: float

# -----------------------------
# Fertilizer Recommendation
# -----------------------------
def recommend_fertilizer(N, P, K):
    rec = []
    if N < 50:
        rec.append("Urea (Nitrogen rich)")
    if P < 40:
        rec.append("DAP (Phosphorus rich)")
    if K < 40:
        rec.append("MOP (Potassium rich)")
    return ", ".join(rec) if rec else "Soil nutrients are balanced"

# -----------------------------
# Weather using GPS
# -----------------------------
def get_weather(lat, lon):
    API_KEY = "76fdf2bcd21a76d908f8aaeda66ada1e"  # 🔑 put your key here

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    data = requests.get(url, timeout=10).json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temperature, humidity, rainfall

# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "Backend running",
        "framework": "FastAPI",
        "message": "Smart Crop Advisory API"
    }

# -----------------------------
# Prediction API
# -----------------------------
@app.post("/predict")
def predict(data: CropInput):
    temperature, humidity, rainfall = get_weather(data.lat, data.lon)

    input_data = np.array([[
        data.N,
        data.P,
        data.K,
        temperature,
        humidity,
        data.ph,
        rainfall
    ]])

    crop = model.predict(input_data)[0]
    fertilizer = recommend_fertilizer(data.N, data.P, data.K)

    return {
        "recommended_crop": crop,
        "fertilizer": fertilizer,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        }
    }
