
![Image](https://github.com/user-attachments/assets/e755fdde-725d-4a8a-9ec4-c55b8164ad87)

# ⚡ PULSE ARCHITECT | Sovereign AI Ecosystem
### *Autonomous Risk Management & ESG Optimization Engine*

---

## 🚀 Overview
**PulseArchitect** is an advanced AI-driven ecosystem developed for the **IBM Dev Day: AI Demystified Hackathon (2026)**. It bridges the gap between autonomous risk identification and environmental sustainability. By utilizing the **IBM Granite** family of models and **DataStax Astra DB**, PulseArchitect doesn't just analyze data—it governs it with a "Sovereign" mindset.

> **Hackathon Submission:** This project was built to demonstrate the practical application of AI agents in high-stakes corporate environments, focusing on transparency, efficiency, and resource preservation.

---

## 🛡️ Core Philosophy: Why "Sovereign"?
In a world of bloated AI models, **PulseArchitect** follows a "Resource-First" philosophy. It utilizes **Dynamic Gear Shifting** between **IBM Granite 8B (Power Mode)** and **Granite 2B (Eco Mode)** to ensure that every token processed is optimized for its environmental impact (Water & Energy). 

---

## ⚡ Key Features

* **🕵️ Autonomous Risk Detection:** Continuously monitors data streams and PDF documents via a watchdog worker to identify corporate threats in real-time.
* **🎫 Sovereign Ticket Sealing:** Automatically converts detected risks into immutable "Sovereign Tickets" stored in **Astra DB**.
* **🌍 Real-time ESG Reporting:** Every AI analysis calculates and displays live Water (L) and Energy (kWh) consumption metrics.
* **🏎️ AI Engine Gear Indicator:** Visual dashboard feedback on which Granite model is currently powering the system.
* **🛡️ Sovereign Memory:** A persistent activity feed that maintains the latest 7 otonomous analyses across sessions.

---

## 🛠️ The Tech Stack

* **LLM:** [IBM Granite 3.0 Series](https://www.ibm.com/granite) (8B-Instruct & 2B-Instruct).
* **Orchestration:** [BeeAI Framework](https://i-am-bee.github.io/beeai-framework/) by IBM.
* **Database:** [DataStax Astra DB](https://astra.datastax.com/) (Vector Search & NoSQL storage).
* **Backend:** FastAPI (Python 3.11).
* **Infrastructure:** IBM Watsonx.ai & Watsonx.data.

---

## ⚠️ A Sincere Disclosure
As a Computer Engineering student (1st Year), I utilized AI as a co-pilot to accelerate the development of this prototype. While the core logic is operational, **PulseArchitect v0.1.0** is still in beta. 
* **Beta Status:** You may encounter minor inconsistencies in data sorting or UI synchronization.
* **Known Bugs:** The "Water Bar" visualization and "Ticket Feed" are under continuous optimization for Astra DB latency.

---

## 🗺️ Roadmap (Future Vision)
- [ ] **RAG Integration:** Deep-memory document retrieval for zero-hallucination analysis.
- [ ] **Q-ADAPTIVE:** Post-quantum cryptography (PQC) layer for ticket security.
- [ ] **Watsonx.governance:** Full audit trails for every AI-driven corporate decision.

---

## ⚙️ Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yorulmazkagan/PulseArchitect.git](https://github.com/yorulmazkagan/PulseArchitect.git)
    cd PulseArchitect
    ```
2.  **Environment Variables:** Create a `.env` file (see `.env.example`).
3.  **Deploy Backend:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload
    ```
4.  **Launch Watchdog:**
    ```bash
    python scripts/watchdog_worker.py
    ```

---

**Developed by [Kağan Yorulmaz](https://www.yorulmazkagan.com)**
*Building the future of Sovereign AI, one token at a time.*
