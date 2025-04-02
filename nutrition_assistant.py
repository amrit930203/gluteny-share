import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime, date
import pandas as pd
import pandas.errors
import json
import html

st.set_page_config(page_title="🥗 Nutrition Assistant", layout="centered")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)


def load_css(file_path="style.css"):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    



# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

USER_FILE = "user_profiles.json"
REPORT_FILE = "report_memory.txt"
MEAL_LOG_FILE = "meal_log.csv"
SYMPTOM_LOG_FILE = "symptom_log.csv"


# --- Define base context ---
def get_base_context(user_name):
    return st.session_state.user_profiles.get(user_name, f"{user_name} is a new user. Please ask questions to help personalize health suggestions.")

# --- Helper: Load meals + reports for memory ---
def get_memory_context(user):
    memory = ""

    if os.path.exists(MEAL_LOG_FILE):
        try:
            df = pd.read_csv(MEAL_LOG_FILE)

            user_logs = df[df["name"] == user]

            if not user_logs.empty:
                latest_logs = user_logs.sort_values(by="date", ascending=False).head(5)

                memory += f"Here are the last 5 meals logged by {user}:\n"
                for _, row in latest_logs.iterrows():
                    meal_info = f"- {row['date']}: {row['meal_type']} – {row['meal']}"
                    memory += meal_info + "\n"

        except pd.errors.EmptyDataError:
            memory += "(Meal log exists but is empty.)\n"

    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            lines = f.readlines()[-10:]
            memory += "\nReport Summary (latest 10 lines):\n" + "".join(lines)

    return memory.strip()
def get_meal_by_date(user, target_date_str):
    """Search meal log for a specific date (e.g., '31 March' or '2025-03-31')"""
    if not os.path.exists(MEAL_LOG_FILE):
        return None

    try:
        df = pd.read_csv(MEAL_LOG_FILE)
        df = df[df["name"] == user]

        # Normalize the date input
        try:
            if not target_date_str.strip().startswith("202"):
                target_date = datetime.strptime(target_date_str.strip(), "%d %B").replace(year=date.today().year)
            else:
                target_date = datetime.strptime(target_date_str.strip(), "%Y-%m-%d")
        except:
            return None

        # Format target date string
        date_str = target_date.strftime("%Y-%m-%d")

        matching = df[df["date"] == date_str]

        if matching.empty:
            return None

        result = f"Meals logged on {date_str}:\n"
        for _, row in matching.iterrows():
            result += f"- {row['meal_type']}: {row['meal']}\n"
        return result.strip()

    except Exception as e:
        return f"Error checking date-based meals: {e}"



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
                symptom_counts.setdefault(symptom, []).append(meal)

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


        # Build insight text
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


        # Build insight text
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

load_css()


# Apply sidebar title above navigation
# Apply sidebar title and magenta theme
with st.sidebar:
    # Sidebar Header
    st.markdown("""
        <div style="padding-bottom: 0.5rem; padding-left: 0.5rem;">
            <h3 style="color:#ffffff; font-weight: 700; margin-bottom: 0;">
                🍽️ Gluteny
            </h3>
            <p style="color:#ffe6fb; font-size: 0.9rem; margin-top: 0.25rem;">
                Your Nutrition Coach 💜
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Poppins font
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Magenta Gradient Sidebar CSS
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background: linear-gradient(160deg, #9b0fa5, #f93baf) !important;
        padding: 2rem 1rem !important;
        font-family: 'Poppins', sans-serif !important;
    }

    section[data-testid="stSidebar"] * {
        color: #f8f6f8 !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] .css-1aumxhk,
    section[data-testid="stSidebar"] .css-1c7y2kd {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] .css-1aumxhk:hover,
    section[data-testid="stSidebar"] .css-1c7y2kd:hover {
        background-color: #ffffff !important;
        color: #9b0fa5 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)




st.title("🥗 Gluteny: Your Smart Nutrition Assistant")

# --- Select and Greet User ---
st.subheader("👤 Who is the user?")
if st.session_state.users:
    # Ensure current_user is initialized
    if "current_user" not in st.session_state:
        st.session_state.current_user = st.session_state.users[0]

    # Persistent and visible dropdown
    current_user = st.selectbox(
        "Select a user",
        st.session_state.users,
        index=st.session_state.users.index(st.session_state.current_user),
        key="user_select"
    )

    if "previous_user" not in st.session_state or st.session_state.previous_user != current_user:
        st.session_state.current_user = current_user
        st.session_state.previous_user = current_user

        st.rerun()

    st.markdown(f"""
    <div style="
        background: #1e1e1e;
        border-radius: 1rem;
        padding: 1.2rem 2rem;
        box-shadow: 0 0 20px rgba(46, 204, 113, 0.2);
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
    ">
        👋 Hi {current_user}!
    </div>
""", unsafe_allow_html=True)

else:
    current_user = None
    st.warning("No users found.")
    st.markdown("👉 [Click here to add a user](Manage_Users)", unsafe_allow_html=True)


st.markdown("""
    <h4 style="color:#2ecc71; font-weight:600; margin-top: 2rem; margin-bottom: 0.5rem; font-size: 1.3rem;">
        Ask Gluteny
    </h4>
""", unsafe_allow_html=True)



# --- Chat Section ---
if current_user:
    if current_user not in st.session_state.chat_history:
        st.session_state.chat_history[current_user] = []

import re
from dateutil import parser

def extract_meal_query_date(user_input: str):
    # Look for a pattern like "what did I eat on 31 March"
    match = re.search(r"what did i eat on ([\w\s]+)", user_input.lower())
    if match:
        try:
            parsed_date = parser.parse(match.group(1), fuzzy=True).date()
            return parsed_date
        except Exception:
            return None
    return None

# --- Updated Chat Section ---#
import html  # Ensure HTML escaping for dynamic content

if current_user:
    # Add a placeholder that disappears when the user begins typing
    user_input = st.text_input(
        label="",  # No label to avoid extra text
        placeholder="Type your question here..."  # Placeholder text inside the input field
    )
    if current_user not in st.session_state.chat_history:
        st.session_state.chat_history[current_user] = []

    # Check if the input contains a meal date query
    query_date = extract_meal_query_date(user_input)

    if query_date:
        try:
            if os.path.exists(MEAL_LOG_FILE):
                meal_df = pd.read_csv(MEAL_LOG_FILE)
                meal_df["date"] = pd.to_datetime(meal_df["date"]).dt.date

                filtered = meal_df[(meal_df["name"] == current_user) & (meal_df["date"] == query_date)]

                if not filtered.empty:
                    meal_list = "\n".join([
                        f"🍽️ {row['meal_type']}: {row['meal']}" for _, row in filtered.iterrows()
                    ])
                    answer = f"Here’s what you had on {query_date.strftime('%B %d, %Y')}\n\n{meal_list}"
                else:
                    answer = f"It seems like there is no meal history available for you on {query_date.strftime('%B %d, %Y')}.\nWould you like to tell me what you ate on that day so I can provide you with some personalized feedback or recommendations?"

                st.session_state.chat_history[current_user].append(("You", user_input))
                st.session_state.chat_history[current_user].append(("Coach", answer))

        except Exception as e:
            st.error(f"⚠️ Error reading meal data: {e}")

    elif user_input:
        try:
            user_context = get_base_context(current_user)
            memory_context = get_memory_context(current_user)
            symptom_insight = get_meal_symptom_insight(current_user)
            full_context = f"""
You are a proactive, friendly, and observant nutritionist assistant named Gluteny.

Your role is to help the user build better food habits, avoid discomfort, and feel good through diet adjustments.

---

👤 **User Profile**
{user_context}

🍽️ **Meal History**
{memory_context}

🧪 **Symptom Correlation Insights**
{symptom_insight}

---

🧠 **Guidelines for You, Gluteny:**
- If you notice patterns (e.g., symptoms repeatedly appearing after certain meals), kindly point them out and suggest gentle, user-friendly alternatives.
- Ask thoughtful follow-up questions based on recent meals or symptoms.
- Keep your tone warm, conversational, and human-like — like a coach who truly cares.
"""

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

# --- Styled chat display ---
# --- Display chat with scrollable container ---
import html  # Ensure HTML escaping for dynamic content

if current_user and current_user in st.session_state.chat_history:
    chat_html = """
    <style>
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background-color: rgba(28, 28, 28, 0.95);
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 0 12px rgba(0,255,100,0.1);
        backdrop-filter: blur(4px);
        margin-bottom: 1rem;
    }
    .user-msg {
        background-color: rgba(60,60,60,0.8);
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        color: #ffffff !important;
        font-size: 1rem;
    }
    .bot-msg {
        background-color: rgba(46,204,113,0.3);
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
        margin-right: auto;
        text-align: left;
        color: #ffffff !important;
        font-size: 1rem;
    }
    </style>
    <div class="chat-container">
    """

    # Dynamically append messages
    for speaker, msg in st.session_state.chat_history[current_user]:
        if speaker == "You":
            chat_html += f"""<div class="user-msg"><strong>{speaker}:</strong><br>{html.escape(msg)}</div>"""
        else:
            chat_html += f"""<div class="bot-msg"><strong>{speaker}:</strong><br>{html.escape(msg)}</div>"""

    chat_html += "</div>"

    # Render the HTML using components.html
    st.components.v1.html(chat_html, height=500)

