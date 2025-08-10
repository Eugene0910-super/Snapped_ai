#!/usr/bin/env python
"""
Run script for Snapped AI application
Works on both Windows and Unix systems
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

# Configuration
PORT = 12000
HOST = "127.0.0.1"
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
ENV_FILE = ".env"

def is_windows():
    """Check if running on Windows"""
    return platform.system().lower() == "windows"

def create_venv():
    """Create a virtual environment if it doesn't exist"""
    if not Path(VENV_DIR).exists():
        print(f"Creating virtual environment in {VENV_DIR}...")
        venv.create(VENV_DIR, with_pip=True)
        return True
    return False

def get_python_path():
    """Get the path to the Python executable in the virtual environment"""
    if is_windows():
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")

def get_pip_path():
    """Get the path to pip in the virtual environment"""
    if is_windows():
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")

def install_requirements():
    """Install requirements using pip"""
    pip_path = get_pip_path()
    print(f"Installing requirements from {REQUIREMENTS_FILE}...")
    subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS_FILE])

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not Path(ENV_FILE).exists():
        print(f"Creating {ENV_FILE} file...")
        with open(ENV_FILE, "w") as f:
            f.write(f"SERPAPI_API_KEY=your_serpapi_key_here\n")
            f.write(f"DATABASE_URL=sqlite:///./app.db\n")
            f.write(f"MAX_SIMILAR_PRODUCTS=30\n")
            f.write(f"HOST={HOST}\n")
            f.write(f"PORT={PORT}\n")
        print(f"Please edit {ENV_FILE} and set your SerpAPI key")
        return True
    return False

def init_database():
    """Initialize the database"""
    python_path = get_python_path()
    print("Initializing database...")
    init_code = "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"
    subprocess.check_call([python_path, "-c", init_code])

def run_app():
    """Run the application using uvicorn"""
    python_path = get_python_path()
    print(f"Starting application on http://{HOST}:{PORT}")
    print(f"API documentation will be available at http://{HOST}:{PORT}/docs")
    subprocess.check_call([
        python_path, "-m", "uvicorn", "app.main:app", 
        "--host", HOST, 
        "--port", str(PORT),
        "--reload"
    ])

def main():
    """Main function"""
    print(f"Setting up Snapped AI on {platform.system()} ({platform.release()})")
    
    # Create virtual environment if needed
    venv_created = create_venv()
    
    # Install requirements
    install_requirements()
    
    # Create .env file if needed
    env_created = create_env_file()
    
    # Initialize database
    init_database()
    
    # If this is the first run, give the user a chance to edit the .env file
    if env_created:
        print("\nPlease edit the .env file to set your SerpAPI key.")
        if is_windows():
            input("Press Enter to continue...")
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()