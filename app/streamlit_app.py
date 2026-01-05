import pickle
import pandas as pd
import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Titanic Survival Prediction",
    page_icon="🚢",
    layout="centered"
)

st.title("🚢 Titanic Survival Prediction")
st.write("Predict passenger survival using a trained ML model")

# -----------------------------
# Load trained model
# -----------------------------
@st.cache_resource
def load_model():
    with open("model/titanic_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# -----------------------------
# User Inputs
# -----------------------------
st.subheader("Passenger Details")

pclass = st.selectbox("Passenger Class", [1, 2, 3])
sex = st.selectbox("Gender", ["Male", "Female"])
age = st.slider("Age", min_value=1, max_value=80, value=30)
fare = st.number_input("Fare Paid", min_value=0.0, max_value=600.0, value=50.0)
family_size = st.slider("Family Size", min_value=1, max_value=10, value=1)

sex_value = 0 if sex == "Male" else 1

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Survival 🚀"):
    input_df = pd.DataFrame([{
        "Pclass": pclass,
        "Sex": sex_value,
        "Age": age,
        "Fare": fare,
        "FamilySize": family_size
    }])

    prediction = model.predict(input_df)[0]

    st.markdown("---")
    if prediction == 1:
        st.success("🎉 Passenger is likely to SURVIVE")
    else:
        st.error("❌ Passenger is NOT likely to survive")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with Machine Learning, Kafka & Streamlit")
