#!/bin/bash

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
fi

# Default port
PORT=8501

# Check if 8501 is busy, then try 8502
if lsof -i :8501 > /dev/null; then
  PORT=8502
fi

# Start Streamlit on selected port
echo "Starting Streamlit on port $PORT..."
streamlit run Nutrition_Assistant.py --server.port=$PORT > streamlit.log 2>&1 &

# Wait for Streamlit to start
sleep 3

# Open in browser
open http://localhost:$PORT
