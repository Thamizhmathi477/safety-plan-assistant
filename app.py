import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="My Safety Plan", page_icon="🛡️", layout="centered")

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
    st.header("🆘 Immediate Help")
    st.markdown("""
    **If you are in crisis right now, call:**
    
    - **Tele-MANAS:** `14416` (24/7)  
    - **Vandrevala:** `9999666555` (24/7)  
    - **iCall:** `9152987821` (Mon-Sat, 8am-10pm)  
    - **KIRAN:** `1800-599-0019`  
    - **Emergency (Police/Ambulance):** `112`  
    """)
    st.divider()
    
    # Progress Bar
    total = len(sections)
    done = sum(1 for sec in sections if st.session_state[sec.lower().replace(" ", "_")].strip() != "")
    st.progress(done / total, text=f"Plan Progress: {done}/{total}")
    
    st.caption("💡 Your answers stay on this device. Nothing is saved to the cloud.")

# --- MAIN APP ---
st.title("🛡️ Personal Safety Plan Assistant")
st.caption("Build your plan step-by-step. Take your time.")

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
            plan_text += f"**{sec}**:\n{val}\n\n"
        else:
            plan_text += f"**{sec}**:\n(Not filled yet)\n\n"
    
    # Add helplines to the exported file too
    plan_text += "-"*40 + "\n"
    plan_text += "EMERGENCY CONTACTS (India):\n"
    plan_text += "Tele-MANAS: 14416\n"
    plan_text += "Vandrevala: 9999666555\n"
    plan_text += "iCall: 9152987821\n"
    plan_text += "KIRAN: 1800-599-0019\n"
    plan_text += "Emergency: 112\n"
    
    st.markdown(plan_text.replace("\n", "  \n"))  # Display nicely
    
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
