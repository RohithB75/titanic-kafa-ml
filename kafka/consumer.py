import json
import pickle
import pandas as pd
from kafka import KafkaConsumer

# -----------------------------
# Load trained ML model
# -----------------------------
with open("model/titanic_model.pkl", "rb") as f:
    model = pickle.load(f)

print("✅ Model loaded successfully")

# -----------------------------
# Kafka Consumer Configuration
# -----------------------------
consumer = KafkaConsumer(
    "titanic_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",      # read from beginning if no offset
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("📥 Listening for passenger data...")

# -----------------------------
# Consume messages & predict
# -----------------------------
for msg in consumer:
    data = msg.value

    # Convert incoming JSON to DataFrame (BEST PRACTICE)
    input_df = pd.DataFrame([{
        "Pclass": data["Pclass"],
        "Sex": data["Sex"],
        "Age": data["Age"],
        "Fare": data["Fare"],
        "FamilySize": data["FamilySize"]
    }])

    # Predict survival
    prediction = model.predict(input_df)[0]

    result = "SURVIVED 🎉" if prediction == 1 else "NOT SURVIVED ❌"
    print(f"🧠 Prediction → {result}")
