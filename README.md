# 📉 RAM Arbitrage Bot (RAB)
### *Hedge against the global memory shortage with algorithmic procurement.*

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package_Manager-de5d43?logo=rust)](https://github.com/astral-sh/uv)
[![Playwright](https://img.shields.io/badge/Playwright-Scraping-2e8b57?logo=playwright)](https://playwright.dev/)

## 🚀 Overview
Due to the 2026 surge in AI datacenter demands, global RAM manufacturing has shifted toward High-Bandwidth Memory (HBM), causing a structural shortage in the consumer market. 

**RAB** is a specialized price-tracking and arbitrage engine designed to monitor "Spot-Market" volatility across major retailers. It utilizes asynchronous scrapers to identify undervalued inventory and trigger buy signals before retail prices adjust to wholesale spikes.

---

## ✨ Key Features
* **Asynchronous Scraping:** Powered by Playwright to handle JavaScript-heavy retail sites without blocking the API.
* **Background Processing:** Uses FastAPI `BackgroundTasks` to perform deep-scans while maintaining a responsive UI/API.
* **Modern Tooling:** Built with **uv** for lightning-fast dependency resolution and virtual environment management.
* **Scalable Core:** Modular scraper architecture allowing for easy integration of new retailers (Newegg, Amazon, MicroCenter).

---

## 🏗️ Technical Architecture

1.  **FastAPI Entry Point:** Receives scan requests and provides results via REST endpoints.
2.  **Scraper Base:** An extensible class that manages browser contexts and anti-detection headers.
3.  **Engine Logic (Pending):** Calculates the "Arbitrage Signal" based on historical price averages and inventory levels.

---

## 🛠️ Installation & Setup

This project uses [uv](https://github.com/astral-sh/uv) for high-performance Python management.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/ram-arbitrage-bot.git](https://github.com/yourusername/ram-arbitrage-bot.git)
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
---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Check bot status. |
| `POST` | `/scan?url={url}` | Trigger a background price scrape. |
| `GET` | `/results` | View all successfully scraped data points. |

---

## 🗺️ Roadmap
- [x] **Phase 1:** Initial FastAPI Heartbeat & Base Scraper.
- [ ] **Phase 2:** Implement CSS Selectors for Newegg/Amazon price extraction.
- [ ] **Phase 3:** Integrate SQLAlchemy (SQLite/Postgres) for price history persistence.
- [ ] **Phase 4:** Add "Arbitrage Alert" notifications via Discord/Telegram.
- [ ] **Phase 5:** Build a React/Next.js dashboard for visual price-velocity tracking.

## 📄 License
MIT License - See [LICENSE](LICENSE) for details.