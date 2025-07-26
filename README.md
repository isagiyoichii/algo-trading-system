# ⚙️ Algo Trading System

This is a full-stack, production-ready algorithmic trading system built with:

- 🐍 Backend: FastAPI (Python)
- 🟦 Frontend: React + TypeScript (Create React App)
- 🐘 Database: PostgreSQL (via Docker)
- 📡 Broker API: Zerodha Kite Connect
- 🐳 Infrastructure: Docker & Docker Compose

## 📁 Folder Structure

algo-trading-system/
├── backend/       # FastAPI backend
├── frontend/      # React frontend
├── data/          # Market data
├── models/        # ML/strategy models
├── logs/          # Log files
├── docs/          # Documentation
├── .env.example   # Safe env variables
├── docker-compose.yml
└── README.md

## 🚀 Getting Started

1. Clone the Repo

   git clone https://github.com/your-username/algo-trading-system.git
   cd algo-trading-system

2. Set Up Environment

   cp .env.example .env
   # Fill in your Zerodha credentials and DB config in .env

3. Start All Services

   docker-compose up --build

Then visit:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## 🧪 Stack & Tools

Layer        | Tool/Tech
-------------|------------------------
Backend      | Python, FastAPI
Frontend     | React, TypeScript
Database     | PostgreSQL
Containers   | Docker, Docker Compose
API Client   | Kite Connect (Zerodha)
ML (future)  | scikit-learn, XGBoost

## 🔒 Security Notes

- .env is ignored from Git for safety
- 2FA with pyotp for Zerodha login
- Tokens handled in backend login script

## 📌 Roadmap

- [x] Phase 0: Setup & Infrastructure
- [x] Phase 1: Data Collector
- [x] Phase 2: Strategy Backtester
- [ ] Phase 3: Portfolio Manager
- [ ] Phase 4: ML/AI Integration
- [ ] Phase 5: Analytics Dashboard

## 📄 License

MIT License
