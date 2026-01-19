import pickle

# Load trained model
with open("crop_model.pkl", "rb") as file:
    model = pickle.load(file)

# Sample input: N, P, K, Temp, Humidity, pH, Rainfall
sample = [[90, 42, 43, 20.5, 80, 6.5, 200]]

prediction = model.predict(sample)

print("Recommended Crop:", prediction[0])
