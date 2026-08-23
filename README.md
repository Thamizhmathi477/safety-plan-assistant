# 🏮 RescuePlan

**A lantern for hard nights.**

RescuePlan is a bilingual (English/Tamil), privacy-minded personal safety planning
assistant for students, built for **RescueHacks 2026** under the **Mental Health
Support** track.

## The Problem

We trained a machine learning model on a public dataset of 27,901 Indian students
and achieved 91.8% AUC in identifying depression risk factors. The strongest
predictors were prior suicidal thoughts, academic pressure, CGPA-related stress,
age, and financial stress. Academic and financial stress are not background noise
for students — they are strongly linked to real mental health outcomes.

Most students never prepare a plan for hard moments *before* they happen — they
try to figure it out in the moment, when it's hardest to think clearly.

## The Solution

RescuePlan guides a student through building a personal safety plan **while things
are calm**, based on the **Stanley-Brown Safety Planning Intervention** — the same
evidence-based framework used by crisis clinicians. In six short steps, a student
identifies:

1. Warning signs
2. Coping strategies
3. Supportive people & places
4. People to ask for help
5. Professional contacts
6. Ways to make their environment safer

The finished plan can be downloaded and kept for reference. Verified India crisis
helplines (Tele-MANAS, Vandrevala Foundation, iCALL, KIRAN, Emergency 112) are
always visible in the sidebar and on a dedicated "I Need Help Now" page.

A **Quick Self Check-in** feature offers gentle, non-diagnostic reflections based
on recent academic pressure, sleep, and financial stress — deliberately designed
to never produce a risk score or percentage. Any mention of suicidal thoughts
immediately and unconditionally routes to real crisis resources.

## Why It's Different

- **Bilingual**: full English and Tamil support, including the downloadable plan —
  built for students who think and process better in their first language.
- **No account, no data collection**: everything lives in the browser session only.
- **Doesn't diagnose or replace professionals** — deliberately avoids risk scores
  or percentage-based "diagnoses," and repeatedly points to real human support.
- **Grounded in a real clinical framework**, not an ad-hoc checklist.
- **Backed by our own trained model**, not just cited statistics.

## Tech Stack

- Python + Streamlit
- Deployed on Streamlit Community Cloud
- scikit-learn / XGBoost model trained separately for insight generation

## Data Source

Aggregate insight from the Student Depression Dataset (Kaggle, public), n=27,901.
No individual data is stored or used by the app itself.

## Disclaimer

RescuePlan is a self-guided planning tool. It does not diagnose mental health
conditions and is not a substitute for professional care. If you are in immediate
danger, please contact emergency services (112 in India) or a trusted person right away.

## Future Development

- Expand language support beyond English/Tamil (Hindi, other regional languages)
- Partner with college counseling cells for pilot testing
- Add optional reminder feature to revisit/update the plan periodically
- Explore verified integration with a crisis helpline for warm handoff
