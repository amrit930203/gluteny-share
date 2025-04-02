✅ Requirements
Python 3.8 or higher

pip (Python package manager)

An OpenAI API key

macOS (for .app launcher) or command-line terminal

Internet connection (for OpenAI calls)




🥗 Gluteny — Your Smart Nutrition Assistant
Gluteny is a personalized AI-powered desktop app that helps you track meals, symptoms, and nutrition, offering intelligent suggestions to improve your health.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📦 Features
👤 Multi-user profile management

🍽️ Meal and symptom logging

🧠 AI-powered nutrition insights via OpenAI

📊 Tracks and correlates symptoms with food

💬 Conversational assistant (Gluteny)

🖥️ Desktop launcher using macOS Automator

🌙 Dark theme UI with premium green & magenta accents

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Getting Started
1. Clone this repository

git clone https://github.com/amrit930203/gluteny-share.git
cd gluteny-share


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


2. Set up your environment
Make sure you have Python and pip installed. You can use brew or pip3 also.

# Recommended: install from requirements
method 1: pip install -r requirements.txt
method 2: python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or manually install key dependencies if the file is missing
pip install streamlit openai python-dotenv pandas




---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


3. Create a .env file for OpenAI API
Create a .env file in the root directory with:


OPENAI_API_KEY=your_openai_api_key_here
You can get an API key from https://platform.openai.com/account/api-keys


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


4. Run the app

streamlit run Nutrition_Assistant.py
Or double-click the GlutenyLauncher.app if you're using the macOS launcher.


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


🍎 macOS Launcher Instructions
If you're using the .app launcher (created via Automator):

✅ Double-click to launch the app in Chrome

🚫 Do not close the browser tab without shutting down the backend

🛑 To properly close the app:

Use Ctrl + C in terminal to stop Streamlit

Or type this in terminal:


pkill -f streamlit

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


🗃️ Data Files

File:Purpose
user_profiles.json:Stores user profiles and preferences

meal_log.csv:Stores all meal logs

symptom_log.csv	(Optional) Symptom logs if maintained separately

report_memory.txt:Tracks conversation summary for AI context and memory

.env:Keeps your OpenAI API key safe

You can delete report_memory.txt if there are no users — it's regenerated automatically when needed.


🧹 Optional Clean-Up
To clear everything:

bash
Copy
Edit
rm user_profiles.json meal_log.csv report_memory.txt



---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

