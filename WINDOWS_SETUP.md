# Windows Setup Guide for Snapped AI

This guide will help you set up and run the Snapped AI application on Windows.

## Prerequisites

1. **Python 3.9+**: Download and install from [python.org](https://www.python.org/downloads/)
2. **Git**: Download and install from [git-scm.com](https://git-scm.com/download/win)
3. **SerpAPI Key**: Get a free API key from [serpapi.com](https://serpapi.com/)

## Installation

### Option 1: Minimal Setup (Recommended for Windows Users with Installation Issues)

This option uses older package versions that don't require Rust at all.

1. Clone the repository:
   ```
   git clone https://github.com/Eugene0910-super/Snapped_ai.git
   cd Snapped_ai
   ```

2. Run the minimal Windows batch script:
   ```
   run_windows_minimal.bat
   ```

3. Open the `.env` file and replace `your_serpapi_key_here` with your actual SerpAPI key.

4. Run the batch script again:
   ```
   run_windows_minimal.bat
   ```

### Option 2: Simplified Setup (For Windows Users)

This option uses a simplified set of dependencies with fewer Rust requirements.

1. Clone the repository:
   ```
   git clone https://github.com/Eugene0910-super/Snapped_ai.git
   cd Snapped_ai
   ```

2. Run the simplified Windows batch script:
   ```
   run_windows_simple.bat
   ```

3. Open the `.env` file and replace `your_serpapi_key_here` with your actual SerpAPI key.

4. Run the batch script again:
   ```
   run_windows_simple.bat
   ```

### Option 3: Standard Setup (Requires Rust)

This option uses all dependencies including those that require Rust.

1. Install Rust:
   - Download and run the Rust installer from [rustup.rs](https://rustup.rs/)
   - Follow the installation instructions
   - Restart your command prompt after installation

2. Clone the repository:
   ```
   git clone https://github.com/Eugene0910-super/Snapped_ai.git
   cd Snapped_ai
   ```

3. Run the Windows batch script:
   ```
   run_windows.bat
   ```

4. Open the `.env` file and replace `your_serpapi_key_here` with your actual SerpAPI key.

### Option 4: Manual Setup

1. Clone the repository:
   ```
   git clone https://github.com/Eugene0910-super/Snapped_ai.git
   cd Snapped_ai
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install minimal dependencies (choose one):
   ```
   pip install -r requirements_minimal.txt  # Minimal dependencies (no Rust)
   ```
   OR
   ```
   pip install -r requirements_simple.txt   # Simplified dependencies (some Rust)
   ```
   OR
   ```
   pip install -r requirements.txt          # Full dependencies (requires Rust)
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   SERPAPI_API_KEY=your_serpapi_key_here
   DATABASE_URL=sqlite:///./app.db
   MAX_SIMILAR_PRODUCTS=30
   HOST=127.0.0.1
   PORT=12000
   ```

5. Initialize the database:
   ```
   python -c "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"
   ```

6. Run the application:
   ```
   python -m uvicorn app.main:app --host 127.0.0.1 --port 12000 --reload
   ```

## Usage

1. Open your browser and navigate to [http://127.0.0.1:12000/docs](http://127.0.0.1:12000/docs)
2. Use the Swagger UI to interact with the API:
   - Upload an image
   - Clip the image if needed
   - Search for similar products

## Troubleshooting

### Common Issues

1. **Rust-related installation errors**: 
   - Use the simplified setup with `run_windows_simple.bat` or `requirements_simple.txt`
   - Or install Rust manually from [rustup.rs](https://rustup.rs/)

2. **Installation errors**: Try installing dependencies one by one:
   ```
   pip install fastapi uvicorn python-multipart httpx pillow python-dotenv
   pip install sqlalchemy aiofiles pydantic pydantic-settings
   pip install waitress
   ```

3. **Database errors**: Delete the `app.db` file and reinitialize:
   ```
   python -c "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"
   ```

4. **Port already in use**: Change the port in the `.env` file and when running uvicorn:
   ```
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

### Feature Differences in Different Setups

#### Minimal Setup (`requirements_minimal.txt`)
- Uses older versions of packages that don't require Rust
- Uses Pydantic v1 instead of v2
- No Redis caching (uses in-memory caching instead)
- No orjson for faster JSON processing (uses standard JSON library instead)
- May have some compatibility issues with the latest code, but core functionality will work

#### Simplified Setup (`requirements_simple.txt`)
- Uses current versions of packages but excludes those requiring Rust
- No Redis caching (uses in-memory caching instead)
- No orjson for faster JSON processing (uses standard JSON library instead)

#### Standard Setup (`requirements.txt`)
- Uses all dependencies including those requiring Rust
- Includes Redis caching (if Redis is available)
- Includes orjson for faster JSON processing

These differences won't affect core functionality but may impact performance for high-volume usage.

### Getting Help

If you encounter any issues, please open an issue on the GitHub repository with:
- The error message
- Steps to reproduce
- Your Windows version
- Your Python version (`python --version`)