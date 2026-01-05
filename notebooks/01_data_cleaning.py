import os
import pandas as pd

# -----------------------------
# Create required directories
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/raw/train.csv")

# -----------------------------
# Handle missing values (NO inplace)
# -----------------------------
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df['Fare'] = df['Fare'].fillna(df['Fare'].median())

# -----------------------------
# Feature Engineering
# -----------------------------
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# -----------------------------
# Save cleaned dataset
# -----------------------------
df.to_csv("data/processed/cleaned_titanic.csv", index=False)

print("✅ cleaned_titanic.csv successfully saved in data/processed/")
