import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime, date
import pandas as pd
import pandas.errors
import json

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

USER_FILE = "user_profiles.json"
MEAL_LOG_FILE = "meal_log.csv"
REPORT_FILE = "report_memory.txt"

# --- Define base context ---
def get_base_context(user_name):
    return st.session_state.user_profiles.get(user_name, f"{user_name} is a new user. Please ask questions to help personalize health suggestions.")

## --- Apply Fitness App Inspired Theme ---
def apply_fitness_theme():
    st.markdown("""
    <style>
    .main {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 12px 32px rgba(0, 255, 100, 0.08);
        backdrop-filter: blur(6px);
        max-width: 1000px;
        margin: auto;
    }

    h1, h2, h3, h4 {
        color: #ffffff;
        font-weight: 600;
    }

    .block-container {
        padding: 2rem 1rem;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #2ecc71;
        border-radius: 12px;
        padding: 0.75rem;
        color: white;
        backdrop-filter: blur(8px);
    }

    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #ffffff !important;
    }

    .stForm {
        background: rgba(255, 255, 255, 0.06);
        padding: 1.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 255, 100, 0.12);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }

    .stButton button {
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #27ae60;
        transform: scale(1.03);
    }

    .stMarkdown, .stDataFrame, .stTextArea {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,255,100,0.1);
        backdrop-filter: blur(6px);
        margin-top: 1rem;
    }

    .stExpander > div > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        backdrop-filter: blur(6px);
        box-shadow: 0 4px 12px rgba(0,255,100,0.1);
    }

    .stDownloadButton > button {
        background-color: #2ecc71;
        color: white;
        font-weight: bold;
        border-radius: 1rem;
        padding: 0.5rem 1.5rem;
    }

    .css-1offfwp {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)


#---------Upload style customise-----------

def apply_upload_style():
    st.markdown("""
    <style>
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,255,100,0.1);
        backdrop-filter: blur(8px);
        margin-top: 1rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
    }

    .stFileUploader .uploadedFileName {
        color: #ffffff;
    }

    .stFileUploader .css-1cpxqw2 {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stFileUploader .css-1cpxqw2:hover {
        background-color: #27ae60;
        transform: scale(1.03);
    }

    .stFileUploader svg {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)




# --- Helper: Load meals + reports for memory ---
def get_memory_context(user):
    memory = ""
    if os.path.exists(MEAL_LOG_FILE):
        try:
            df = pd.read_csv(MEAL_LOG_FILE)
            user_logs = df[df["name"] == user].tail(5)
            if not user_logs.empty:
                memory += f"Recent meals for {user}:\n"
                for _, row in user_logs.iterrows():
                    memory += f"- {row['meal_type']}: {row['meal']} on {row['timestamp']}\n"
        except pd.errors.EmptyDataError:
            memory += "\n(Meal log exists but is empty)\n"
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            lines = f.readlines()[-10:]
            memory += "\nReport Summary (latest 10 lines):\n" + "".join(lines)
    return memory

# --- Session State Initialization ---
def load_user_profiles():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_profiles():
    with open(USER_FILE, "w") as f:
        json.dump(st.session_state.user_profiles, f)

if "users" not in st.session_state:
    st.session_state.user_profiles = load_user_profiles()
    st.session_state.users = list(st.session_state.user_profiles.keys())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# --- Main Page Setup ---
st.set_page_config(page_title="🥗 Nutrition Assistant", layout="centered")
apply_fitness_theme()
apply_upload_style()

st.title("🥗 Gluteny: Your Smart Nutrition Assistant")

# --- Select & Greet ---
st.subheader("👤 Who's asking?")
if st.session_state.users:
    current_user = st.selectbox("Select user", st.session_state.users, index=0, key="user_select")
    if "previous_user" not in st.session_state or st.session_state.previous_user != current_user:
        st.session_state.current_user = current_user
        st.session_state.previous_user = current_user
        st.rerun()
    if current_user:
        st.markdown(f"<div style='text-align:center;color:white;'>👋 Hi {current_user}!</div>", unsafe_allow_html=True)
else:
    current_user = None
    st.info("Please add a user below to begin.")

# --- Manage Users ---
with st.expander("➕➖ Manage Users"):
    col1, col2 = st.columns(2)
    with col1:
        new_user = st.text_input("New user's name")
        new_context = st.text_area("User's health profile")
        height_cm = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
        weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.1)
        age = st.number_input("Age (years)", min_value=1, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        if height_cm > 0:
            bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)
            st.markdown(f"**BMI:** {bmi}")
            if bmi < 18.5:
                st.info("Underweight — consider gaining weight healthily.")
            elif 18.5 <= bmi <= 24.9:
                st.success("Healthy BMI — great job!")
            elif 25 <= bmi <= 29.9:
                st.warning("Overweight — consider mindful eating and activity.")
            else:
                st.error("Obese — health risk. Consult a specialist.")

        if st.button("Add User"):
            if new_user and new_user not in st.session_state.users:
                profile_text = f"{new_context}\nHeight: {height_cm} cm\nWeight: {weight_kg} kg\nBMI: {bmi}\nAge: {age} years\nGender: {gender}"
                st.session_state.users.append(new_user)
                st.session_state.user_profiles[new_user] = profile_text
                save_user_profiles()
                st.rerun()

    with col2:
        if st.session_state.users:
            user_to_delete = st.selectbox("Delete user", st.session_state.users, key="delete_user")
            if st.button("Delete User"):
                st.session_state.users.remove(user_to_delete)
                st.session_state.chat_history.pop(user_to_delete, None)
                st.session_state.user_profiles.pop(user_to_delete, None)
                save_user_profiles()
                if os.path.exists(MEAL_LOG_FILE):
                    df = pd.read_csv(MEAL_LOG_FILE)
                    df = df[df["name"] != user_to_delete]
                    df.to_csv(MEAL_LOG_FILE, index=False)
                st.rerun()

# --- Chat Assistant ---
if current_user:
    user_input = st.text_input("What would you like to ask?")
    if current_user not in st.session_state.chat_history:
        st.session_state.chat_history[current_user] = []

    if user_input:
        try:
            user_context = get_base_context(current_user)
            memory_context = get_memory_context(current_user)
            full_context = f"You are a friendly nutritionist.\nUser info:\n{user_context}\n\nMemory:\n{memory_context}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": full_context},
                    {"role": "user", "content": user_input},
                ]
            )

            answer = response.choices[0].message.content.strip()
            st.session_state.chat_history[current_user].append(("You", user_input))
            st.session_state.chat_history[current_user].append(("Coach", answer))

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

    for speaker, msg in st.session_state.chat_history[current_user]:
        st.markdown(f"**{speaker}:** {msg}")

# --- Log Meal ---
st.markdown("---")
st.subheader("🍽️ Log a Meal")

def calculate_nutritional_score(meal):
    calories = 200
    protein = 15
    fat = 10
    carbs = 30
    return 100 - abs(50 - protein) - abs(50 - carbs) - abs(50 - fat)

if current_user:
    with st.form("meal_form", clear_on_submit=True):
        meal_text = st.text_input("What did you eat?", placeholder="e.g. 2 rotis, paneer, salad")
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type")
        submitted = st.form_submit_button("Log Meal")

        if submitted and meal_text.strip():
            log_entry = {
                "timestamp": datetime.now().isoformat(timespec='seconds'),
                "date": str(date.today()),
                "name": current_user,
                "meal": meal_text.strip(),
                "meal_type": meal_type
            }

            df = pd.DataFrame([log_entry])
            if os.path.exists(MEAL_LOG_FILE):
                df.to_csv(MEAL_LOG_FILE, mode='a', header=False, index=False)
            else:
                df.to_csv(MEAL_LOG_FILE, mode='w', header=True, index=False)

            score = calculate_nutritional_score(meal_text)
            st.success(f"{meal_type} logged for {current_user} ✅")
            st.write(f"Nutritional Quality Score for this meal: {score}")
            st.rerun()
else:
    st.error("Please select a user first to log a meal.")

# --- View Today's Meals ---
if current_user:
    st.subheader(f"📋 Today's Meals for {current_user}")

    if os.path.exists(MEAL_LOG_FILE):
        try:
            all_logs = pd.read_csv(MEAL_LOG_FILE)
            if "date" in all_logs.columns:
                today_logs = all_logs[(all_logs["date"] == str(date.today())) & (all_logs["name"] == current_user)]
                if not today_logs.empty:
                    st.dataframe(today_logs[["timestamp", "meal_type", "meal"]].sort_values("timestamp"))
                else:
                    st.info(f"No meals logged for {current_user} today yet.")
        except pd.errors.EmptyDataError:
            st.info("Meal log is empty.")
    else:
        st.info("Meal log not found.")
