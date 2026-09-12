# Expense Agent

An AI agent that manages your expenses through natural language — instead of clicking through a UI or calling API endpoints manually, you just tell it what to do.

**Examples:**
- "Add 300 for movies and 150 for snacks"
- "What's my total spending on groceries?"

## How it works

The agent doesn't touch the database directly. It only *decides* what should happen; a separate execution step actually does it. That separation is the core idea behind an "agent" as opposed to a plain chatbot.

```
User message
   ↓
LLM (Groq) reads the message + available tools, decides what to call
   ↓
Python code executes the chosen tool(s)
   ↓
Tool sends a request to the FastAPI backend
   ↓
FastAPI reads/writes SQLite, returns a result
   ↓
Result is fed back to the LLM
   ↓
LLM turns the result into a natural-language reply
```

If a request needs multiple steps (e.g. two expenses in one sentence), the agent loops — executing tools and checking back with the LLM — until it gets a final text answer instead of another tool call.

## Tech stack

- **LangChain** — tool-calling orchestration, message handling
- **Groq (`openai/gpt-oss-120b`)** — the LLM, via free-tier API
- **FastAPI** — backend API (add expenses, query totals)
- **SQLite** + SQLAlchemy — storage
- **Pydantic** — schema validation for tool arguments
- **Streamlit** — chat UI (optional; also runnable from the terminal)

## Project structure

This project has two parts, in separate folders:

```
expense-tracker-api/     # FastAPI backend
├── main.py               # API routes (add expense, get totals, etc.)
├── requirements.txt
└── expenses.db            # SQLite database (created on first run)

ai-agent/                 # The agent
├── main.py                # Terminal version of the agent
├── stream.py               # Streamlit UI version
├── requirements.txt
└── .env                    # GROQ_API_KEY (not committed)
```

Adjust the folder names above to match your actual repo layout.

## Setup

**1. Start the backend API:**
```
cd expense-tracker-api
pip install -r requirements.txt
uvicorn main:app --reload
```
Leave this running — it needs to stay up while you use the agent.

**2. In a separate terminal, set up and run the agent:**
```
cd ai-agent
pip install -r requirements.txt
```
Create a `.env` file inside `ai-agent/` with your Groq API key:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

Then run either version:
- Terminal chat: `python main.py`
- Web UI: `streamlit run stream.py`

## What I'd improve with more time

- Persist conversation history across sessions (currently resets on restart)
- Authentication on the API
- More tools (edit/delete expenses, spending trends over time)