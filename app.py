import streamlit as st

# ============================================================
# RESCUEHACKS — PERSONAL MENTAL HEALTH SAFETY PLAN ASSISTANT
# ============================================================

st.set_page_config(
    page_title="RescuePlan",
    page_icon="🏮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# LANGUAGE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F4F6F9;
}

h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    color: #1B2430 !important;
}

.hero {
    padding: 2rem 0 1rem 0;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #1B2430;
    line-height: 1.05;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    color: #6E7B89;
    font-size: 1.08rem;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    background: #FFF2D9;
    color: #9A6415;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.feature-card {
    background: white;
    padding: 1.2rem;
    border-radius: 15px;
    border: 1px solid #E1E6EC;
    margin-bottom: 0.7rem;
}

.feature-title {
    font-weight: 700;
    color: #1B2430;
    margin-bottom: 0.3rem;
}

.feature-text {
    color: #718092;
    font-size: 0.9rem;
}

.stButton button {
    border-radius: 10px;
    font-weight: 600;
    padding: 0.65rem 1.2rem;
}

.stTextArea textarea {
    border-radius: 12px;
    border: 1.5px solid #D8DEE6;
    background: white;
}

.stTextArea textarea:focus {
    border-color: #E8A33D;
}

section[data-testid="stSidebar"] {
    background: #1B2430;
}

section[data-testid="stSidebar"] * {
    color: #E7EBF0 !important;
}

section[data-testid="stSidebar"] h2 {
    color: #E8A33D !important;
    font-family: 'Fraunces', serif !important;
}

.stProgress > div > div {
    background: #E8A33D;
}

.step-box {
    background: white;
    padding: 1.4rem;
    border-radius: 15px;
    border: 1px solid #E1E6EC;
}

.readiness {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid #E1E6EC;
    text-align: center;
}

.readiness-number {
    font-family: 'Fraunces', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #1B2430;
}

.warning-box {
    background: #FFF7E8;
    border-left: 5px solid #E8A33D;
    padding: 1rem;
    border-radius: 8px;
}

.safe-box {
    background: #EDF7F1;
    border-left: 5px solid #6E9B87;
    padding: 1rem;
    border-radius: 8px;
}

.emergency-box {
    background: #FFF0F0;
    border-left: 5px solid #C94C4C;
    padding: 1rem;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

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
    "Safer Environment"
]

for section in sections:
    key = section.lower().replace(" ", "_")

    if key not in st.session_state:
        st.session_state[key] = ""


# ============================================================
# TRANSLATIONS
# ============================================================

T = {
    "English": {
        "app": "RescuePlan",
        "tagline": "A lantern for hard nights.",
        "description":
            "Build a personal safety plan while things are calm, "
            "so you know what to do when things become difficult.",
        "build": "🌿 Build My Safety Plan",
        "help": "🆘 I Need Help Now",
        "privacy": "Designed with privacy in mind. No account is required.",
        "warning": "This tool does not diagnose mental-health conditions "
                   "or replace professional care.",
        "next": "Next →",
        "back": "← Back",
        "complete": "View My Plan →",
        "download": "📥 Download My Plan",
        "start": "Start Over",
    },

    "Tamil": {
        "app": "RescuePlan",
        "tagline": "கடினமான நேரங்களுக்கான ஒரு விளக்கு.",
        "description":
            "நீங்கள் அமைதியாக இருக்கும் நேரத்தில் உங்கள் தனிப்பட்ட "
            "பாதுகாப்புத் திட்டத்தை உருவாக்குங்கள்.",
        "build": "🌿 எனது பாதுகாப்புத் திட்டத்தை உருவாக்கு",
        "help": "🆘 எனக்கு இப்போது உதவி தேவை",
        "privacy": "தனியுரிமையை கருத்தில் கொண்டு வடிவமைக்கப்பட்டுள்ளது.",
        "warning":
            "இந்த கருவி மனநல நோயைக் கண்டறியாது மற்றும் "
            "தொழில்முறை உதவிக்கு மாற்றாகாது.",
        "next": "அடுத்து →",
        "back": "← பின்செல்",
        "complete": "எனது திட்டத்தைப் பார்க்க →",
        "download": "📥 எனது திட்டத்தை பதிவிறக்கு",
        "start": "மீண்டும் தொடங்கு",
    }
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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🏮 RescuePlan")

    st.caption("Personal Mental Health Safety Plan Assistant")

    st.divider()

    language = st.radio(
        "Language / மொழி",
        ["English", "Tamil"],
        index=0 if st.session_state.language == "English" else 1
    )

    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

    st.divider()

    st.markdown("## 🆘 Immediate Help")

    st.warning(
        "If you are in immediate danger, contact emergency services "
        "or reach a trusted person now."
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
        text=f"Plan readiness: {completed}/{len(sections)}"
    )

    st.caption(
        "The app does not diagnose or replace professional mental-health care."
    )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="hero">'
        '<div class="badge">RESCUEHACKS 2026 • MENTAL HEALTH SUPPORT</div>'
        f'<div class="hero-title">🏮 {text["tagline"]}</div>'
        f'<p class="hero-subtitle">{text["description"]}</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            text["build"],
            use_container_width=True
        ):
            st.session_state.page = "plan"
            st.session_state.step = 0
            st.rerun()

    with col2:

        if st.button(
            text["help"],
            use_container_width=True
        ):
            st.session_state.page = "help"
            st.rerun()

    st.write("")

    st.markdown(
        '<div class="warning-box">'
        '<strong>Important:</strong><br>'
        + text["warning"] +
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("Why RescuePlan?")

    features = [
        (
            "🧭 Guided",
            "Six simple steps help you prepare a plan without overwhelming you."
        ),
        (
            "🔎 Personalized",
            "Your own warning signs, coping strategies and support network become part of the plan."
        ),
        (
            "🆘 Safety-first",
            "Immediate support information stays accessible while you use the app."
        ),
        (
            "🔒 Privacy-minded",
            "No account or personal profile is required to create a plan."
        ),
    ]

    for title, description in features:

        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">{title}</div>
                <div class="feature-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.caption(text["privacy"])


# ============================================================
# IMMEDIATE HELP PAGE
# ============================================================

elif st.session_state.page == "help":

    st.markdown(
        '<p class="hero-title">🆘 You don't have to handle everything alone.</p>',
        unsafe_allow_html=True
    )

    st.write(
        "If you are in immediate danger or believe you may hurt yourself, "
        "please seek immediate help from emergency services, a trusted person, "
        "or a qualified mental-health professional."
    )

    st.markdown(
        '<div class="emergency-box">'
        '<strong>🚨 Emergency</strong><br>'
        'India National Emergency Number: <strong>112</strong>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("🇮🇳 Mental Health Support")

    for name, number, availability in helplines:

        with st.container(border=True):

            st.markdown(f"### {name}")

            st.markdown(
                f"📞 **{number}**  \n"
                f"Availability: **{availability}**"
            )

    st.write("")

    st.markdown(
        '<div class="safe-box">'
        '<strong>One small step:</strong><br>'
        'If calling feels difficult, consider moving to a place where '
        'another trusted person is present.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("← Back to RescuePlan", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


# ============================================================
# PLAN PAGE
# ============================================================

elif st.session_state.page == "plan":

    current_step = st.session_state.step

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="badge">YOUR PERSONAL PLAN</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="hero-title">Build your plan, one step at a time.</p>',
        unsafe_allow_html=True
    )

    st.caption(
        "There is no perfect answer. Write what would genuinely help you."
    )

    # --------------------------------------------------------
    # STEP INDICATOR
    # --------------------------------------------------------

    cols = st.columns(6)

    for i, section in enumerate(sections):

        key = section.lower().replace(" ", "_")

        filled = bool(
            st.session_state[key].strip()
        )

        with cols[i]:

            if filled:
                st.success(f"✓ {i + 1}")

            elif i == current_step:
                st.info(f"● {i + 1}")

            else:
                st.caption(f"○ {i + 1}")

    st.write("")

    # --------------------------------------------------------
    # COMPLETION
    # --------------------------------------------------------

    if current_step < len(sections):

        section_title = sections[current_step]

        key = section_title.lower().replace(" ", "_")

        st.markdown(
            f'<div class="step-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"### Step {current_step + 1} of {len(sections)}"
        )

        st.subheader(section_title)

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
                "What changes could make your surroundings safer when you're struggling?"
        }

        st.caption(hints[key])

        examples = {

            "warning_signs":
                "Example: I stop sleeping properly, become quiet, stop replying to messages.",

            "coping_strategies":
                "Example: Walk outside, listen to music, write in a journal.",

            "supportive_people_places":
                "Example: My cousin, college library, my favorite peaceful place.",

            "people_to_ask_for_help":
                "Example: Mom — call her. Best friend — message them.",

            "professional_contacts":
                "Example: College counselor, family doctor, mental-health helpline.",

            "safer_environment":
                "Example: Stay near family, avoid being alone, move away from unsafe situations."
        }

        st.caption("💡 " + examples[key])

        user_input = st.text_area(
            "Your response",
            value=st.session_state[key],
            height=160,
            key=f"textarea_{key}",
            label_visibility="collapsed"
        )

        st.session_state[key] = user_input

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # SIMPLE PERSONALIZED FEEDBACK
        # ----------------------------------------------------

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
                        "irritable"
                    ]
                ):

                    st.info(
                        "💡 You identified an early change. "
                        "Consider choosing one trusted person who could "
                        "notice this pattern and support you."
                    )

            elif key == "coping_strategies":

                if len(user_input.strip()) > 10:

                    st.success(
                        "🌿 Good start. You now have at least one action "
                        "you can try before things become overwhelming."
                    )

            elif key == "people_to_ask_for_help":

                st.info(
                    "🤝 Having a specific person and a specific way to "
                    "contact them can make asking for help easier."
                )

        st.write("")

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

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

    # --------------------------------------------------------
    # FINAL PLAN
    # --------------------------------------------------------

    else:

        st.markdown(
            '<div class="badge">PLAN COMPLETE</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p class="hero-title">Your plan is ready.</p>',
            unsafe_allow_html=True
        )

        completed = sum(
            1
            for section in sections
            if st.session_state[
                section.lower().replace(" ", "_")
            ].strip()
        )

        # ----------------------------------------------------
        # READINESS
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="readiness">
                <div class="readiness-number">
                    {completed}/6
                </div>
                <strong>Plan Readiness</strong>
                <p>
                    {completed} of 6 sections completed
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if completed == 6:

            st.success(
                "🎉 Your safety plan is complete. Keep it somewhere "
                "you can easily access when you need it."
            )

        elif completed >= 4:

            st.info(
                "Your plan is almost complete. Consider filling the "
                "remaining sections to make it more useful."
            )

        else:

            st.warning(
                "Your plan has a good starting point. Adding more "
                "sections can make it more practical."
            )

        # ----------------------------------------------------
        # PERSONALIZED PLAN
        # ----------------------------------------------------

        st.subheader("🔎 My Personal Safety Plan")

        for section in sections:

            key = section.lower().replace(" ", "_")

            value = st.session_state[key].strip()

            with st.container(border=True):

                if value:

                    st.markdown(f"### ✓ {section}")
                    st.write(value)

                else:

                    st.markdown(f"### ○ {section}")
                    st.caption("Not filled yet")

        # ----------------------------------------------------
        # SMART REMINDERS
        # ----------------------------------------------------

        missing = []

        for section in sections:

            key = section.lower().replace(" ", "_")

            if not st.session_state[key].strip():

                missing.append(section)

        if missing:

            st.subheader("💡 Before you finish")

            for item in missing:

                st.markdown(
                    f"- Consider adding something for **{item}**."
                )

        # ----------------------------------------------------
        # DOWNLOAD PLAN
        # ----------------------------------------------------

        plan_text = "=" * 55 + "\n"
        plan_text += "RESCUEPLAN — MY PERSONAL SAFETY PLAN\n"
        plan_text += "=" * 55 + "\n\n"

        for section in sections:

            key = section.lower().replace(" ", "_")

            value = st.session_state[key].strip()

            plan_text += section.upper() + "\n"
            plan_text += "-" * 30 + "\n"

            if value:
                plan_text += value
            else:
                plan_text += "(Not filled yet)"

            plan_text += "\n\n"

        plan_text += "=" * 55 + "\n"
        plan_text += "INDIA SUPPORT & EMERGENCY CONTACTS\n"
        plan_text += "=" * 55 + "\n\n"

        plan_text += "Tele-MANAS: 14416 (24/7)\n"
        plan_text += "Tele-MANAS: 1800-89-14416 (24/7)\n"
        plan_text += "Vandrevala Foundation: 9999666555 (24/7)\n"
        plan_text += "iCALL: 9152987821 (Mon-Sat, 10 AM-8 PM)\n"
        plan_text += "KIRAN: 1800-599-0019 (24/7)\n"
        plan_text += "Emergency: 112\n\n"

        plan_text += "-" * 55 + "\n"
        plan_text += (
            "This plan is a self-guided planning tool. "
            "It does not diagnose or replace professional care.\n"
        )

        st.download_button(
            label=text["download"],
            data=plan_text,
            file_name="RescuePlan_My_Safety_Plan.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.write("")

        if st.button(
            text["start"],
            use_container_width=True
        ):

            for section in sections:

                key = section.lower().replace(" ", "_")

                st.session_state[key] = ""

            st.session_state.step = 0
            st.session_state.page = "home"

            st.rerun()
