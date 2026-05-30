# 🚀 Horizon Automation Engine

An autonomous, resilient Market Intelligence Agent built for the Bright Data Hackathon. This platform uses a State Machine Graph architecture to securely scrape live web data via residential proxies and generate structured visual intelligence tables using Google Gemini 2.5 Flash.

## 🛠️ Tech Stack
- **Framework:** Streamlit (UI Dashboard Layout)
- **Agent Architecture:** Graph State Machine Logic (Self-Correction Router)
- **Web Scraping Infrastructure:** Bright Data SERP API Node & Residential Proxy Network
- **Cognitive Engine:** Google Gemini 2.5 Flash

## 📐 System Architecture Diagram
- **Node 1 (Guardrail Gate):** Inspects input query for injection attacks. Aborts graph on threat detection.
- **Node 2 (Scraper Proxy Node):** Tunnels requests safely. Includes an automatic fallback/retry loop mechanism if network timeouts occur.
- **Node 3 (LLM Analytics Node):** Converts messy HTML streams into Markdown visual matrices dynamically.

## 🚀 Quick Start
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd brightdata_hackathon