
import json
import os

USER_FILE = "user_profiles.json"

def load_user_profiles():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_profiles(profiles):
    with open(USER_FILE, "w") as f:
        json.dump(profiles, f)
