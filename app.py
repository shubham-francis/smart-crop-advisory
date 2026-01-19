import streamlit as st
import pickle
import numpy as np

# Load trained model
with open("crop_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Smart Crop Advisory", page_icon="🌾")

st.title("🌾 Smart Crop Advisory System")
st.write("Enter soil and climate details to get the best crop recommendation.")

# Input fields
N = st.number_input("Nitrogen (N)", min_value=0.0)
P = st.number_input("Phosphorus (P)", min_value=0.0)
K = st.number_input("Potassium (K)", min_value=0.0)

temp = st.number_input("Temperature (°C)", min_value=0.0)
humidity = st.number_input("Humidity (%)", min_value=0.0)
ph = st.number_input("Soil pH", min_value=0.0)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0)

# Predict button
if st.button("Get Crop Recommendation 🌱"):
    input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    result = model.predict(input_data)

    st.success(f"✅ Recommended Crop: **{result[0].upper()}**")
