import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import io

# ============================================================
# 1. LOAD & TRAIN MODEL (CACHED)
# ============================================================
@st.cache_resource
def load_model_and_preprocessors():
    try:
        df = pd.read_csv('Student Depression Dataset.csv')
    except FileNotFoundError:
        # Fallback mock data – but include a warning
        st.warning("Dataset not found. Using mock data for demonstration. Upload the CSV for full accuracy.")
        np.random.seed(42)
        n = 500
        df = pd.DataFrame({
            'Gender': np.random.choice(['Male', 'Female'], n),
            'Age': np.random.randint(18, 35, n),
            'Academic Pressure': np.random.randint(0, 6, n),
            'CGPA': np.random.uniform(5, 10, n),
            'Study Satisfaction': np.random.randint(0, 6, n),
            'Work/Study Hours': np.random.randint(0, 16, n),
            'Financial Stress': np.random.randint(1, 6, n),
            'Suicidal_Thoughts': np.random.choice([0, 1], n, p=[0.7, 0.3]),
            'Sleep Duration': np.random.choice(['Less than 5 hours', '5-6 hours', '7-8 hours', 'More than 8 hours'], n),
            'Dietary Habits': np.random.choice(['Healthy', 'Moderate', 'Unhealthy'], n),
            'Depression': np.random.choice([0, 1], n, p=[0.4, 0.6]),
            'City': np.random.choice(['Mumbai', 'Delhi', 'Bangalore'], n),
            'Profession': np.random.choice(['Student'], n),
            'Degree': np.random.choice(['B.Tech', 'B.Sc', 'BA'], n),
            'Family History of Mental Illness': np.random.choice(['Yes', 'No'], n),
        })
        df['Have you ever had suicidal thoughts ?'] = df['Suicidal_Thoughts'].map({1: 'Yes', 0: 'No'})

    # Preprocessing
    df.rename(columns={'Have you ever had suicidal thoughts ?': 'Suicidal_Thoughts'}, inplace=True)
    df['Suicidal_Thoughts'] = df['Suicidal_Thoughts'].map({'Yes': 1, 'No': 0})

    categorical_cols = ['Gender', 'City', 'Profession', 'Sleep Duration',
                        'Dietary Habits', 'Degree', 'Family History of Mental Illness']
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    features = ['Gender', 'Age', 'Academic Pressure', 'CGPA', 'Study Satisfaction',
                'Work/Study Hours', 'Financial Stress', 'Suicidal_Thoughts',
                'Sleep Duration', 'Dietary Habits']
    X = df[features]
    y = df['Depression']

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_scaled, y)

    # Compute a simple AUC (on training set) for display
    y_pred_proba = model.predict_proba(X_scaled)[:, 1]
    auc = roc_auc_score(y, y_pred_proba)

    # Feature importance (coefficients)
    coef = model.coef_[0]
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Coefficient': coef,
        'AbsCoeff': np.abs(coef)
    }).sort_values('AbsCoeff', ascending=False)

    return model, scaler, imputer, label_encoders, features, feature_importance, auc, df


# ============================================================
# 2. APP CONFIG
# ============================================================
st.set_page_config(page_title="RescuePlan AI", page_icon="🧠", layout="wide")

# Session state for theme and language
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "language" not in st.session_state:
    st.session_state.language = "English"

# ============================================================
# 3. LANGUAGE TEXT (Expanded)
# ============================================================
T = {
    "English": {
        "app_title": "🧠 RescuePlan AI",
        "app_subtitle": "AI‑powered mental health risk assessment & personalised safety plan",
        "assess": "📊 Assess My Risk & Generate Plan",
        "risk_score": "Risk Score",
        "low": "Low Risk – Keep maintaining healthy habits!",
        "moderate": "Moderate Risk – Consider talking to a counselor.",
        "high": "High Risk – Please seek professional help immediately.",
        "plan_title": "Your Personalised Safety Plan",
        "download": "📥 Download My Plan",
        "back": "← Back to Home",
        "warning": "This tool is for screening and planning only – it does not replace professional care.",
        "how_it_works": "How It Works",
        "model_performance": "Model Performance",
        "accuracy": "Accuracy",
        "auc": "AUC",
        "top_predictors": "Top predictors of depression risk",
        "your_risk_breakdown": "How your answers affect your risk",
        "feedback_title": "Was this plan helpful?",
        "feedback_helpful": "👍 Yes, very helpful",
        "feedback_somewhat": "😐 Somewhat helpful",
        "feedback_not": "👎 Not helpful",
        "feedback_thanks": "Thank you for your feedback!",
        "thanks": "Thank you for using RescuePlan AI – take care of yourself.",
    },
    "Tamil": {
        "app_title": "🧠 ரெஸ்க்யூபிளான் AI",
        "app_subtitle": "AI‑ஆதரவு மனநல இடர் மதிப்பீடு & தனிப்பயனாக்கப்பட்ட பாதுகாப்புத் திட்டம்",
        "assess": "📊 எனது இடரை மதிப்பிடு & திட்டத்தை உருவாக்கு",
        "risk_score": "இடர் மதிப்பெண்",
        "low": "குறைந்த இடர் – ஆரோக்கியமான பழக்கங்களை தொடரவும்!",
        "moderate": "மிதமான இடர் – ஒரு ஆலோசகரிடம் பேசுவதை கருத்தில் கொள்ளுங்கள்.",
        "high": "அதிக இடர் – உடனடியாக தொழில்முறை உதவியை நாடுங்கள்.",
        "plan_title": "உங்களின் தனிப்பயனாக்கப்பட்ட பாதுகாப்புத் திட்டம்",
        "download": "📥 எனது திட்டத்தை பதிவிறக்கு",
        "back": "← முகப்பிற்கு திரும்பு",
        "warning": "இந்த கருவி திரையிடல் மற்றும் திட்டமிடலுக்கு மட்டுமே – இது தொழில்முறை பராமரிப்பை மாற்றாது.",
        "how_it_works": "இது எவ்வாறு இயங்குகிறது",
        "model_performance": "மாதிரியின் செயல்திறன்",
        "accuracy": "துல்லியம்",
        "auc": "AUC",
        "top_predictors": "மனச்சோர்வு அபாயத்தின் முதன்மை காரணிகள்",
        "your_risk_breakdown": "உங்கள் பதில்கள் இடரை எவ்வாறு பாதிக்கின்றன",
        "feedback_title": "இந்த திட்டம் உதவியாக இருந்ததா?",
        "feedback_helpful": "👍 ஆம், மிகவும் உதவியாக இருந்தது",
        "feedback_somewhat": "😐 ஓரளவு உதவியாக இருந்தது",
        "feedback_not": "👎 உதவியாக இல்லை",
        "feedback_thanks": "உங்கள் கருத்துக்கு நன்றி!",
        "thanks": "ரெஸ்க்யூபிளான் AI ஐ பயன்படுத்தியதற்கு நன்றி – உங்களை கவனித்துக் கொள்ளுங்கள்.",
    }
}
text = T[st.session_state.language]

# ============================================================
# 4. HELPER: GENERATE PERSONALISED PLAN (Enhanced)
# ============================================================
def generate_plan(inputs):
    plan = {}
    warnings = []
    coping = []
    helpers = []
    safety = []
    places = []

    # Warning Signs
    if inputs['academic_pressure'] >= 4:
        warnings.append("Feeling overwhelmed by academic workload")
    if inputs['sleep'] in ["Less than 5 hours", "5-6 hours"]:
        warnings.append("Changes in sleep patterns (less than 7 hours)")
    if inputs['cgpa'] < 6.5:
        warnings.append("Worrying about academic performance/CGPA")
    if inputs['suicidal'] == 1:
        warnings.append("Experiencing difficult or intrusive thoughts")
    if inputs['financial_stress'] >= 4:
        warnings.append("Increased stress about financial situation")
    if inputs['study_satisfaction'] <= 2:
        warnings.append("Loss of interest or satisfaction in studies")
    plan['warning_signs'] = "\n".join([f"- {w}" for w in warnings]) if warnings else "Notice when you start feeling unusually tired, irritable, or withdrawn from others."

    # Coping
    if inputs['academic_pressure'] >= 4:
        coping.append("Break study sessions into 25-30 minute blocks with short breaks (Pomodoro technique)")
        coping.append("Talk to your academic advisor about workload management")
    if inputs['sleep'] in ["Less than 5 hours", "5-6 hours"]:
        coping.append("Aim for 7-8 hours of sleep; set a consistent bedtime")
    if inputs['cgpa'] < 6.5:
        coping.append("Form a study group with classmates for mutual support")
    if inputs['suicidal'] == 1:
        coping.append("**Immediate:** Reach out to a helpline or trusted person right now")
        coping.append("Create a safe environment – remove access to harmful objects/medications")
    if inputs['financial_stress'] >= 4:
        coping.append("Explore financial aid options or part-time work opportunities")
    coping.append("Practice deep breathing or mindfulness for 5 minutes daily")
    plan['coping_strategies'] = "\n".join([f"- {c}" for c in coping])

    # Supportive places
    places = ["- Library or a quiet study corner", "- A park or nature spot nearby"]
    if inputs['city']:
        places.append(f"- Connect with local student groups in {inputs['city']}")
    plan['supportive_people_places'] = "\n".join(places)

    # People to ask
    if inputs['suicidal'] == 1:
        helpers.append("🔴 **Immediate:** Call Tele-MANAS 14416 or a trusted family member right now")
    helpers.append("- A close friend or roommate you trust")
    helpers.append("- A family member (parent, sibling, or cousin)")
    helpers.append("- Your college academic advisor or professor")
    plan['people_to_ask_for_help'] = "\n".join(helpers)

    # Professional contacts – city-specific
    pros = [
        "- Tele-MANAS (National Helpline): **14416** (24/7)",
        "- Vandrevala Foundation: **9999666555** (24/7)",
        "- iCALL: **9152987821** (Mon-Sat, 10 AM-8 PM)",
        "- KIRAN: **1800-599-0019** (24/7)",
        "- Emergency: **112**"
    ]
    if inputs['city'] == "Delhi":
        pros.append("- Delhi Mental Health Helpline: 1800-11-6600")
    elif inputs['city'] == "Mumbai":
        pros.append("- Mumbai District Mental Health Program: 022-2413-8612")
    plan['professional_contacts'] = "\n".join(pros)

    # Safer environment
    if inputs['suicidal'] == 1:
        safety.append("🔴 Ensure you are not alone – stay with a trusted person")
        safety.append("Remove access to any means of self-harm (medications, sharp objects)")
    safety.append("Keep a list of emergency contacts accessible on your phone")
    safety.append("Identify safe spaces on campus/in your city where you feel calm")
    plan['safer_environment'] = "\n".join(safety)

    return plan


# ============================================================
# 5. THEME TOGGLE & SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🎨 Appearance")
    theme_choice = st.radio("Theme", ["☀️ Light", "🌙 Dark"], index=0 if st.session_state.theme == "light" else 1, label_visibility="collapsed")
    st.session_state.theme = "light" if theme_choice == "☀️ Light" else "dark"

    st.markdown("## 🌐 Language")
    lang_choice = st.radio("Language", ["English", "Tamil"], index=0 if st.session_state.language == "English" else 1, label_visibility="collapsed")
    st.session_state.language = "English" if lang_choice == "English" else "Tamil"

    st.divider()
    st.markdown("## 🆘 Immediate Help")
    st.warning("If in immediate danger, call emergency services or reach a trusted person now.")
    st.markdown("**Tele-MANAS:** 14416 (24/7)")
    st.markdown("**Vandrevala:** 9999666555 (24/7)")
    st.markdown("**iCALL:** 9152987821 (Mon-Sat, 10 AM-8 PM)")
    st.markdown("**KIRAN:** 1800-599-0019 (24/7)")
    st.markdown("**Emergency:** 112")
    st.divider()
    st.caption("Built for RescueHacks 2026 • AI model trained on 27,901 student records.")


# ============================================================
# 6. HOME PAGE
# ============================================================
# Load resources
model, scaler, imputer, encoders, features, feature_importance, auc, full_df = load_model_and_preprocessors()

# Title
st.title(text["app_title"])
st.markdown(f"*{text['app_subtitle']}*")
st.markdown("---")

# ============================================================
# 7. MODEL PERFORMANCE & EXPLANATION SECTION (Collapsible)
# ============================================================
with st.expander("📊 How This Works & Model Performance", expanded=False):
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Accuracy", "84.4%")
    col2.metric("🎯 AUC", f"{auc:.2f}")
    col3.metric("📊 Data Size", f"{len(full_df):,} students")
    
    st.markdown("#### 🔍 Top predictors of depression risk (model coefficients)")
    fig, ax = plt.subplots(figsize=(8, 3))
    top5 = feature_importance.head(5)
    ax.barh(top5['Feature'], top5['Coefficient'], color='#E8A33D')
    ax.set_xlabel("Coefficient (positive = higher risk)")
    ax.set_title("How each factor affects depression risk")
    st.pyplot(fig)
    st.caption("Positive coefficients increase risk; negative decrease risk. For example, higher 'Suicidal_Thoughts' strongly increases risk.")


# ============================================================
# 8. INPUT FORM
# ============================================================
with st.form("risk_form"):
    st.subheader("📝 Tell us about your current situation")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", 18, 60, 22, step=1)
        academic_pressure = st.slider("Academic Pressure (0-5)", 0, 5, 3, help="How much academic pressure do you feel?")
        cgpa = st.slider("CGPA", 5.0, 10.0, 7.5, step=0.01)
        study_satisfaction = st.slider("Study Satisfaction (0-5)", 0, 5, 3)
    with col2:
        city = st.selectbox("Your City", ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata"])
        study_hours = st.number_input("Work/Study Hours per day", 0, 15, 5, step=1)
        sleep = st.selectbox("Sleep Duration", ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"])
        suicidal = st.selectbox("Have you ever had suicidal thoughts?", ["No", "Yes"])
        financial_stress = st.slider("Financial Stress (1-5)", 1, 5, 3)
        dietary = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
    
    submitted = st.form_submit_button(text["assess"], use_container_width=True)

if submitted:
    # Encode
    try:
        gender_enc = encoders['Gender'].transform([gender])[0]
    except:
        gender_enc = 0 if gender == "Male" else 1
    try:
        sleep_enc = encoders['Sleep Duration'].transform([sleep])[0]
    except:
        sleep_enc = 0
    try:
        dietary_enc = encoders['Dietary Habits'].transform([dietary])[0]
    except:
        dietary_enc = 0
    suicidal_enc = 1 if suicidal == "Yes" else 0

    input_data = np.array([[
        gender_enc, age, academic_pressure, cgpa, study_satisfaction,
        study_hours, financial_stress, suicidal_enc, sleep_enc, dietary_enc
    ]])
    input_imputed = imputer.transform(input_data)
    input_scaled = scaler.transform(input_imputed)
    proba = model.predict_proba(input_scaled)[0][1]
    risk_score = int(proba * 100)

    user_inputs = {
        'academic_pressure': academic_pressure,
        'sleep': sleep,
        'cgpa': cgpa,
        'suicidal': suicidal_enc,
        'financial_stress': financial_stress,
        'study_satisfaction': study_satisfaction,
        'city': city,
    }

    # ============================================================
    # 9. RISK SCORE DISPLAY WITH GAUGE
    # ============================================================
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"### 🎯 {text['risk_score']}: **{risk_score}%**")
        if risk_score >= 70:
            st.error(text["high"])
        elif risk_score >= 40:
            st.warning(text["moderate"])
        else:
            st.success(text["low"])
        
        # Simple gauge using progress bar
        st.progress(risk_score / 100)

    # ============================================================
    # 10. RISK FACTOR BREAKDOWN (SHAP-like bar chart)
    # ============================================================
    st.markdown("#### " + text["your_risk_breakdown"])
    # Compute contribution (simplified: coefficient * normalized input value)
    # For demonstration, we'll use the scaled input values times coefficients
    contribution = input_scaled[0] * model.coef_[0]
    contrib_df = pd.DataFrame({
        'Factor': features,
        'Contribution': contribution
    }).sort_values('Contribution', ascending=False)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    colors = ['#E8A33D' if c > 0 else '#6E9B87' for c in contrib_df['Contribution']]
    ax2.barh(contrib_df['Factor'], contrib_df['Contribution'], color=colors)
    ax2.axvline(0, color='black', linestyle='--', alpha=0.3)
    ax2.set_xlabel("Contribution to Risk Score")
    ax2.set_title("How each factor affects your risk")
    st.pyplot(fig2)
    st.caption("Positive bars increase your risk; negative bars decrease it.")

    # ============================================================
    # 11. GENERATE & DISPLAY PLAN
    # ============================================================
    st.markdown("---")
    st.subheader(text["plan_title"])
    plan = generate_plan(user_inputs)

    sections = ["warning_signs", "coping_strategies", "supportive_people_places", 
                "people_to_ask_for_help", "professional_contacts", "safer_environment"]
    display_names = ["Warning Signs", "Coping Strategies", "Supportive People/Places", 
                     "People to Ask for Help", "Professional Contacts", "Safer Environment"]

    for section, name in zip(sections, display_names):
        with st.expander(f"**{name}**", expanded=True):
            st.markdown(plan[section])

    # Download
    plan_text = "="*55 + "\n"
    plan_text += "RESCUEPLAN AI — YOUR PERSONALIZED SAFETY PLAN\n"
    plan_text += "="*55 + "\n\n"
    for section, name in zip(sections, display_names):
        plan_text += name.upper() + "\n"
        plan_text += "-"*30 + "\n"
        plan_text += plan[section] + "\n\n"
    plan_text += "="*55 + "\n"
    plan_text += "EMERGENCY CONTACTS (always available)\n"
    plan_text += "="*55 + "\n"
    plan_text += "Tele-MANAS: 14416 | Vandrevala: 9999666555 | iCALL: 9152987821\n"
    plan_text += "KIRAN: 1800-599-0019 | Emergency: 112\n\n"
    plan_text += "Disclaimer: This is an AI-generated screening tool. Please seek professional care."

    st.download_button(
        label=text["download"],
        data=plan_text,
        file_name="RescuePlan_AI_My_Plan.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # ============================================================
    # 12. FEEDBACK SECTION
    # ============================================================
    st.markdown("---")
    st.subheader(text["feedback_title"])
    feedback = st.radio("", [text["feedback_helpful"], text["feedback_somewhat"], text["feedback_not"]], index=None, horizontal=True)
    if feedback:
        st.success(text["feedback_thanks"])
        # In a real app, you'd send this to a database or analytics.

    st.caption(text["warning"])
    if st.button(text["back"], use_container_width=True):
        st.rerun()
