from flask import Flask, request, send_from_directory
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

# Serve the HTML file
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "browser_gps.html")

@app.route("/location", methods=["POST"])
def location():
    try:
        data = request.json
        lat = data.get("lat")
        lon = data.get("lon")

        if lat is None or lon is None:
            return {"error": "Missing latitude or longitude"}, 400

        api_key = "970ad40aaeb614d797e5beafba12002a"
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        weather = response.json()

        return weather, 200
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
