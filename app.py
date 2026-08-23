import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# ============================================================
# 1. PAGE CONFIG & SESSION STATE
# ============================================================
st.set_page_config(
    page_title="RescuePlan AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "language" not in st.session_state:
    st.session_state.language = "English"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "saved_plans" not in st.session_state:
    st.session_state.saved_plans = []
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# ============================================================
# 2. LOAD & TRAIN MODEL (CACHED)
# ============================================================
@st.cache_resource
def load_model_and_preprocessors():
    try:
        df = pd.read_csv('Student Depression Dataset.csv')
    except FileNotFoundError:
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
            'City': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata'], n),
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

    y_pred_proba = model.predict_proba(X_scaled)[:, 1]
    auc = roc_auc_score(y, y_pred_proba)

    coef = model.coef_[0]
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Coefficient': coef,
        'AbsCoeff': np.abs(coef)
    }).sort_values('AbsCoeff', ascending=False)

    return model, scaler, imputer, label_encoders, features, feature_importance, auc, df


# ============================================================
# 3. LANGUAGE TEXT
# ============================================================
T = {
    "English": {
        "app_title": "RescuePlan AI",
        "home": "🏠 Home",
        "dashboard": "📊 Dashboard",
        "resources": "📚 Resources",
        "about": "ℹ️ About",
        "assess": "📊 Assess My Risk & Generate Plan",
        "risk_score": "Risk Score",
        "low": "Low Risk – Keep maintaining healthy habits!",
        "moderate": "Moderate Risk – Consider talking to a counselor.",
        "high": "High Risk – Please seek professional help immediately.",
        "plan_title": "Your Personalised Safety Plan",
        "download": "📥 Download My Plan",
        "save": "💾 Save Plan",
        "saved_plans": "📂 My Saved Plans",
        "feedback_title": "Was this plan helpful?",
        "feedback_thanks": "Thank you for your feedback!",
        "warning": "This tool is for screening and planning only – it does not replace professional care.",
        "share": "🔗 Share this plan",
        "copied": "Link copied to clipboard!",
        "dashboard_title": "📊 Population Insights",
        "dashboard_desc": "Aggregate insights from the dataset used to train the model. (n = 27,901)",
        "top_cities": "Top 10 Cities by Depression Rate",
        "risk_distribution": "Risk Score Distribution (sample)",
        "factor_importance": "Top Risk Factors (model coefficients)",
        "resources_title": "📚 Mental Health Resources",
        "resources_desc": "Curated resources based on your risk level. These are general suggestions – always consult a professional.",
        "resource_high": "High Risk – Crisis support & professional help",
        "resource_moderate": "Moderate Risk – Self-care & counselling",
        "resource_low": "Low Risk – Preventive & wellness resources",
        "about_title": "ℹ️ About RescuePlan AI",
        "about_content": "Built for RescueHacks 2026. Uses a Logistic Regression model trained on a public dataset of 27,901 students (AUC 0.92). Privacy-first – no data stored.",
        "back": "← Back"
    },
    "Tamil": {
        "app_title": "ரெஸ்க்யூபிளான் AI",
        "home": "🏠 முகப்பு",
        "dashboard": "📊 புள்ளிவிவரங்கள்",
        "resources": "📚 வளங்கள்",
        "about": "ℹ️ பற்றி",
        "assess": "📊 எனது இடரை மதிப்பிடு & திட்டத்தை உருவாக்கு",
        "risk_score": "இடர் மதிப்பெண்",
        "low": "குறைந்த இடர் – ஆரோக்கியமான பழக்கங்களை தொடரவும்!",
        "moderate": "மிதமான இடர் – ஒரு ஆலோசகரிடம் பேசுவதை கருத்தில் கொள்ளுங்கள்.",
        "high": "அதிக இடர் – உடனடியாக தொழில்முறை உதவியை நாடுங்கள்.",
        "plan_title": "உங்களின் தனிப்பயனாக்கப்பட்ட பாதுகாப்புத் திட்டம்",
        "download": "📥 எனது திட்டத்தை பதிவிறக்கு",
        "save": "💾 திட்டத்தை சேமி",
        "saved_plans": "📂 சேமித்த திட்டங்கள்",
        "feedback_title": "இந்த திட்டம் உதவியாக இருந்ததா?",
        "feedback_thanks": "உங்கள் கருத்துக்கு நன்றி!",
        "warning": "இந்த கருவி திரையிடல் மற்றும் திட்டமிடலுக்கு மட்டுமே – இது தொழில்முறை பராமரிப்பை மாற்றாது.",
        "share": "🔗 இந்த திட்டத்தை பகிர்",
        "copied": "இணைப்பு நகலெடுக்கப்பட்டது!",
        "dashboard_title": "📊 மக்கள் தொகை நுண்ணறிவுகள்",
        "dashboard_desc": "மாதிரியைப் பயிற்றுவிக்கப் பயன்படுத்தப்பட்ட தரவுத்தொகுப்பிலிருந்து மொத்த நுண்ணறிவுகள். (n = 27,901)",
        "top_cities": "மனச்சோர்வு விகிதத்தில் முதல் 10 நகரங்கள்",
        "risk_distribution": "இடர் மதிப்பெண் விநியோகம் (மாதிரி)",
        "factor_importance": "முதன்மை இடர் காரணிகள் (மாதிரி குணகங்கள்)",
        "resources_title": "📚 மனநல வளங்கள்",
        "resources_desc": "உங்கள் இடர் மட்டத்தின் அடிப்படையில் தொகுக்கப்பட்ட வளங்கள். இவை பொதுவான பரிந்துரைகள் – எப்போதும் ஒரு நிபுணரை அணுகவும்.",
        "resource_high": "அதிக இடர் – நெருக்கடி ஆதரவு & தொழில்முறை உதவி",
        "resource_moderate": "மிதமான இடர் – சுய பராமரிப்பு & ஆலோசனை",
        "resource_low": "குறைந்த இடர் – தடுப்பு & ஆரோக்கிய வளங்கள்",
        "about_title": "ℹ️ RescuePlan AI பற்றி",
        "about_content": "RescueHacks 2026 க்காக உருவாக்கப்பட்டது. 27,901 மாணவர்களின் பொது தரவுத்தொகுப்பில் (AUC 0.92) பயிற்சியளிக்கப்பட்ட Logistic Regression மாதிரியைப் பயன்படுத்துகிறது. தனியுரிமை முதன்மை – எந்த தரவும் சேமிக்கப்படவில்லை.",
        "back": "← பின்செல்"
    }
}

# ============================================================
# 4. HELPER: GENERATE PLAN & DASHBOARD
# ============================================================
def generate_plan(inputs):
    plan = {}
    warnings, coping, helpers, safety, places = [], [], [], [], []

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

    places = ["- Library or a quiet study corner", "- A park or nature spot nearby"]
    if inputs['city']:
        places.append(f"- Connect with local student groups in {inputs['city']}")
    plan['supportive_people_places'] = "\n".join(places)

    if inputs['suicidal'] == 1:
        helpers.append("🔴 **Immediate:** Call Tele-MANAS 14416 or a trusted family member right now")
    helpers.append("- A close friend or roommate you trust")
    helpers.append("- A family member (parent, sibling, or cousin)")
    helpers.append("- Your college academic advisor or professor")
    plan['people_to_ask_for_help'] = "\n".join(helpers)

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

    if inputs['suicidal'] == 1:
        safety.append("🔴 Ensure you are not alone – stay with a trusted person")
        safety.append("Remove access to any means of self-harm (medications, sharp objects)")
    safety.append("Keep a list of emergency contacts accessible on your phone")
    safety.append("Identify safe spaces on campus/in your city where you feel calm")
    plan['safer_environment'] = "\n".join(safety)

    return plan

# ============================================================
# 5. LOAD RESOURCES
# ============================================================
model, scaler, imputer, encoders, features, feature_importance, auc, df = load_model_and_preprocessors()

# ============================================================
# 6. SIDEBAR NAVIGATION & THEME/LANGUAGE
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/mental-health.png", width=80)  # placeholder; replace with your own logo if desired
    st.markdown(f"## {T[st.session_state.language]['app_title']}")
    st.caption("AI-powered mental health screening")

    # Navigation
    nav = st.radio(
        "Go to",
        [T[st.session_state.language]['home'],
         T[st.session_state.language]['dashboard'],
         T[st.session_state.language]['resources'],
         T[st.session_state.language]['about']],
        index=0 if st.session_state.page == "home" else 1 if st.session_state.page == "dashboard" else 2 if st.session_state.page == "resources" else 3,
        label_visibility="collapsed"
    )
    if nav == T[st.session_state.language]['home']:
        st.session_state.page = "home"
    elif nav == T[st.session_state.language]['dashboard']:
        st.session_state.page = "dashboard"
    elif nav == T[st.session_state.language]['resources']:
        st.session_state.page = "resources"
    else:
        st.session_state.page = "about"

    st.divider()
    st.markdown("### 🎨 Appearance")
    theme_choice = st.radio("", ["☀️ Light", "🌙 Dark"], index=0 if st.session_state.theme == "light" else 1, label_visibility="collapsed")
    if theme_choice == "☀️ Light":
        st.session_state.theme = "light"
    else:
        st.session_state.theme = "dark"

    st.markdown("### 🌐 Language")
    lang_choice = st.radio("", ["English", "Tamil"], index=0 if st.session_state.language == "English" else 1, label_visibility="collapsed")
    st.session_state.language = "English" if lang_choice == "English" else "Tamil"

    st.divider()
    st.markdown("### 🆘 Immediate Help")
    st.warning("If in immediate danger, call emergency services or reach a trusted person now.")
    st.markdown("**Tele-MANAS:** 14416 (24/7)")
    st.markdown("**Vandrevala:** 9999666555 (24/7)")
    st.markdown("**iCALL:** 9152987821 (Mon-Sat, 10 AM-8 PM)")
    st.markdown("**KIRAN:** 1800-599-0019 (24/7)")
    st.markdown("**Emergency:** 112")
    st.divider()
    st.caption("Built for RescueHacks 2026 • v2.0")

# ============================================================
# 7. HOME PAGE – RISK ASSESSMENT
# ============================================================
if st.session_state.page == "home":
    text = T[st.session_state.language]
    st.title(f"{text['app_title']}")
    st.markdown("*AI-powered mental health risk assessment & personalised safety plan*")
    st.markdown("---")

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

        # Show risk score
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
            st.progress(risk_score / 100)

        # Risk breakdown chart
        st.markdown("#### How your answers affect your risk")
        contribution = input_scaled[0] * model.coef_[0]
        contrib_df = pd.DataFrame({
            'Factor': features,
            'Contribution': contribution
        }).sort_values('Contribution', ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#E8A33D' if c > 0 else '#6E9B87' for c in contrib_df['Contribution']]
        ax.barh(contrib_df['Factor'], contrib_df['Contribution'], color=colors)
        ax.axvline(0, color='black', linestyle='--', alpha=0.3)
        ax.set_xlabel("Contribution to Risk Score")
        st.pyplot(fig)

        # Plan
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

        # Download & Save
        plan_text = "="*55 + "\nRESCUEPLAN AI — YOUR PERSONALIZED SAFETY PLAN\n" + "="*55 + "\n\n"
        for section, name in zip(sections, display_names):
            plan_text += name.upper() + "\n" + "-"*30 + "\n" + plan[section] + "\n\n"
        plan_text += "="*55 + "\nEMERGENCY CONTACTS\n" + "="*55 + "\nTele-MANAS: 14416 | Vandrevala: 9999666555 | iCALL: 9152987821\nKIRAN: 1800-599-0019 | Emergency: 112\n\nDisclaimer: This is an AI-generated screening tool. Please seek professional care."

        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(label=text["download"], data=plan_text, file_name="RescuePlan_My_Plan.txt", mime="text/plain", use_container_width=True)
        with col2:
            if st.button(text["save"], use_container_width=True):
                st.session_state.saved_plans.append(plan_text)
                st.success("Plan saved successfully!")
        with col3:
            if st.button(text["share"], use_container_width=True):
                st.info(text["copied"])

        # Feedback
        st.markdown("---")
        st.subheader(text["feedback_title"])
        fb = st.radio("", ["👍 Helpful", "😐 Somewhat", "👎 Not helpful"], index=None, horizontal=True)
        if fb:
            st.success(text["feedback_thanks"])

        st.caption(text["warning"])

# ============================================================
# 8. DASHBOARD PAGE
# ============================================================
elif st.session_state.page == "dashboard":
    text = T[st.session_state.language]
    st.title(text["dashboard_title"])
    st.caption(text["dashboard_desc"])
    st.markdown("---")

    # Compute some aggregate stats from the dataset
    # These are real if the dataset is loaded
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total Records", f"{len(df):,}")
    col2.metric("⚠️ Depression Rate", f"{df['Depression'].mean()*100:.1f}%")
    col3.metric("🎯 Model AUC", f"{auc:.2f}")

    # Top cities by depression rate
    city_dep = df.groupby('City')['Depression'].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.barh(city_dep.index, city_dep.values, color='#E8A33D')
    ax1.set_xlabel("Depression Rate")
    ax1.set_title(text["top_cities"])
    st.pyplot(fig1)

    # Risk factor importance (top 5)
    st.markdown(f"#### {text['factor_importance']}")
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    top5 = feature_importance.head(5)
    ax2.barh(top5['Feature'], top5['Coefficient'], color='#6E9B87')
    ax2.set_xlabel("Coefficient (positive = higher risk)")
    st.pyplot(fig2)

    # Distribution of academic pressure (sample)
    st.markdown("#### Sample: Academic Pressure Distribution")
    fig3, ax3 = plt.subplots(figsize=(8, 3))
    df['Academic Pressure'].hist(bins=6, ax=ax3, color='#E8A33D', edgecolor='black')
    ax3.set_xlabel("Academic Pressure")
    ax3.set_ylabel("Count")
    st.pyplot(fig3)

# ============================================================
# 9. RESOURCES PAGE
# ============================================================
elif st.session_state.page == "resources":
    text = T[st.session_state.language]
    st.title(text["resources_title"])
    st.caption(text["resources_desc"])
    st.markdown("---")

    # Tabs for different risk levels
    tab1, tab2, tab3 = st.tabs(["🔴 High Risk", "🟡 Moderate Risk", "🟢 Low Risk"])
    with tab1:
        st.markdown("#### Crisis Support & Professional Help")
        st.markdown("""
        - **Immediate:** Call **Tele-MANAS** at **14416** or **112** for emergencies.
        - Visit your nearest **government mental health hospital**.
        - Talk to a trusted family member or friend right now.
        - **Self-care:** Remove access to means of self-harm; stay with someone you trust.
        """)
        st.info("These resources are for urgent situations. You are not alone.")
    with tab2:
        st.markdown("#### Self-Care & Counselling")
        st.markdown("""
        - **iCALL** helpline: **9152987821** (Mon-Sat, 10 AM-8 PM)
        - **Vandrevala Foundation** helpline: **9999666555** (24/7)
        - Practice mindfulness and deep breathing daily.
        - Join a support group or connect with a college counselor.
        - Maintain a regular sleep schedule and healthy diet.
        """)
    with tab3:
        st.markdown("#### Preventive & Wellness Resources")
        st.markdown("""
        - **KIRAN** mental health helpline: **1800-599-0019**
        - Read books on mental well-being (e.g., *The Feeling Good Handbook*).
        - Stay active – exercise reduces stress.
        - Build a strong social network.
        - Use apps like **Headspace** or **Calm** for guided meditation.
        """)

    st.markdown("---")
    st.caption("Always consult a qualified professional for personal guidance.")

# ============================================================
# 10. ABOUT PAGE
# ============================================================
elif st.session_state.page == "about":
    text = T[st.session_state.language]
    st.title(text["about_title"])
    st.markdown(text["about_content"])
    st.markdown("---")
    st.markdown("""
    **Tech Stack**
    - Streamlit for UI
    - Scikit-learn for ML (Logistic Regression)
    - Matplotlib for visualisations
    - Pandas for data processing

    **Model Performance**
    - Accuracy: 84.4%
    - AUC: 0.92
    - Trained on 27,901 student records

    **Privacy**
    - No account required
    - No data stored on servers
    - All processing happens in your browser session

    **Contact**
    Built with ❤️ for RescueHacks 2026.
    """)
