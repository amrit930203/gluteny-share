import json
import pandas as pd
from datetime import datetime

# --- File Paths ---
USER_FILE = "user_profiles.json"
MEAL_LOG_FILE = "meal_log.csv"
SYMPTOM_LOG_FILE = "symptom_log.csv"

# --- Test User Profiles ---
test_profiles = {
    "Ankita Test": (
        "Gluten intolerant.\n"
        "Height: 163 cm\nWeight: 68 kg\nBMI: 25.6\n"
        "DOB: 1994-05-14\nAge: 30 years\nGender: Female"
    ),
    "Raj Test": (
        "Pre-diabetic, sedentary.\n"
        "Height: 175 cm\nWeight: 85 kg\nBMI: 27.8\n"
        "DOB: 1990-11-20\nAge: 34 years\nGender: Male"
    )
}

# --- Save user_profiles.json ---
try:
    with open(USER_FILE, "r") as f:
        existing_profiles = json.load(f)
except FileNotFoundError:
    existing_profiles = {}

existing_profiles.update(test_profiles)

with open(USER_FILE, "w") as f:
    json.dump(existing_profiles, f, indent=2)

# --- Sample Meal Data ---
meal_data = [
    {
        "timestamp": "2025-03-28T08:15:00",
        "date": "2025-03-28",
        "name": "Ankita Test",
        "meal": "Oats, almond milk, apple",
        "meal_type": "Breakfast",
        "symptoms": "Bloating",
        "notes": "Felt uneasy afterward"
    },
    {
        "timestamp": "2025-03-28T13:00:00",
        "date": "2025-03-28",
        "name": "Raj Test",
        "meal": "Rice, rajma, salad",
        "meal_type": "Lunch",
        "symptoms": "Brain fog, Fatigue",
        "notes": "Ate a bit too much"
    },
]

meal_df = pd.DataFrame(meal_data)
meal_df.to_csv(MEAL_LOG_FILE, index=False)

# --- Also save to symptom_log.csv for compatibility ---
symptom_df = meal_df[["timestamp", "date", "name", "symptoms", "notes"]]
symptom_df.to_csv(SYMPTOM_LOG_FILE, index=False)

print("✅ Test users and data added!")
