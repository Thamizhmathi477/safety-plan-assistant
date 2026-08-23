import streamlit as st
import pandas as pd

# ============================================================
# RESCUEPLAN — RESCUEHACKS COMPETITION EDITION
# ============================================================

st.set_page_config(
    page_title="RescuePlan",
    page_icon="🏮",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "language" not in st.session_state:
    st.session_state.language = "English"

if "page" not in st.session_state:
    st.session_state.page = "home"

if "step" not in st.session_state:
    st.session_state.step = 0


sections = [
    "Warning Signs",
    "Coping Strategies",
    "Supportive People/Places",
    "People to Ask for Help",
    "Professional Contacts",
    "Safer Environment",
]

sections_tamil = {
    "Warning Signs": "எச்சரிக்கை அறிகுறிகள்",
    "Coping Strategies": "சமாளிக்கும் வழிமுறைகள்",
    "Supportive People/Places": "ஆதரவான நபர்கள் / இடங்கள்",
    "People to Ask for Help": "உதவி கேட்கக்கூடிய நபர்கள்",
    "Professional Contacts": "தொழில்முறை தொடர்புகள்",
    "Safer Environment": "பாதுகாப்பான சூழல்",
}


for section in sections:
    key = section.lower().replace(" ", "_")

    if key not in st.session_state:
        st.session_state[key] = ""


# ============================================================
# LANGUAGE TEXT
# ============================================================

T = {
    "English": {
        "tagline": "A lantern for hard nights.",
        "description": (
            "Build a personal safety plan while things are calm, "
            "so you know what to do when things become difficult."
        ),
        "build": "🌿 Build My Safety Plan",
        "help": "🆘 I Need Help Now",
        "privacy": "Designed with privacy in mind. No account is required.",
        "warning": (
            "This tool does not diagnose mental-health conditions "
            "or replace professional care."
        ),
        "next": "Next →",
        "back": "← Back",
        "complete": "View My Plan →",
        "download": "📥 Download My Plan",
        "start": "↻ Start Over",
        "why_title": "📊 Why This Matters",
        "why_caption": (
            "We trained a model on a public dataset of 27,901 Indian students "
            "(91.8% AUC) to understand what's most linked to depression risk. "
            "Academic pressure and financial stress were among the strongest "
            "factors — right alongside a history of difficult thoughts. "
            "Having a plan ready before things get hard makes a real difference."
        ),
        "why_chart_label": "Top predictors of depression risk, from our trained model",
        "checkin": "🌱 Quick Self Check-in",
        "checkin_title": "How are things going lately?",
        "checkin_desc": (
            "A few quick reflections — not a test or a diagnosis. "
            "Just a moment to notice how you're doing."
        ),
        "checkin_suicidal_q": "Have you had thoughts of hurting yourself recently?",
        "checkin_submit": "See My Reflection",
        "checkin_back": "← Back to RescuePlan",
    },

    "Tamil": {
        "tagline": "கடினமான நேரங்களுக்கான ஒரு விளக்கு.",
        "description": (
            "நீங்கள் அமைதியாக இருக்கும் நேரத்தில் உங்கள் தனிப்பட்ட "
            "பாதுகாப்புத் திட்டத்தை உருவாக்குங்கள்."
        ),
        "build": "🌿 எனது பாதுகாப்புத் திட்டத்தை உருவாக்கு",
        "help": "🆘 எனக்கு இப்போது உதவி தேவை",
        "privacy": "தனியுரிமையை கருத்தில் கொண்டு வடிவமைக்கப்பட்டுள்ளது.",
        "warning": (
            "இந்த கருவி மனநல நோயைக் கண்டறியாது மற்றும் "
            "தொழில்முறை உதவிக்கு மாற்றாகாது."
        ),
        "next": "அடுத்து →",
        "back": "← பின்செல்",
        "complete": "எனது திட்டத்தைப் பார்க்க →",
        "download": "📥 எனது திட்டத்தை பதிவிறக்கு",
        "start": "↻ மீண்டும் தொடங்கு",
        "why_title": "📊 இது ஏன் முக்கியம்",
        "why_caption": (
            "27,901 மாணவர்களைக் கொண்ட ஒரு பொது தரவுத்தொகுப்பில் நாங்கள் ஒரு "
            "மாதிரியை பயிற்றுவித்தோம் (91.8% துல்லியம்). படிப்பு அழுத்தமும் "
            "நிதி நெருக்கடியும் மனச்சோர்வு அபாயத்துடன் மிக நெருக்கமாக "
            "தொடர்புடையவை. கடினமான நேரங்களுக்கு முன்பே ஒரு திட்டம் தயாராக "
            "இருப்பது உண்மையான மாற்றத்தை ஏற்படுத்தும்."
        ),
        "why_chart_label": "எங்கள் மாதிரியின்படி மனச்சோர்வு அபாயத்தின் முதன்மை காரணிகள்",
        "checkin": "🌱 விரைவு சுய பரிசோதனை",
        "checkin_title": "சமீபத்தில் எப்படி போய்க்கொண்டிருக்கிறது?",
        "checkin_desc": (
            "சில விரைவான பிரதிபலிப்புகள் — இது ஒரு தேர்வோ கண்டறிதலோ அல்ல. "
            "நீங்கள் எப்படி இருக்கிறீர்கள் என்பதை கவனிக்க ஒரு தருணம்."
        ),
        "checkin_suicidal_q": "சமீபத்தில் உங்களை காயப்படுத்தும் எண்ணங்கள் ஏதேனும் இருந்ததா?",
        "checkin_submit": "எனது பிரதிபலிப்பைப் பார்க்க",
        "checkin_back": "← RescuePlan க்குத் திரும்பு",
    },
}

text = T[st.session_state.language]


# ============================================================
# HELPLINES
# ============================================================

helplines = [
    ("Tele-MANAS", "14416", "24/7"),
    ("Tele-MANAS", "1800-89-14416", "24/7"),
    ("Vandrevala Foundation", "9999666555", "24/7"),
    ("iCALL", "9152987821", "Mon–Sat, 10 AM–8 PM"),
    ("KIRAN", "1800-599-0019", "24/7"),
    ("Emergency", "112", "Emergency services"),
]

# ============================================================
# IMPACT DATA (aggregate, from Student Depression Dataset, n=27,901)
# Source: public Kaggle dataset. No individual records used or stored.
# ============================================================

impact_data = pd.DataFrame(
    {
        "Predictor": [
            "Prior Suicidal Thoughts",
            "Academic Pressure",
            "CGPA",
            "Age",
            "Financial Stress",
        ],
        "Relative Importance (%)": [23.1, 17.3, 13.2, 11.0, 10.3],
    }
).set_index("Predictor")


# ============================================================
# THEME COLORS
# ============================================================

if st.session_state.theme == "light":

    BG = "#F4F6F9"
    CARD = "#FFFFFF"
    TEXT = "#1B2430"
    MUTED = "#667585"
    BORDER = "#E1E6EC"
    INPUT_BG = "#FFFFFF"
    INPUT_TEXT = "#1B2430"
    SIDEBAR = "#1B2430"

else:

    BG = "#10161D"
    CARD = "#1A232D"
    TEXT = "#F4F7FA"
    MUTED = "#B7C0CB"
    BORDER = "#354454"
    INPUT_BG = "#202B36"
    INPUT_TEXT = "#F4F7FA"
    SIDEBAR = "#0B1117"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap'
);

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

h1, h2, h3 {{
    font-family: 'Fraunces', serif !important;
    color: {TEXT} !important;
}}

p, span, label {{
    color: {TEXT};
}}

.hero {{
    padding: 2rem 0 1rem 0;
}}

.hero-title {{
    font-family: 'Fraunces', serif;
    font-size: 3rem;
    font-weight: 700;
    color: {TEXT} !important;
    line-height: 1.05;
    margin-bottom: 0.5rem;
}}

.hero-subtitle {{
    color: {MUTED} !important;
    font-size: 1.08rem;
    line-height: 1.6;
}}

.badge {{
    display: inline-block;
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    background: #3A301E;
    color: #F2C66D !important;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
}}

.feature-card,
.step-box,
.readiness {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 15px;
}}

.feature-card {{
    padding: 1.2rem;
    margin-bottom: 0.7rem;
}}

.feature-title {{
    color: {TEXT} !important;
    font-weight: 700;
    margin-bottom: 0.3rem;
}}

.feature-text {{
    color: {MUTED} !important;
    font-size: 0.9rem;
}}

.step-box {{
    padding: 1.4rem;
}}

.readiness {{
    padding: 1.5rem;
    text-align: center;
}}

.readiness-number {{
    font-family: 'Fraunces', serif;
    font-size: 3rem;
    font-weight: 700;
    color: {TEXT} !important;
}}

.stTextArea textarea {{
    background-color: {INPUT_BG} !important;
    color: {INPUT_TEXT} !important;
    border: 1.5px solid {BORDER} !important;
    border-radius: 12px !important;
    font-size: 15px !important;
}}

.stTextArea textarea:focus {{
    border-color: #E8A33D !important;
    box-shadow: 0 0 0 2px rgba(232, 163, 61, 0.18) !important;
}}

.stTextArea textarea::placeholder {{
    color: {MUTED} !important;
}}

.stButton button {{
    border-radius: 10px;
    font-weight: 600;
    padding: 0.65rem 1.2rem;
    border: 1px solid {BORDER};
}}

.stButton button:hover {{
    border-color: #E8A33D;
}}

.stDownloadButton button {{
    background-color: #6E9B87 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.7rem 1.2rem !important;
}}

.stDownloadButton button:hover {{
    background-color: #5A8571 !important;
}}

.warning-box {{
    background-color: #FFF7E8;
    color: #5D461F;
    border-left: 5px solid #E8A33D;
    padding: 1rem;
    border-radius: 8px;
}}

.safe-box {{
    background-color: #EDF7F1;
    color: #315541;
    border-left: 5px solid #6E9B87;
    padding: 1rem;
    border-radius: 8px;
}}

.emergency-box {{
    background-color: #FFF0F0;
    color: #6E2929;
    border-left: 5px solid #C94C4C;
    padding: 1rem;
    border-radius: 8px;
}}

section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR};
}}

section[data-testid="stSidebar"] * {{
    color: #E7EBF0 !important;
}}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: #E8A33D !important;
    font-family: 'Fraunces', serif !important;
}}

section[data-testid="stSidebar"] hr {{
    border-color: #34435A;
}}

[data-testid="stRadio"] label {{
    color: #E7EBF0 !important;
}}

.stProgress > div > div {{
    background-color: #E8A33D;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: {CARD} !important;
    border-color: {BORDER} !important;
}}

[data-testid="stCaptionContainer"] {{
    color: {MUTED} !important;
}}

@media (max-width: 768px) {{

    .hero-title {{
        font-size: 2.2rem;
    }}

    .hero-subtitle {{
        font-size: 1rem;
    }}

    .feature-card {{
        padding: 1rem;
    }}

}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🏮 RescuePlan")

    st.caption(
        "Personal Mental Health Safety Plan Assistant"
    )

    st.divider()

    st.markdown("### 🎨 Appearance")

    theme_choice = st.radio(
        "Choose theme",
        ["☀️ Light", "🌙 Dark"],
        index=0 if st.session_state.theme == "light" else 1,
        label_visibility="collapsed",
    )

    selected_theme = (
        "light"
        if theme_choice == "☀️ Light"
        else "dark"
    )

    if selected_theme != st.session_state.theme:

        st.session_state.theme = selected_theme

        st.rerun()

    st.markdown("### 🌐 Language")

    language_choice = st.radio(
        "Language",
        ["English", "Tamil"],
        index=(
            0
            if st.session_state.language == "English"
            else 1
        ),
        label_visibility="collapsed",
    )

    if language_choice != st.session_state.language:

        st.session_state.language = language_choice

        st.rerun()

    st.divider()

    st.markdown("## 🆘 Immediate Help")

    st.warning(
        "If you are in immediate danger, contact emergency "
        "services or reach a trusted person now."
    )

    for name, number, availability in helplines:

        st.markdown(
            f"**{name}**  \n"
            f"📞 `{number}`  \n"
            f"_{availability}_"
        )

    st.divider()

    completed = sum(
        1
        for section in sections
        if st.session_state[
            section.lower().replace(" ", "_")
        ].strip()
    )

    st.progress(
        completed / len(sections),
        text=f"Plan readiness: {completed}/{len(sections)}",
    )

    st.caption(
        "No account is required to create a plan."
    )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="hero">'
        '<div class="badge">'
        'RESCUEHACKS 2026 • MENTAL HEALTH SUPPORT'
        '</div>'
        f'<div class="hero-title">'
        f'🏮 {text["tagline"]}'
        f'</div>'
        f'<p class="hero-subtitle">'
        f'{text["description"]}'
        f'</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            text["build"],
            use_container_width=True,
        ):

            st.session_state.page = "plan"
            st.session_state.step = 0

            st.rerun()

    with col2:

        if st.button(
            text["help"],
            use_container_width=True,
        ):

            st.session_state.page = "help"

            st.rerun()

    st.write("")

    if st.button(
        text["checkin"],
        use_container_width=True,
    ):

        st.session_state.page = "checkin"

        st.rerun()

    st.write("")

    st.markdown(
        f'<div class="warning-box">'
        f'<strong>Important:</strong><br>'
        f'{text["warning"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # WHY THIS MATTERS — DATA-BACKED IMPACT SECTION
    # --------------------------------------------------------

    st.subheader(text["why_title"])

    st.caption(text["why_caption"])

    st.bar_chart(impact_data, color="#E8A33D")

    st.caption(text["why_chart_label"])

    st.write("")

    st.subheader("Why RescuePlan?")

    features = [
        (
            "🧭 Guided",
            "Six simple steps help you prepare a plan without overwhelming you.",
        ),
        (
            "🔎 Personalized",
            "Your warning signs, coping strategies and support network become part of your plan.",
        ),
        (
            "🆘 Safety-first",
            "Immediate support information remains accessible while you use the app.",
        ),
        (
            "🔒 Privacy-minded",
            "No account or personal profile is required to create a plan.",
        ),
    ]

    for title, description in features:

        st.markdown(
            f'<div class="feature-card">'
            f'<div class="feature-title">{title}</div>'
            f'<div class="feature-text">{description}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    st.caption(text["privacy"])

    st.caption(
        "Data source: [Student Depression Dataset](https://www.kaggle.com/datasets/hopesb/student-depression-dataset), Kaggle, n=27,901."
    )


# ============================================================
# IMMEDIATE HELP PAGE
# ============================================================

elif st.session_state.page == "help":

    st.markdown(
        "<p class='hero-title'>"
        "🆘 You don't have to handle everything alone."
        "</p>",
        unsafe_allow_html=True,
    )

    st.write(
        "If you are in immediate danger or believe you may "
        "hurt yourself, please seek immediate help from "
        "emergency services, a trusted person, or a qualified "
        "mental-health professional."
    )

    st.markdown(
        '<div class="emergency-box">'
        '<strong>🚨 Emergency</strong><br>'
        'India National Emergency Number: <strong>112</strong>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    st.subheader("🇮🇳 Mental Health Support")

    for name, number, availability in helplines:

        with st.container(border=True):

            st.markdown(
                f"### {name}"
            )

            st.markdown(
                f"📞 **{number}**  \n"
                f"Availability: **{availability}**"
            )

    st.write("")

    st.markdown(
        '<div class="safe-box">'
        '<strong>One small step:</strong><br>'
        'If calling feels difficult, consider moving to a place '
        'where another trusted person is present.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "← Back to RescuePlan",
        use_container_width=True,
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# SELF CHECK-IN PAGE (reflection only — no score, no diagnosis)
# ============================================================

elif st.session_state.page == "checkin":

    st.markdown(
        f'<p class="hero-title">{text["checkin_title"]}</p>',
        unsafe_allow_html=True,
    )

    st.caption(text["checkin_desc"])

    st.write("")

    # ----------------------------------------------------
    # SUICIDAL THOUGHTS — ASKED FIRST, HANDLED SEPARATELY
    # This is never scored or blended with other answers.
    # A "Yes" always routes straight to real help, no exceptions.
    # ----------------------------------------------------

    suicidal = st.radio(
        text["checkin_suicidal_q"],
        ["No", "Yes"],
        index=None,
    )

    if suicidal == "Yes":

        st.markdown(
            '<div class="emergency-box">'
            '<strong>You don\'t have to go through this alone.</strong><br>'
            'Please reach out to one of these right now — a trusted person, '
            'or a helpline below. You deserve support.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        for name, number, availability in helplines:

            with st.container(border=True):

                st.markdown(f"### {name}")

                st.markdown(
                    f"📞 **{number}**  \n"
                    f"Availability: **{availability}**"
                )

    else:

        with st.form("checkin_form"):

            academic_pressure = st.slider(
                "Academic pressure lately (0 = none, 5 = a lot)", 0, 5, 2
            )
            sleep = st.selectbox(
                "Sleep lately",
                [
                    "Less than 5 hours",
                    "5-6 hours",
                    "7-8 hours",
                    "More than 8 hours",
                ],
            )
            financial_stress = st.slider(
                "Financial stress lately (1 = low, 5 = high)", 1, 5, 2
            )
            study_satisfaction = st.slider(
                "How satisfied do you feel with your studies? (0 = not at all, 5 = very)",
                0, 5, 3,
            )

            submitted = st.form_submit_button(text["checkin_submit"])

        if submitted:

            st.write("")

            st.subheader("A few gentle reflections")

            notes = []

            if academic_pressure >= 4:
                notes.append(
                    "Academic pressure sounds heavy right now — maybe exams or "
                    "placements. It might help to talk to a professor, mentor, "
                    "or your class advisor about how you're managing your workload."
                )

            if sleep in ["Less than 5 hours", "5-6 hours"]:
                notes.append(
                    "Your sleep has been on the shorter side lately. It's easy to "
                    "let this slide during exam season, but it genuinely affects "
                    "how manageable everything else feels."
                )

            if financial_stress >= 4:
                notes.append(
                    "Financial stress can quietly weigh on everything else. Your "
                    "college may have a scholarship or financial aid office — "
                    "worth a visit if you haven't checked."
                )

            if study_satisfaction <= 2:
                notes.append(
                    "It sounds like studying hasn't felt rewarding lately — not "
                    "just difficult, but disconnected. That's worth mentioning to "
                    "someone you trust, not just pushing through on your own."
                )

            if notes:

                for n in notes:
                    st.info(n)

            else:

                st.success(
                    "Things sound relatively steady right now. It's still worth "
                    "building a safety plan for harder days ahead."
                )

            st.write("")

            st.caption(
                "This is a reflection, not an assessment or diagnosis. If anything "
                "here feels heavier than you'd like to carry alone, please talk to "
                "someone you trust or a counselor."
            )

            st.write("")

            if st.button(
                text["build"],
                use_container_width=True,
            ):

                st.session_state.page = "plan"
                st.session_state.step = 0

                st.rerun()

    st.write("")

    if st.button(
        text["checkin_back"],
        use_container_width=True,
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# SAFETY PLAN PAGE
# ============================================================

elif st.session_state.page == "plan":

    current_step = st.session_state.step

    st.markdown(
        '<div class="badge">YOUR PERSONAL PLAN</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="hero-title">'
        'Build your plan, one step at a time.'
        '</p>',
        unsafe_allow_html=True,
    )

    st.caption(
        "There is no perfect answer. "
        "Write what would genuinely help you."
    )

    cols = st.columns(6)

    for i, section in enumerate(sections):

        key = section.lower().replace(" ", "_")

        filled = bool(
            st.session_state[key].strip()
        )

        with cols[i]:

            if filled:

                st.success(
                    f"✓ {i + 1}"
                )

            elif i == current_step:

                st.info(
                    f"● {i + 1}"
                )

            else:

                st.caption(
                    f"○ {i + 1}"
                )

    st.write("")

    if current_step < len(sections):

        section_title = sections[current_step]

        key = section_title.lower().replace(" ", "_")

        hints = {

            "warning_signs":
                "What changes do you notice when things begin becoming difficult?",

            "coping_strategies":
                "What can you do by yourself that usually helps you feel calmer?",

            "supportive_people_places":
                "What people, places or activities make you feel comfortable or distracted?",

            "people_to_ask_for_help":
                "Who could you contact when you need someone to know what you're going through?",

            "professional_contacts":
                "Who could provide professional support — counselor, doctor, psychologist or helpline?",

            "safer_environment":
                "What changes could make your surroundings safer when you're struggling?",
        }

        examples = {

            "warning_signs":
                "I skip meals in the mess, stop replying on WhatsApp for days, "
                "or start avoiding my friend group in class.",

            "coping_strategies":
                "Go for a walk around the hostel grounds, call my sister, "
                "watch anime for an hour, write in my journal.",

            "supportive_people_places":
                "My roommate, the library terrace, my cousin's house during "
                "weekends, the temple near my village.",

            "people_to_ask_for_help":
                "Amma — she always picks up. My senior from the coding club, "
                "she's been through placement stress too.",

            "professional_contacts":
                "College counselor (2nd floor, admin block), Dr. Suresh at the "
                "PHC back home, Tele-MANAS if I can't reach anyone else.",

            "safer_environment":
                "Keep my phone away from my desk at night, tell my roommate "
                "when I'm having a bad week so she checks on me.",
        }

        st.markdown(
            '<div class="step-box">',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"### Step {current_step + 1} "
            f"of {len(sections)}"
        )

        st.subheader(section_title)

        st.caption(
            hints[key]
        )

        st.caption(
            "💡 " + examples[key]
        )

        user_input = st.text_area(
            "Your response",
            value=st.session_state[key],
            height=160,
            key=f"textarea_{key}",
            label_visibility="collapsed",
            placeholder=(
                "Write anything that would be useful "
                "to remember later..."
            ),
        )

        st.session_state[key] = user_input

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

        if user_input.strip():

            lower = user_input.lower()

            if key == "warning_signs":

                if any(
                    word in lower
                    for word in [
                        "alone",
                        "isolate",
                        "sleep",
                        "cry",
                        "angry",
                        "irritable",
                    ]
                ):

                    st.info(
                        "💡 You identified an early change. "
                        "Consider choosing one trusted person "
                        "who could notice this pattern and "
                        "support you."
                    )

            elif key == "coping_strategies":

                if len(user_input.strip()) > 10:

                    st.success(
                        "🌿 Good start. You now have at least "
                        "one action you can try before things "
                        "become overwhelming."
                    )

            elif key == "people_to_ask_for_help":

                st.info(
                    "🤝 Having a specific person and a specific "
                    "way to contact them can make asking for "
                    "help easier."
                )

        st.write("")

        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:

            if current_step > 0:

                if st.button(text["back"]):

                    st.session_state.step -= 1

                    st.rerun()

        with col2:

            if current_step < len(sections) - 1:

                if st.button(text["next"]):

                    st.session_state.step += 1

                    st.rerun()

            else:

                if st.button(text["complete"]):

                    st.session_state.step = len(sections)

                    st.rerun()

    # ========================================================
    # FINAL PLAN
    # ========================================================

    else:

        st.markdown(
            '<div class="badge">PLAN COMPLETE</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="hero-title">'
            'Your plan is ready.'
            '</p>',
            unsafe_allow_html=True,
        )

        completed = sum(
            1
            for section in sections
            if st.session_state[
                section.lower().replace(" ", "_")
            ].strip()
        )

        st.markdown(
            f'<div class="readiness">'
            f'<div class="readiness-number">'
            f'{completed}/6'
            f'</div>'
            f'<strong>Plan Readiness</strong>'
            f'<p>{completed} of 6 sections completed</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        if completed == 6:

            st.success(
                "🎉 Your safety plan is complete. "
                "Keep it somewhere you can easily access."
            )

        elif completed >= 4:

            st.info(
                "Your plan is almost complete. "
                "Consider filling the remaining sections."
            )

        else:

            st.warning(
                "Your plan has a good starting point. "
                "Adding more sections can make it more practical."
            )

        st.subheader(
            "🔎 My Personal Safety Plan"
        )

        for section in sections:

            key = section.lower().replace(" ", "_")

            value = st.session_state[key].strip()

            display_title = (
                sections_tamil[section]
                if st.session_state.language == "Tamil"
                else section
            )

            with st.container(border=True):

                if value:

                    st.markdown(
                        f"### ✓ {display_title}"
                    )

                    st.write(value)

                else:

                    st.markdown(
                        f"### ○ {display_title}"
                    )

                    st.caption(
                        "Not filled yet"
                        if st.session_state.language == "English"
                        else "இன்னும் நிரப்பப்படவில்லை"
                    )

        missing = []

        for section in sections:

            key = section.lower().replace(" ", "_")

            if not st.session_state[key].strip():

                missing.append(section)

        if missing:

            st.subheader(
                "💡 Before you finish"
            )

            for item in missing:

                st.markdown(
                    f"- Consider adding something for "
                    f"**{item}**."
                )

        # ----------------------------------------------------
        # DOWNLOAD — LOCALIZED FOR ENGLISH AND TAMIL
        # ----------------------------------------------------

        is_tamil = st.session_state.language == "Tamil"

        if is_tamil:

            title_line = "ரெஸ்க்யூபிளான் — எனது தனிப்பட்ட பாதுகாப்புத் திட்டம்"
            not_filled = "(இன்னும் நிரப்பப்படவில்லை)"
            helplines_header = "இந்திய ஆதரவு & அவசர தொடர்புகள்"
            disclaimer = (
                "இது ஒரு சுய-வழிகாட்டும் திட்டமிடல் கருவி. "
                "இது மனநல நோயைக் கண்டறியாது மற்றும் தொழில்முறை "
                "பராமரிப்புக்கு மாற்றாகாது."
            )

        else:

            title_line = "RESCUEPLAN — MY PERSONAL SAFETY PLAN"
            not_filled = "(Not filled yet)"
            helplines_header = "INDIA SUPPORT & EMERGENCY CONTACTS"
            disclaimer = (
                "This plan is a self-guided planning tool. "
                "It does not diagnose or replace professional care."
            )

        plan_text = "=" * 55 + "\n"
        plan_text += title_line + "\n"
        plan_text += "=" * 55 + "\n\n"

        for section in sections:

            key = section.lower().replace(" ", "_")

            value = st.session_state[key].strip()

            display_title = (
                sections_tamil[section] if is_tamil else section
            )

            plan_text += display_title.upper() + "\n"
            plan_text += "-" * 30 + "\n"

            if value:

                plan_text += value

            else:

                plan_text += not_filled

            plan_text += "\n\n"

        plan_text += "=" * 55 + "\n"
        plan_text += helplines_header + "\n"
        plan_text += "=" * 55 + "\n\n"

        plan_text += "Tele-MANAS: 14416\n"
        plan_text += "Tele-MANAS alternate: 1800-89-14416\n"
        plan_text += "Vandrevala Foundation: 9999666555\n"
        plan_text += "iCALL: 9152987821\n"
        plan_text += "KIRAN: 1800-599-0019\n"
        plan_text += "Emergency: 112\n\n"

        plan_text += "-" * 55 + "\n"
        plan_text += disclaimer + "\n"

        st.download_button(
            label=text["download"],
            data=plan_text,
            file_name="RescuePlan_My_Safety_Plan.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.write("")

        if st.button(
            text["start"],
            use_container_width=True,
        ):

            for section in sections:

                key = section.lower().replace(" ", "_")

                st.session_state[key] = ""

            st.session_state.step = 0
            st.session_state.page = "home"

            st.rerun()
