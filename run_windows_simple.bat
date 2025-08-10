@echo off
REM Windows batch script to run the FastAPI application with simplified dependencies

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.9+ and try again.
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install simplified dependencies (no Rust required)
echo Installing simplified dependencies...
pip install -r requirements_simple.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo SERPAPI_API_KEY=your_serpapi_key_here > .env
    echo DATABASE_URL=sqlite:///./app.db >> .env
    echo MAX_SIMILAR_PRODUCTS=30 >> .env
    echo HOST=127.0.0.1 >> .env
    echo PORT=12000 >> .env
)

REM Initialize the database
echo Initializing database...
python -c "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"

REM Run the application
echo Starting the application...
python -m uvicorn app.main:app --host 127.0.0.1 --port 12000 --reload

REM Deactivate virtual environment when done
call venv\Scripts\deactivate.bat