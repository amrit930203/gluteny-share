# utils/chat_utils.py
from config import MEAL_LOG_FILE, REPORT_FILE
import pandas as pd
import os

def get_base_context(user_name, user_profiles):
    return user_profiles.get(user_name, f"{user_name} is a new user.")

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