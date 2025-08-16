@echo off

REM Check for Python 3
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python 3 is required but it's not installed.
    exit /b 1
)

REM Create a virtual environment
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create a virtual environment.
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate the virtual environment.
    exit /b 1
)

REM Install required packages
pip install --upgrade pip
pip install -r resources\requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install the required packages.
    exit /b 1
)

REM Run the Streamlit app
streamlit run app.py
if %errorlevel% neq 0 (
    echo Failed to run the Streamlit app.
    exit /b 1
)

REM Deactivate the virtual environment
deactivate
