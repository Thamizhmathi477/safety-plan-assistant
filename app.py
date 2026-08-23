import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
import joblib

# -----------------------------
# Load and train model (cached)
# -----------------------------
@st.cache_resource
def load_model_and_preprocessors():
    # Load dataset (assumed to be in the same folder)
    df = pd.read_csv('Student Depression Dataset.csv')
    
    # Rename and encode
    df.rename(columns={'Have you ever had suicidal thoughts ?': 'Suicidal_Thoughts'}, inplace=True)
    df['Suicidal_Thoughts'] = df['Suicidal_Thoughts'].map({'Yes': 1, 'No': 0})
    
    categorical_cols = [
        'Gender', 'City', 'Profession', 'Sleep Duration',
        'Dietary Habits', 'Degree', 'Family History of Mental Illness'
    ]
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
    
    # Feature columns
    features = [
        'Gender', 'Age', 'Academic Pressure', 'CGPA', 'Study Satisfaction',
        'Work/Study Hours', 'Financial Stress', 'Suicidal_Thoughts',
        'Sleep Duration', 'Dietary Habits'
    ]
    X = df[features]
    y = df['Depression']
    
    # Impute and scale
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)
    
    # Train Logistic Regression (best model from your analysis)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler, imputer, label_encoders, features

# -----------------------------
# Load once and cache
# -----------------------------
model, scaler, imputer, encoders, feature_names = load_model_and_preprocessors()

# -----------------------------
# App UI
# -----------------------------
st.set_page_config(page_title="MindGuard – Student Depression Risk", layout="wide")

st.title("🧠 MindGuard: Student Mental Health Risk Assessment")
st.markdown("""
Enter your details below to get a **personalised risk score** and actionable advice.
*This is a screening tool, not a medical diagnosis.*
""")

with st.form("risk_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", 18, 60, 22, step=1)
        academic_pressure = st.slider("Academic Pressure (0-5)", 0, 5, 3)
        cgpa = st.slider("CGPA", 5.0, 10.0, 7.5, step=0.01)
        study_satisfaction = st.slider("Study Satisfaction (0-5)", 0, 5, 3)
    with col2:
        study_hours = st.number_input("Work/Study Hours per day", 0, 15, 5, step=1)
        sleep = st.selectbox("Sleep Duration", ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"])
        suicidal = st.selectbox("Have you ever had suicidal thoughts?", ["No", "Yes"])
        financial_stress = st.slider("Financial Stress (1-5)", 1, 5, 3)
        dietary = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
    
    submitted = st.form_submit_button("Assess My Risk")

if submitted:
    # Encode inputs using the same encoders
    gender_enc = encoders['Gender'].transform([gender])[0]
    sleep_enc = encoders['Sleep Duration'].transform([sleep])[0]
    dietary_enc = encoders['Dietary Habits'].transform([dietary])[0]
    suicidal_enc = 1 if suicidal == "Yes" else 0
    
    # Build input array
    input_data = np.array([[
        gender_enc,
        age,
        academic_pressure,
        cgpa,
        study_satisfaction,
        study_hours,
        financial_stress,
        suicidal_enc,
        sleep_enc,
        dietary_enc
    ]])
    
    # Impute and scale
    input_imputed = imputer.transform(input_data)
    input_scaled = scaler.transform(input_imputed)
    
    # Predict
    proba = model.predict_proba(input_scaled)[0][1]
    risk_score = int(proba * 100)
    
    # Display risk
    st.subheader(f"🔄 Risk Score: **{risk_score}%**")
    
    if risk_score >= 70:
        st.error("🔴 **High Risk** – Please consult a mental health professional as soon as possible.")
    elif risk_score >= 40:
        st.warning("🟡 **Moderate Risk** – Monitor your well‑being and consider talking to a counselor.")
    else:
        st.success("🟢 **Low Risk** – Keep up healthy habits and maintain a balanced lifestyle.")
    
    # Personalised recommendations
    st.subheader("💡 Personalised Recommendations")
    recs = []
    if academic_pressure >= 4:
        recs.append("📘 Reduce academic load – talk to your advisor about balancing your courses.")
    if cgpa < 6.0:
        recs.append("📚 Consider academic support like tutoring or study groups.")
    if study_satisfaction <= 2:
        recs.append("😊 Try to find more enjoyment in your studies – join a study group or explore topics you're passionate about.")
    if study_hours > 8:
        recs.append("⏰ Limit study/working hours to ≤8 hours per day; take regular breaks.")
    if sleep in ["Less than 5 hours", "5-6 hours"]:
        recs.append("🛌 Aim for 7-8 hours of sleep – it’s crucial for mental health.")
    if financial_stress >= 4:
        recs.append("💰 Seek financial aid or counselling to manage financial stress.")
    if suicidal == "Yes":
        recs.append("📞 You are not alone – please reach out to a mental health hotline immediately.")
    if dietary == "Unhealthy":
        recs.append("🥗 Improve your diet – eat regular, balanced meals to support your mental health.")
    
    if recs:
        for r in recs:
            st.write(r)
    else:
        st.write("You’re doing well! Keep maintaining your healthy routine.")

st.markdown("---")
st.caption("Disclaimer: This tool is for educational and screening purposes only. Please seek professional help for any mental health concerns.")
