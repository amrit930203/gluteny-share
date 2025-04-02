import streamlit as st
from datetime import datetime, date
import os
import pandas as pd

MEAL_LOG_FILE = "meal_log.csv"

st.set_page_config(page_title="Log Meal & Symptoms", layout="centered")

# --- Simplified Styling ---
st.markdown("""
<style>
html, body, .stApp {
    background-color: #fff8dc !important;
    color: black !important;
}
.stTextInput > div > div > input,
.stSelectbox > div[data-baseweb="select"],
.stTextArea > div > textarea,
.stMultiSelect > div {
    background: white !important;
    border: 1px solid #2ecc71 !important;
    border-radius: 12px !important;
    padding: 0.75rem !important;
    color: black !important;
    font-size: 1rem !important;
}
.stButton button {
    background-color: #2ecc71 !important;
    color: black !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
}
.stButton button:hover {
    background-color: #27ae60 !important;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Log Meal & Symptoms")

# --- Select User ---
if "users" not in st.session_state or not st.session_state.users:
    st.info("Please add a user from the Home page to continue.")
    st.stop()

# Select user dropdown
current_user = st.selectbox("Select user", st.session_state.users, index=0)

# --- Log Meal and Symptoms ---
st.markdown("---")
st.subheader("🍽️ Log a Meal with Symptoms")

with st.form("meal_and_symptoms_form", clear_on_submit=True):
    meal_text = st.text_input("What did you eat?", placeholder="e.g. 2 rotis, paneer, salad")
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type")
    symptoms = st.multiselect(
        "What symptoms are you experiencing (if any)?",
        ["Bloating", "Fatigue", "Headache", "Gas", "Skin rash", "Brain fog", "Acidity", "Other"]
    )
    notes = st.text_area("Additional notes (optional)")
    meal_date = st.date_input("Date of the Meal", max_value=date.today())
    submitted = st.form_submit_button("Log Meal and Symptoms")

    if submitted and meal_text.strip():
        log_entry = {
            "timestamp": datetime.now().isoformat(timespec='seconds'),
            "date": str(meal_date),
            "name": current_user,
            "meal": meal_text.strip(),
            "meal_type": meal_type,
            "symptoms": ", ".join(symptoms),  # Empty string if no symptoms
            "notes": notes.strip() if notes else ""  # Default to an empty string
        }

        df = pd.DataFrame([log_entry])

        # Ensure file integrity by validating and fixing column mismatches
        if os.path.exists(MEAL_LOG_FILE):
            try:
                existing_df = pd.read_csv(MEAL_LOG_FILE)
                # Ensure columns match before appending
                expected_columns = ["timestamp", "date", "name", "meal", "meal_type", "symptoms", "notes"]
                for col in expected_columns:
                    if col not in existing_df.columns:
                        existing_df[col] = ""  # Add missing columns with empty values
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df.to_csv(MEAL_LOG_FILE, index=False)
            except pd.errors.ParserError:
                st.error("Meal log file structure is corrupted. Attempting to fix...")
                df.to_csv(MEAL_LOG_FILE, mode='w', header=True, index=False)  # Overwrite with correct structure
        else:
            df.to_csv(MEAL_LOG_FILE, mode='w', header=True, index=False)

        st.success(f"Meal and symptoms logged successfully for {current_user} on {meal_date} ✅")

# --- View Meals & Symptoms Timeline ---
st.markdown("---")
st.subheader(f"🧠 Meals & Symptoms Timeline for {current_user}")

if os.path.exists(MEAL_LOG_FILE):
    try:
        meal_df = pd.read_csv(MEAL_LOG_FILE)
        meal_df = meal_df[meal_df["name"] == current_user].sort_values("date", ascending=False)
        columns_to_display = ["date", "meal_type", "meal"]  # Default columns

        # Dynamically include optional columns if they exist
        if "symptoms" in meal_df.columns:
            columns_to_display.append("symptoms")
        if "notes" in meal_df.columns:
            columns_to_display.append("notes")

        if not meal_df.empty:
            st.dataframe(meal_df[columns_to_display])
        else:
            st.info("No meals and symptoms logged yet.")
    except pd.errors.ParserError:
        st.error("Error reading the meal log file. The file may be corrupted.")
