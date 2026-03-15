# 📉 RAM Arbitrage Bot (RAB)

### _Hedge against the global memory shortage with algorithmic procurement._

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package_Manager-de5d43?logo=rust)](https://github.com/astral-sh/uv)
[![Playwright](https://img.shields.io/badge/Playwright-Scraping-2e8b57?logo=playwright)](https://playwright.dev/)
[![Tests](https://github.com/autumnmoon11/ram-arbitrage-bot/actions/workflows/python-tests.yml/badge.svg)](https://github.com/autumnmoon11/ram-arbitrage-bot/actions)

## 🚀 Overview

Due to the 2026 surge in AI datacenter demands, global RAM manufacturing has shifted toward High-Bandwidth Memory (HBM), causing a structural shortage in the consumer market.

**RAB** is a specialized price-tracking and arbitrage engine designed to monitor "Spot-Market" volatility across major retailers. It utilizes asynchronous scrapers to identify undervalued inventory and trigger buy signals before retail prices adjust to wholesale spikes.

## ✨ Key Features

- **Asynchronous Scraping:** Powered by Playwright to handle JavaScript-heavy retail sites without blocking the API.
- **Background Processing:** Uses FastAPI `BackgroundTasks` to perform deep-scans while maintaining a responsive UI/API.
- **Modern Tooling:** Built with **uv** for lightning-fast dependency resolution and virtual environment management.
- **Scalable Core:** Modular scraper architecture allowing for easy integration of new retailers.
- **Persistence Layer:** Built with **SQLModel** (SQLAlchemy + Pydantic) for robust price-history tracking.
- **Multi-Retailer Scraping:** Dedicated stealth scrapers for **Amazon** and **Newegg** using Playwright.
- **Automated CI/CD:** Robust testing suite powered by **Pytest** and **GitHub Actions**.
- **Lifespan Management:** Modern FastAPI lifespan handlers for safe database initialization.

## 🏗️ Technical Architecture

1. **FastAPI & SQLModel:** Handles persistence and RESTful access to price data.
2. **Stealth Scrapers:** Uses randomized viewports and human-like headers to bypass bot detection.
3. **Background Worker:** Decoupled scraping tasks to ensure high API availability.
4. **Engine Logic (Pending):** Calculates the "Arbitrage Signal" based on historical price averages and inventory levels.

## 🛠️ Installation & Setup

This project uses [uv](https://github.com/astral-sh/uv) for high-performance Python management.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ram-arbitrage-bot.git
   cd ram-arbitrage-bot
   ```

2. **Initialize the environment & install dependencies:**

   ```bash
   # uv will automatically create the .venv and install from pyproject.toml
   uv sync

   # Install the necessary Playwright browser engine
   uv run playwright install chromium
   ```

3. **Run the Heartbeat (Development Server):**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## 📡 API Endpoints

| Method | Endpoint          | Description                                              |
| :----- | :---------------- | :------------------------------------------------------- |
| `POST` | `/scan?url={url}` | Trigger a background scrape for Newegg/Amazon.           |
| `GET`  | `/results`        | Query historical price points from the database.         |
| `GET`  | `/arbitrage`      | (In Dev) Identify price discrepancies between retailers. |

## 🗺️ Roadmap

- [x] **Phase 1:** Initial FastAPI Heartbeat & Base Scraper.
- [x] **Phase 2:** CSS Selectors for Newegg & Amazon (Stealth Mode).
- [x] **Phase 3:** SQLModel persistence & Unit Testing suite.
- [ ] **Phase 4:** Regex-based Model Number extraction for 100% match accuracy.
- [ ] **Phase 5:** "Arbitrage Alert" notifications and Price-Velocity dashboard.
- [ ] **Phase 6:** Build a React/Next.js dashboard for visual price-velocity tracking.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.
