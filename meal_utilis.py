# utils/meal_utils.py
from datetime import datetime, date
import pandas as pd
import os
from config import MEAL_LOG_FILE

def calculate_nutritional_score(meal_text):
    calories = 200
    protein = 15
    fat = 10
    carbs = 30
    return 100 - abs(50 - protein) - abs(50 - carbs) - abs(50 - fat)

def log_meal(name, meal, meal_type):
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "date": str(date.today()),
        "name": name,
        "meal": meal,
        "meal_type": meal_type
    }

    df = pd.DataFrame([log_entry])
    if os.path.exists(MEAL_LOG_FILE):
        df.to_csv(MEAL_LOG_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(MEAL_LOG_FILE, mode='w', header=True, index=False)

def get_today_meals(name):
    if os.path.exists(MEAL_LOG_FILE):
        df = pd.read_csv(MEAL_LOG_FILE)
        return df[(df["date"] == str(date.today())) & (df["name"] == name)]
    return pd.DataFrame()