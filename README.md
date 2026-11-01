# ✈️ Multi-Agent AI Travel Booking System

An autonomous multi-agent travel orchestration pipeline built using **LangGraph**, **Groq API** (`openai/gpt-oss-120b`), **PostgreSQL**, and **Streamlit**.

The system coordinates specialized AI agents to search flights, accommodation options, and local attractions, compiling a complete day-by-day travel itinerary while strictly adhering to user budget limits (e.g., PKR 150,000).

---
## 🖼️ Application Interface
![AI Travel Booking System UI](assets/app_preview.png)

---
## 🌟 Key Features

- **Multi-Agent Architecture:** Powered by a 4-agent state graph (`Flight Agent` ✈️ → `Hotel Agent` 🏨 → `Itinerary Agent` 🗺️ → `Final Agent` 🏁).
- **State Persistence & Thread Isolation:** Uses **PostgreSQL** (`PostgresSaver`) to persist session state across runs while isolating thread contexts (`thread_id`).
- **High-Speed Execution:** Built on **Groq Cloud API** using `openai/gpt-oss-120b` for structured tool calling and prompt guardrails.
- **Interactive Streamlit UI:** Displays execution metrics, individual agent intermediate outputs in dedicated tabs, quick-selection prompt presets, and automated `.txt` itinerary downloads.

---

## 🛠️ Tech Stack

- **Framework:** LangGraph, LangChain
- **LLM Provider:** Groq API (`openai/gpt-oss-120b`)
- **Database:** PostgreSQL (Checkpointer)
- **Frontend UI:** Streamlit
- **Tools / Search:** Tavily API, AviationStack API
- **Language:** Python 3.14

---

## 🏗️ Architecture Flow

```text
[User Input] 
     │
     ▼
[Flight Agent] ──(Flight Results)──► [Hotel Agent] ──(Hotel Results)──► [Itinerary Agent] ──► [Final Agent] ──► [Streamlit UI]
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/Multi_Agent_Travel_System.git](https://https://github.com/ArujFatima/Multi_Agent_Travel_System.git)
cd Multi_Agent_Travel_System
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv langgraph_env1
# On Windows PowerShell:
.\langgraph_env1\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your API credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
Database_URL=postgresql://postgres:your_password@localhost:5432/your_db_name
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📜 License
Distributed under the MIT License.