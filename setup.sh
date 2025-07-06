#!/bin/bash

echo "Setting up DVT IDE Chatbot..."

# Create virtual environment
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Prompt for launch mode
echo "Setup complete. Do you want to run the chatbot in (w)eb or (c)li mode?"
read -p "[w/c]: " mode
if [ "$mode" == "c" ]; then
  python app.py cli
else
  python app.py
fi
