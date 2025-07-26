# 📊 Algorithmic Trading System — Project Status

## ✅ Phase 0: Planning & Environment Setup
- [x] Folder structure created (`backend`, `scripts`, `frontend`, `logs`)
- [x] `.env` + `.env.example` created
- [x] Docker Compose with PostgreSQL setup
- [x] React frontend scaffolded
- [x] Git initialized

## 🔄 Phase 1: Data Infrastructure & Collection
- [x] `fetch_major_1min.py` working (OHLCV + retry + summary)
- [x] Token automation server done (`token_server.py`)
- [x] PostgreSQL table schema defined
- [x] CSV export module for OHLCV
- [x] Duplicate detection logic

## ⏳ Phase 2: Strategy Framework & Backtesting
- [x] Strategy base class outlined
- [x] Backtest engine with order simulation
- [x] Equity curve, drawdown chart
- [x] CSV report export

## ⏳ Phase 3–4: ML + Execution Infra
- [ ] Feature engineering / model integration
- [ ] Execution logic / Zerodha order flow

## ⏳ Phase 3: Portfolio Manager
- [x] Basic portfolio tracking class

## ⏳ Phase 4: ML/AI Integration
- [x] MLStrategy stub with logistic regression

## ⏳ Phase 5: Analytics Dashboard
- [x] Drawdown API endpoint
