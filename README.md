# RescuePlan AI – Mental Health Safety Plan Generator

## 🧠 Overview
RescuePlan AI is a Streamlit web app that assesses a student's risk of depression using a trained machine learning model and generates a personalized safety plan tailored to their specific challenges.

## ✨ Features
- **AI Risk Assessment** – Uses a Logistic Regression model trained on 27,901 student records (AUC 0.92).
- **Personalized Safety Plan** – Automatically fills 6 key sections (warning signs, coping strategies, support network, professional contacts, safer environment) based on user inputs.
- **Bilingual** – English and Tamil support.
- **Privacy-first** – No data stored; all processing happens locally in the browser session.

## 🚀 Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://safety-plan-assistant-ojhbrq2avvuhcbfg848upj.streamlit.app/)

## 📂 Files
- `app.py` – Main Streamlit application.
- `requirements.txt` – Python dependencies.
- `Student Depression Dataset.csv` – Dataset used to train the model (public Kaggle dataset). If missing, the app uses a synthetic fallback.

## 🛠️ How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## 🏆 Hackathon
Built for RescueHacks 2026 – Mental Health Support track.

## 📝 Disclaimer
This tool is for screening and planning purposes only. It does not replace professional medical or psychological care.
