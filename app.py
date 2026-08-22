import streamlit as st

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="My Safety Plan",
    page_icon="🏮",
    layout="centered"
)

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
        background-color: #F4F6F9;
    }

    h1, h2, h3 {
        font-family: 'Fraunces', serif !important;
        color: #1B2430 !important;
        letter-spacing: -0.3px;
    }

    .hero-title {
        font-family: 'Fraunces', serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #1B2430;
        margin-bottom: 0.2rem;
        line-height: 1.15;
    }

    .hero-sub {
        font-family: 'Inter', sans-serif;
        color: #7C8A9A;
        font-size: 1.02rem;
        margin-top: 0;
        margin-bottom: 1.6rem;
    }

    .stone-path {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0.5rem 0 2rem 0;
    }

    .stone {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        flex-shrink: 0;
        border: 2px solid #D8DEE6;
        background: #FFFFFF;
        color: #A7B1BD;
    }

    .stone.lit {
        background: #E8A33D;
        border-color: #E8A33D;
        color: #1B2430;
        box-shadow: 0 0 0 4px rgba(232, 163, 61, 0.18);
    }

    .stone.current {
        border-color: #1B2430;
        color: #1B2430;
    }

    .stone-line {
        flex: 1;
        height: 2px;
        background: #D8DEE6;
        margin: 0 4px;
    }

    .step-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #E8A33D;
        margin-bottom: 0.3rem;
    }

    .stTextArea textarea {
        border-radius: 12px;
        border: 1.5px solid #D8DEE6;
        background-color: #FFFFFF;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
        padding: 0.9rem;
    }

    .stTextArea textarea:focus {
        border-color: #E8A33D;
        box-shadow: 0 0 0 2px rgba(232, 163, 61, 0.15);
    }

    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.55rem 1.3rem;
        border: none;
        transition: all 0.15s ease;
    }

    div[data-testid="column"]:nth-of-type(2) .stButton button {
        background-color: #1B2430;
        color: #F4F6F9;
    }

    div[data-testid="column"]:nth-of-type(2) .stButton button:hover {
        background-color: #E8A33D;
        color: #1B2430;
    }

    div[data-testid="column"]:nth-of-type(1) .stButton button {
        background-color: transparent;
        color: #7C8A9A;
        border: 1.5px solid #D8DEE6;
    }

    .stDownloadButton button {
        background-color: #6E9B87;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.65rem 1.5rem;
        border: none;
    }

    .stDownloadButton button:hover {
        background-color: #5A8571;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #1B2430;
    }

    section[data-testid="stSidebar"] * {
        color: #E7EBF0 !important;
        font-family: 'Inter', sans-serif;
    }

    section[data-testid="stSidebar"] h2 {
        font-family: 'Fraunces', serif !important;
        color: #E8A33D !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #34435A;
    }

    section[data-testid="stSidebar"] code {
        background-color: #2A3646;
        color: #E8A33D !important;
        padding: 1px 6px;
        border-radius: 4px;
    }

    .stProgress > div > div {
        background-color: #E8A33D;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        border-color: #E3E7EC !important;
        background: #FFFFFF;
    }

    .stAlert {
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
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

for sec in sections:
    key = sec.lower().replace(" ", "_")

    if key not in st.session_state:
        st.session_state[key] = ""


# ============================================================
# HELPLINE INFORMATION
# ============================================================
helplines = [
    ("Tele-MANAS", "14416", "24/7", "Government of India"),
    ("Vandrevala Foundation", "9999666555", "24/7", "Free mental-health support"),
    ("iCALL", "9152987821", "Mon–Sat, 10 AM–8 PM", "TISS psychosocial helpline"),
    ("KIRAN", "1800-599-0019", "24/7", "Government mental-health helpline"),
    ("Emergency", "112", "Emergency services", "National emergency number"),
]


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.markdown("## 🏮 Immediate Help")

    st.warning(
        "If you are in immediate danger or think you may hurt yourself, "
        "contact emergency services or a trusted person now."
    )

    st.markdown("### 🇮🇳 India Support")

    for name, number, availability, description in helplines:
        st.markdown(
            f"""
            **{name}**  
            📞 `{number}`  
            _{availability}_  
            """
        )

    st.divider()

    st.markdown("### 📊 Your Progress")

    total = len(sections)

    done = sum(
        1
        for sec in sections
        if st.session_state[
            sec.lower().replace(" ", "_")
        ].strip() != ""
    )

    progress = done / total

    st.progress(
        progress,
        text=f"Plan progress: {done}/{total}"
    )

    st.divider()

    st.markdown("### 🔒 Privacy")

    st.caption(
        "Your responses are kept in the current app session and are not "
        "saved by this app as a personal account or profile. The download "
        "creates a text file containing the plan you entered."
    )

    st.caption(
        "For maximum privacy, avoid entering passwords, financial details, "
        "or other unnecessary sensitive information."
    )


# ============================================================
# HERO HEADER
# ============================================================
st.markdown(
    '<p class="hero-title">🏮 A lantern for hard nights</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="hero-sub">'
    'Build your plan now, in the calm — so it\'s ready to guide you later. '
    'Take your time.'
    '</p>',
    unsafe_allow_html=True
)


# ============================================================
# STEPPING-STONE PATH
# ============================================================
current_step = st.session_state.step

stone_html = '<div class="stone-path">'

for i in range(len(sections)):

    key = sections[i].lower().replace(" ", "_")

    filled = st.session_state[key].strip() != ""

    cls = "stone"

    if filled:
        cls += " lit"

    elif i == current_step:
        cls += " current"

    stone_html += f'<div class="{cls}">{i + 1}</div>'

    if i < len(sections) - 1:
        stone_html += '<div class="stone-line"></div>'

stone_html += '</div>'

st.markdown(
    stone_html,
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION FUNCTIONS
# ============================================================
def go_to_next():
    if st.session_state.step < len(sections):
        st.session_state.step += 1


def go_to_prev():
    if st.session_state.step > 0:
        st.session_state.step -= 1


# ============================================================
# SECTION HINTS
# ============================================================
hints = {
    "warning_signs":
        "Examples: I can't sleep, I feel irritable, I isolate myself.",

    "coping_strategies":
        "Examples: Take slow breaths, listen to calming music, go for a walk.",

    "supportive_people_places":
        "Examples: My favorite cafe, my pet, a quiet place, a nature trail.",

    "people_to_ask_for_help":
        "Examples: Mom — call her, friend — message them, trusted teacher.",

    "professional_contacts":
        "Examples: College counselor, family doctor, psychologist.",

    "safer_environment":
        "Examples: Stay with someone I trust, move away from unsafe situations."
}


# ============================================================
# MAIN STEP VIEW
# ============================================================
if current_step < len(sections):

    section_title = sections[current_step]

    key = section_title.lower().replace(" ", "_")

    st.markdown(
        f'<p class="step-eyebrow">'
        f'Step {current_step + 1} of {len(sections)}'
        f'</p>',
        unsafe_allow_html=True
    )

    st.subheader(section_title)

    st.caption(hints.get(key, ""))

    user_input = st.text_area(
        "Write your thoughts here:",
        value=st.session_state[key],
        height=150,
        key=f"input_{key}",
        label_visibility="collapsed",
        placeholder="Write anything that would be useful to remember later..."
    )

    st.session_state[key] = user_input

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:

        if current_step > 0:
            st.button(
                "← Back",
                on_click=go_to_prev
            )

    with col2:

        if current_step < len(sections) - 1:

            st.button(
                "Next →",
                on_click=go_to_next
            )

        else:

            st.button(
                "View my plan →",
                on_click=go_to_next
            )

else:

    # ========================================================
    # COMPLETED PLAN
    # ========================================================

    st.markdown(
        '<p class="step-eyebrow">Complete</p>',
        unsafe_allow_html=True
    )

    st.header("Your plan is ready")

    st.success(
        "You now have a plan you can refer to when things feel difficult."
    )

    st.info(
        "This tool is for planning and support. It does not diagnose "
        "mental-health conditions or replace professional care."
    )

    # --------------------------------------------------------
    # BUILD DOWNLOADABLE PLAN
    # --------------------------------------------------------

    plan_text = "=" * 50 + "\n"
    plan_text += "MY PERSONAL SAFETY PLAN\n"
    plan_text += "=" * 50 + "\n\n"

    for sec in sections:

        key = sec.lower().replace(" ", "_")

        val = st.session_state[key].strip()

        plan_text += f"{sec.upper()}:\n"

        if val:
            plan_text += val
        else:
            plan_text += "(Not filled yet)"

        plan_text += "\n\n"

    plan_text += "=" * 50 + "\n"
    plan_text += "INDIA SUPPORT & EMERGENCY CONTACTS\n"
    plan_text += "=" * 50 + "\n\n"

    plan_text += "Tele-MANAS: 14416 (24/7)\n"
    plan_text += "Tele-MANAS alternate: 1800-89-14416\n"
    plan_text += "Vandrevala Foundation: 9999666555 (24/7)\n"
    plan_text += "iCALL: 9152987821 (Mon-Sat, 10 AM-8 PM)\n"
    plan_text += "KIRAN: 1800-599-0019 (24/7)\n"
    plan_text += "Emergency: 112\n"

    plan_text += "\n"
    plan_text += "-" * 50 + "\n"
    plan_text += (
        "If you are in immediate danger, contact emergency services "
        "or seek help from a trusted person or professional.\n"
    )

    # --------------------------------------------------------
    # DISPLAY PLAN
    # --------------------------------------------------------

    for sec in sections:

        key = sec.lower().replace(" ", "_")

        val = st.session_state[key].strip()

        with st.container(border=True):

            st.markdown(f"**{sec}**")

            if val:
                st.write(val)
            else:
                st.caption("Not filled yet")

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.write("")

    st.download_button(
        label="📥 Download my plan (.txt)",
        data=plan_text,
        file_name="my_safety_plan.txt",
        mime="text/plain"
    )

    st.caption(
        "The downloaded file is created from the information you entered "
        "in this session. Store it somewhere private and accessible to you."
    )

    # --------------------------------------------------------
    # START OVER
    # --------------------------------------------------------

    st.write("")

    if st.button("↻ Start over"):

        for sec in sections:

            key = sec.lower().replace(" ", "_")

            st.session_state[key] = ""

        st.session_state.step = 0

        st.rerun()
