# Finova Investment Platform

**Finova** is a Python-based investment platform simulation that allows users to create accounts, deposit funds, invest in predefined assets, and track the growth of their portfolio over time.  
The project is fully **WSGI-compatible** and structured for easy server deployment or future web integration.

## Features
- **User Registration and Login**
- **Deposit and Manage Account Balances**
- **Invest in Predefined Assets**
- **Track Portfolio Performance**
- **WSGI-ready Deployment (via `wsgi.py`)**

## How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/finova-investment-platform.git
cd finova-investment-platform
```

### 2. Install the required libraries
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python wsgi.py
```

## Notes: 

- Make sure you have Python 3.8+ installed.
- Ensure your requirements.txt includes necessary packages like flask.

## Tech Stack:
- Python 3.8+
- Flask
- WSGI
- Local file storage (JSON/CSV)

## Project Status
This project is currently a simulation for learning and demonstration purposes.
It does not involve real money or real financial transactions.

## Future Improvements
- Integrate real-time market data APIs
- Add password encryption
- Build a full web interface (Flask/FastAPI/Django)
- Migrate to a database backend (SQLite, PostgreSQL)
