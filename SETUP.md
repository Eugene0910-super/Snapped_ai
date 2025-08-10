# Setup Guide for Snapped AI

This guide will help you set up and run the Snapped AI application on any platform.

## Prerequisites

1. **Python 3.9+**: Download and install from [python.org](https://www.python.org/downloads/)
2. **Git**: Download and install from [git-scm.com](https://git-scm.com/download/win)
3. **SerpAPI Key**: Get a free API key from [serpapi.com](https://serpapi.com/)

## Installation

### Setup Steps

1. Clone the repository:
   ```
   git clone https://github.com/Eugene0910-super/Snapped_ai.git
   cd Snapped_ai
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix (Linux/Mac)
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
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
   python run.py
   ```
   
   Or directly with uvicorn:
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

1. **Installation errors**: Try installing dependencies one by one:
   ```
   pip install fastapi uvicorn python-multipart httpx pillow python-dotenv
   pip install sqlalchemy aiofiles pydantic
   pip install waitress
   ```

2. **Database errors**: Delete the `app.db` file and reinitialize:
   ```
   python -c "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"
   ```

3. **Port already in use**: Change the port in the `.env` file and when running uvicorn:
   ```
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Python version compatibility**: This application is tested with Python 3.9-3.13. If you're using a different version, you may need to adjust the dependencies.

### Getting Help

If you encounter any issues, please open an issue on the GitHub repository with:
- The error message
- Steps to reproduce
- Your operating system
- Your Python version (`python --version`)