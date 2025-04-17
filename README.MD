# Project Documentation

## Overview
This project is a Python-based application that combines FastAPI, LangGraph, and Streamlit for building AI-powered applications. The project structure suggests it includes components for data processing, database management, and AI model integration.

## Project Structure
```
.
├── adapter/          # Adapter components
├── components/       # UI and application components
├── core/            # Core application logic
├── data/            # Data files and resources
├── database/        # Database related files
├── notebooks/       # Jupyter notebooks
├── prompts/         # AI prompt templates
├── app.py           # Main FastAPI application
├── main.py          # Application entry point
├── objects.py       # Data models and objects
├── logger_.py       # Logging configuration
├── requirements.txt # Project dependencies
└── startup.sh       # Startup script
```

## Prerequisites
- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Setup
1. Create a `.env` file in the root directory
2. Configure the necessary environment variables (refer to `.env.example` if available)

## Running the Application

### Using the Startup Script
```bash
./startup.sh
```

### Manual Start
```bash
# For FastAPI backend
uvicorn app:app --reload

# For Streamlit frontend (if applicable)
streamlit run main.py
```

## Dependencies
- FastAPI (0.115.12) - Web framework
- LangChain (various components) - AI framework
- Streamlit (1.44.1) - Web application framework
- Pandas (2.2.3) - Data manipulation
- Qdrant Client (1.13.3) - Vector database
- Other dependencies as listed in requirements.txt

## Logging
- Logs are stored in `Project1_logs.log`
- Logging configuration is managed in `logger_.py`

## Database
- The project uses SQLite databases:
  - `token_tracking.db`
  - `etisalat_sales.db`

## Contributing
1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request
