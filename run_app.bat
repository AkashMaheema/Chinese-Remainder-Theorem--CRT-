@echo off
setlocal

cd /d "%~dp0"

echo Starting Chinese Remainder Theorem Streamlit app...
python -m streamlit run app.py

if %errorlevel% neq 0 (
    echo.
    echo Streamlit launch failed. Attempting to install dependencies...
    python -m pip install -r requirements.txt

    if %errorlevel% neq 0 (
        echo.
        echo Dependency installation failed.
        echo Make sure Python is installed and available on PATH.
        pause
        exit /b 1
    )

    echo.
    echo Retrying app launch...
    python -m streamlit run app.py
)

echo.
echo App closed.
pause
