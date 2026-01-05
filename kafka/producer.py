import json
import time
import pandas as pd
from kafka import KafkaProducer

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load test data (NO Survived column)
df = pd.read_csv("data/raw/test.csv")

# Basic preprocessing (same as training)
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Fare'] = df['Fare'].fillna(df['Fare'].median())
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

print("🚀 Streaming passenger data to Kafka...")

for _, row in df.iterrows():
    message = {
        "Pclass": int(row["Pclass"]),
        "Sex": int(row["Sex"]),
        "Age": float(row["Age"]),
        "Fare": float(row["Fare"]),
        "FamilySize": int(row["FamilySize"])
    }

    producer.send("titanic_topic", message)
    print("Sent:", message)
    time.sleep(1)

producer.close()
