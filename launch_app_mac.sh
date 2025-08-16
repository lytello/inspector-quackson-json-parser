#!/bin/bash

# Exit on error
set -e

# Log file for errors
LOG_FILE="error_log.txt"

# Clear previous log
> "$LOG_FILE"

# Change to the directory of this script
cd "$(dirname "$0")"

# Function to handle errors
handle_error() {
    echo ""
    echo "❌ An error occurred. See '$LOG_FILE' for details."
    echo ""
    echo "🔻 Error log:"
    cat "$LOG_FILE"
    echo ""
    read -p "Press [Enter] to exit..."
    exit 1
}

# Trap errors and run handler
trap 'handle_error' ERR

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but it's not installed." | tee -a "$LOG_FILE"
    handle_error
fi

# Create virtual environment
python3 -m venv venv 2>>"$LOG_FILE"

# Activate the virtual environment
source venv/bin/activate 2>>"$LOG_FILE"

# Install required packages
pip install --upgrade pip 2>>"$LOG_FILE"
pip install -r resources/requirements.txt 2>>"$LOG_FILE"

# Run the Streamlit app
streamlit run app.py 2>>"$LOG_FILE"

# Deactivate after exit
deactivate

# Pause at the end so terminal stays open
echo ""
read -p "✅ Done. Press [Enter] to close..."
