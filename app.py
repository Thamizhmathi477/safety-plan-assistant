import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="My Safety Plan", page_icon="🛡️", layout="centered")

# --- Custom CSS for a professional look ---
st.markdown("""
<style>
    /* Overall background */
    .stApp {
        background-color: #F7F9FC;
    }

    /* Main title */
    h1 {
        color: #1E3A5F;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Subheaders / step titles */
    h3 {
        color: #2C4A6E;
        font-weight: 600;
    }

    /* Card-like container for the main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Text areas */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #D8E0EA;
        background-color: #FFFFFF;
        font-size: 15px;
    }

    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        border: none;
    }

    /* Primary-style Next/View buttons */
    div[data-testid="column"]:nth-of-type(2) .stButton button {
        background-color: #2E6E5E;
        color: white;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton button:hover {
        background-color: #245A4C;
        color: white;
    }

    /* Back button - subtle */
    div[data-testid="column"]:nth-of-type(1) .stButton button {
        background-color: #EDEFF2;
        color: #3A3A3A;
    }

    /* Download button */
    .stDownloadButton button {
        background-color: #1E3A5F;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
    }
    .stDownloadButton button:hover {
        background-color: #16304F;
        color: white;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1E3A5F;
    }
    section[data-testid="stSidebar"] * {
        color: #F0F4F8 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #3A5A7A;
    }

    /* Progress bar track */
    .stProgress > div > div {
        background-color: #4CAF93;
    }

    /* Caption text */
    .stCaption, .css-1n76uvr {
        color: #6B7A8F;
    }

    /* Success/info boxes */
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 0

# List of sections
sections = [
    "Warning Signs",
    "Coping Strategies",
    "Supportive People/Places",
    "People to Ask for Help",
    "Professional Contacts",
    "Safer Environment"
]

# Initialize empty answers if they don't exist
for sec in sections:
    key = sec.lower().replace(" ", "_")
    if key not in st.session_state:
        st.session_state[key] = ""

# --- SIDEBAR (Always Visible) ---
with st.sidebar:
    st.markdown("## 🆘 Immediate Help")
    st.markdown("""
    **If you are in crisis right now, call:**

    📞 **Tele-MANAS** — `14416` *(24/7)*
    📞 **Vandrevala** — `9999666555` *(24/7)*
    📞 **iCall** — `9152987821` *(Mon–Sat, 8am–10pm)*
    📞 **KIRAN** — `1800-599-0019` *(24/7)*
    🚨 **Emergency (Police/Ambulance)** — `112`
    """)
    st.divider()

    # Progress Bar
    total = len(sections)
    done = sum(1 for sec in sections if st.session_state[sec.lower().replace(" ", "_")].strip() != "")
    st.progress(done / total, text=f"Plan Progress: {done}/{total}")

    st.caption("💡 Your answers stay on this device. Nothing is saved to the cloud.")

# --- MAIN APP ---
st.markdown("<h1 style='margin-bottom:0;'>🛡️ Personal Safety Plan Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7A8F; font-size:16px; margin-top:0;'>Build your plan step-by-step. Take your time — there's no rush.</p>", unsafe_allow_html=True)
st.write("")

# Navigation logic
def go_to_next():
    if st.session_state.step < len(sections):
        st.session_state.step += 1

def go_to_prev():
    if st.session_state.step > 0:
        st.session_state.step -= 1

# --- STEP RENDERER ---
current_step = st.session_state.step

if current_step < len(sections):
    section_title = sections[current_step]
    key = section_title.lower().replace(" ", "_")

    st.subheader(f"Step {current_step + 1} of {len(sections)}: {section_title}")

    # Helpful hints for each section
    hints = {
        "warning_signs": "e.g., 'I can't sleep', 'I feel irritable', 'I isolate myself'",
        "coping_strategies": "e.g., 'Take deep breaths', 'Listen to calming music', 'Go for a walk'",
        "supportive_people_places": "e.g., 'My favorite cafe', 'My dog', 'A nature trail nearby'",
        "people_to_ask_for_help": "e.g., 'Mom - call her', 'Rahul - WhatsApp him'",
        "professional_contacts": "e.g., 'School counselor: Mr. Sharma (ext. 123)', 'Family doctor'",
        "safer_environment": "e.g., 'Give sharp objects to a friend', 'Stay with family member'"
    }

    st.caption(hints.get(key, ""))

    # Text area
    user_input = st.text_area(
        "Write your thoughts here:",
        value=st.session_state[key],
        height=150,
        key=f"input_{key}"
    )
    st.session_state[key] = user_input

    st.write("")
    # Navigation Buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if current_step > 0:
            st.button("⬅️ Back", on_click=go_to_prev)
    with col2:
        if current_step < len(sections) - 1:
            st.button("Next ➡️", on_click=go_to_next)
        else:
            st.button("✅ View My Plan", on_click=go_to_next)

else:
    # --- FINAL SUMMARY PAGE ---
    st.balloons()
    st.header("✅ Your Completed Safety Plan")
    st.success("Keep this safe. You have a plan ready if things get hard.")

    # Compile all answers
    plan_text = "="*40 + "\n"
    plan_text += "MY PERSONAL SAFETY PLAN\n"
    plan_text += "="*40 + "\n\n"

    for sec in sections:
        key = sec.lower().replace(" ", "_")
        val = st.session_state[key].strip()
        if val:
            plan_text += f"{sec}:\n{val}\n\n"
        else:
            plan_text += f"{sec}:\n(Not filled yet)\n\n"

    # Add helplines to the exported file too
    plan_text += "-"*40 + "\n"
    plan_text += "EMERGENCY CONTACTS (India):\n"
    plan_text += "Tele-MANAS: 14416\n"
    plan_text += "Vandrevala: 9999666555\n"
    plan_text += "iCall: 9152987821\n"
    plan_text += "KIRAN: 1800-599-0019\n"
    plan_text += "Emergency: 112\n"

    # Nicely rendered cards instead of raw markdown dump
    for sec in sections:
        key = sec.lower().replace(" ", "_")
        val = st.session_state[key].strip()
        with st.container(border=True):
            st.markdown(f"**{sec}**")
            st.write(val if val else "_Not filled yet_")

    st.write("")

    # Download button
    st.download_button(
        label="📥 Download My Plan as .txt",
        data=plan_text,
        file_name="my_safety_plan.txt",
        mime="text/plain"
    )

    if st.button("🔄 Start Over (Clear Everything)"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
