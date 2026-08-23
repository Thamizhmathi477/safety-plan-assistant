import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# ============================================================
# 1. LOAD & TRAIN MODEL (CACHED)
# ============================================================
@st.cache_resource
def load_model_and_preprocessors():
    # Try to load the real dataset; if not found, use mock data.
    try:
        df = pd.read_csv('Student Depression Dataset.csv')
    except FileNotFoundError:
        st.warning("Dataset not found. Using mock data for demo. For full functionality, upload the CSV.")
        # Build a small synthetic dataset that mimics the real one
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
        # Ensure column exists for renaming
        df['Have you ever had suicidal thoughts ?'] = df['Suicidal_Thoughts'].map({1: 'Yes', 0: 'No'})

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

    features = [
        'Gender', 'Age', 'Academic Pressure', 'CGPA', 'Study Satisfaction',
        'Work/Study Hours', 'Financial Stress', 'Suicidal_Thoughts',
        'Sleep Duration', 'Dietary Habits'
    ]
    X = df[features]
    y = df['Depression']

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_scaled, y)

    return model, scaler, imputer, label_encoders, features

# ============================================================
# 2. APP CONFIG & SESSION STATE
# ============================================================
st.set_page_config(page_title="RescuePlan AI", page_icon="🧠", layout="centered")

if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "language" not in st.session_state:
    st.session_state.language = "English"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

# Language text
T = {
    "English": {
        "title": "🧠 RescuePlan AI",
        "subtitle": "AI-powered risk assessment & personalized safety plan",
        "assess": "📊 Assess My Risk & Generate Plan",
        "risk_score": "Risk Score",
        "low": "Low Risk – Keep maintaining healthy habits!",
        "moderate": "Moderate Risk – Consider talking to a counselor.",
        "high": "High Risk – Please seek professional help immediately.",
        "plan_title": "Your Personalized Safety Plan",
        "download": "📥 Download My Plan",
        "back": "← Back to Home",
        "warning": "This tool is for screening and planning only – it does not replace professional care.",
    },
    "Tamil": {
        "title": "🧠 ரெஸ்க்யூபிளான் AI",
        "subtitle": "AI-ஆதரவு இடர் மதிப்பீடு மற்றும் தனிப்பயனாக்கப்பட்ட பாதுகாப்புத் திட்டம்",
        "assess": "📊 எனது இடரை மதிப்பிடு & திட்டத்தை உருவாக்கு",
        "risk_score": "இடர் மதிப்பெண்",
        "low": "குறைந்த இடர் – ஆரோக்கியமான பழக்கங்களை தொடரவும்!",
        "moderate": "மிதமான இடர் – ஒரு ஆலோசகரிடம் பேசுவதை கருத்தில் கொள்ளுங்கள்.",
        "high": "அதிக இடர் – உடனடியாக தொழில்முறை உதவியை நாடுங்கள்.",
        "plan_title": "உங்களின் தனிப்பயனாக்கப்பட்ட பாதுகாப்புத் திட்டம்",
        "download": "📥 எனது திட்டத்தை பதிவிறக்கு",
        "back": "← முகப்பிற்கு திரும்பு",
        "warning": "இந்த கருவி திரையிடல் மற்றும் திட்டமிடலுக்கு மட்டுமே – இது தொழில்முறை பராமரிப்பை மாற்றாது.",
    }
}
text = T[st.session_state.language]

# ============================================================
# 3. HELPER: GENERATE PERSONALIZED PLAN
# ============================================================
def generate_plan(inputs):
    plan = {}
    
    # Warning Signs – based on risk factors
    warnings = []
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

    # Coping Strategies – tailored to risk factors
    coping = []
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

    # Supportive People/Places – based on city
    places = ["- Library or a quiet study corner", "- A park or nature spot nearby"]
    if inputs['city']:
        places.append(f"- Connect with local student groups in {inputs['city']}")
    plan['supportive_people_places'] = "\n".join(places)

    # People to Ask for Help
    helpers = []
    if inputs['suicidal'] == 1:
        helpers.append("🔴 **Immediate:** Call Tele-MANAS 14416 or a trusted family member right now")
    helpers.append("- A close friend or roommate you trust")
    helpers.append("- A family member (parent, sibling, or cousin)")
    helpers.append("- Your college academic advisor or professor")
    plan['people_to_ask_for_help'] = "\n".join(helpers)

    # Professional Contacts – include city-specific numbers if available
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

    # Safer Environment
    safety = []
    if inputs['suicidal'] == 1:
        safety.append("🔴 Ensure you are not alone – stay with a trusted person")
        safety.append("Remove access to any means of self-harm (medications, sharp objects)")
    safety.append("Keep a list of emergency contacts accessible on your phone")
    safety.append("Identify safe spaces on campus/in your city where you feel calm")
    plan['safer_environment'] = "\n".join(safety)

    return plan

# ============================================================
# 4. HOME PAGE – AI Risk Assessment + Plan Generator
# ============================================================
if st.session_state.page == "home":
    # Load model (triggers training if not cached)
    model, scaler, imputer, encoders, features = load_model_and_preprocessors()
    
    st.title(text["title"])
    st.markdown(f"*{text['subtitle']}*")
    st.markdown("---")
    
    # Input Form
    with st.form("risk_form"):
        st.subheader("📝 Tell us about your current situation")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            age = st.number_input("Age", 18, 60, 22, step=1)
            academic_pressure = st.slider("Academic Pressure (0-5)", 0, 5, 3)
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
        # Encode inputs
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
        
        # Build input array
        input_data = np.array([[
            gender_enc, age, academic_pressure, cgpa, study_satisfaction,
            study_hours, financial_stress, suicidal_enc, sleep_enc, dietary_enc
        ]])
        
        # Impute and scale
        input_imputed = imputer.transform(input_data)
        input_scaled = scaler.transform(input_imputed)
        
        # Predict
        proba = model.predict_proba(input_scaled)[0][1]
        risk_score = int(proba * 100)
        
        # Store inputs for plan generation
        user_inputs = {
            'academic_pressure': academic_pressure,
            'sleep': sleep,
            'cgpa': cgpa,
            'suicidal': suicidal_enc,
            'financial_stress': financial_stress,
            'study_satisfaction': study_satisfaction,
            'city': city,
        }
        
        # Display Risk Score
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
        
        # Generate and show plan
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
        
        # Download button
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
        
        st.caption(text["warning"])
        
        # Back button
        if st.button(text["back"], use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

# ============================================================
# 5. HELPLINES & ABOUT (Optional) – can be added as sidebar or expander
# ============================================================
with st.sidebar:
    st.markdown("## 🆘 Immediate Help")
    st.warning("If you are in immediate danger, contact emergency services or reach a trusted person now.")
    st.markdown("**Tele-MANAS:** 14416 (24/7)")
    st.markdown("**Vandrevala Foundation:** 9999666555 (24/7)")
    st.markdown("**iCALL:** 9152987821 (Mon-Sat, 10 AM-8 PM)")
    st.markdown("**KIRAN:** 1800-599-0019 (24/7)")
    st.markdown("**Emergency:** 112")
    st.divider()
    st.markdown("### About")
    st.caption("Built with ❤️ for RescueHacks 2026. AI model trained on 27,901 student records.")
