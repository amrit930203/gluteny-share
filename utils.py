# utils.py
import os
import pandas as pd
import json
from datetime import datetime


USER_FILE = "user_profiles.json"
MEAL_LOG_FILE = "meal_log.csv"
SYMPTOM_LOG_FILE = "symptom_log.csv"
REPORT_FILE = "report_memory.txt"

def load_user_profiles():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_profiles(profiles):
    with open(USER_FILE, "w") as f:
        json.dump(profiles, f)

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

def calculate_nutritional_score(meal):
    calories = 200  # Placeholder
    protein = 15
    fat = 10
    carbs = 30
    score = 100 - abs(50 - protein) - abs(50 - carbs) - abs(50 - fat)
    return score

def get_meal_symptom_insight(user):
    if not os.path.exists(MEAL_LOG_FILE) or not os.path.exists(SYMPTOM_LOG_FILE):
        return "Not enough data yet to analyze meal and symptom correlations."

    try:
        meals = pd.read_csv(MEAL_LOG_FILE)
        symptoms = pd.read_csv(SYMPTOM_LOG_FILE)

        meals = meals[meals["name"] == user]
        symptoms = symptoms[symptoms["name"] == user]

        combined = pd.merge(meals, symptoms, on="date", how="inner")

        if combined.empty:
            return "No overlapping meal and symptom data found yet."

        symptom_counts = {}
        for _, row in combined.iterrows():
            meal = row["meal"].lower()
            symptom_list = row["symptoms"].split(", ")
            for symptom in symptom_list:
                if symptom not in symptom_counts:
                    symptom_counts[symptom] = []
                symptom_counts[symptom].append(meal)

        insight = ""
        for symptom, meals_triggered in symptom_counts.items():
            meal_summary = pd.Series(meals_triggered).value_counts().head(2)
            insight += f"🔁 **{symptom}** has occurred after meals like:\n"
            for meal, count in meal_summary.items():
                insight += f"• {meal} ({count} times)\n"
            insight += "\n"

        return insight.strip()

    except Exception as e:
        return f"Error analyzing symptom insight: {e}"
