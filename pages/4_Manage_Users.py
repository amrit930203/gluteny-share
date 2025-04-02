import streamlit as st
import os
import pandas as pd
import json
from datetime import date

USER_FILE = "user_profiles.json"
MEAL_LOG_FILE = "meal_log.csv"

# Load and Save Functions
def load_user_profiles():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_profiles(profiles):
    with open(USER_FILE, "w") as f:
        json.dump(profiles, f)

# Set Page Config
st.set_page_config(page_title="Manage Users", layout="centered")

# Inject CSS for dark + green UI and refined dropdown styling
st.markdown("""
<style>
/* 🌕 Premium Yellow Background */
html, body, .stApp {
    background-color: #fff8dc !important;
}

/* ⬛ Basic text colors */
h1, h2, h3, h4, .stMarkdown, .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
    color: black !important;
}

/* 🟢 Input Elements */
.stTextInput > div > div > input,
.stTextArea > div > textarea,
.stNumberInput > div > input,
.stDateInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid #2ecc71;
    border-radius: 10px;
    color: black !important;
    padding: 0.5rem;
}

/* ✅ Selectbox Fix (visible selected value) */
div[data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid #2ecc71;
    border-radius: 10px;
    padding: 0.5rem;
    color: black !important; /* Ensure selected text is readable */
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div[role="option"],
div[data-baseweb="select"] div[role="button"] {
    color: black !important; /* Ensure options text is readable */
    font-weight: 500;
    font-size: 1rem;
}
div[data-baseweb="select"] [class*="placeholder"] {
    color: #555; /* Use a subtler color for placeholders */
}

/* 🟢 Buttons */
.stButton > button {
    background-color: #2ecc71;
    color: black;
    border-radius: 10px;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #27ae60;
    transform: scale(1.03);
}

.stSelectbox, .stTextInput, .stTextArea, .stNumberInput, .stDateInput {
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "users" not in st.session_state:
    st.session_state.user_profiles = load_user_profiles()
    st.session_state.users = list(st.session_state.user_profiles.keys())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# Layout Columns
col1, col2 = st.columns(2)

# Add New User
with col1:
    new_user = st.text_input("New user's name")
    new_context = st.text_area("User's health profile")
    height_cm = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
    weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.1)
    dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today())

    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.markdown(f"**Age:** {age} years")
    
    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        index=0 if "selected_gender" not in st.session_state else ["Male", "Female", "Other"].index(st.session_state.selected_gender)
    )
    st.session_state.selected_gender = gender

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
            profile_text = (
                f"{new_context}\n"
                f"Height: {height_cm} cm\n"
                f"Weight: {weight_kg} kg\n"
                f"BMI: {bmi}\n"
                f"DOB: {dob}\n"
                f"Age: {age} years\n"
                f"Gender: {gender}"
            )
            st.session_state.users.append(new_user)
            st.session_state.user_profiles[new_user] = profile_text
            save_user_profiles(st.session_state.user_profiles)
            st.success(f"✅ {new_user} added!")

# Delete User
with col2:
    if st.session_state.users:
        user_to_delete = st.selectbox("Delete user", st.session_state.users, key="delete_user")
        if st.button("Delete User"):
            st.session_state.users.remove(user_to_delete)
            st.session_state.chat_history.pop(user_to_delete, None)
            st.session_state.user_profiles.pop(user_to_delete, None)
            save_user_profiles(st.session_state.user_profiles)
            if os.path.exists(MEAL_LOG_FILE):
                df = pd.read_csv(MEAL_LOG_FILE)
                df = df[df["name"] != user_to_delete]
                df.to_csv(MEAL_LOG_FILE, index=False)
            st.success(f"🗑️ {user_to_delete} deleted!")
