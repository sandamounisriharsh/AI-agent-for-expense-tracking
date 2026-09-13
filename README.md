# 💰 AI Expense Tracker

An AI-powered expense tracking application that allows users to manage their expenses through a modern web interface and interact with an AI agent using natural language.

The application combines **React, FastAPI, SQLite, LangChain, and Groq** to provide both traditional expense management and conversational AI capabilities.

---

## 🚀 Live Demo

### 🌐 Frontend  ###
https://ai-agent-for-expense-tracking.vercel.app

The frontend is deployed using **Vercel**.

---

## 🔗 Deployed Services

### 🗄️ Expense Tracker API
https://ai-agent-for-expense-tracking.onrender.com

### 📚 Expense API Documentation
https://ai-agent-for-expense-tracking.onrender.com/docs

### 🤖 AI Agent API
https://ai-agent-for-expense-tracking-1.onrender.com

### 📚 AI Agent Documentation
https://ai-agent-for-expense-tracking-1.onrender.com/docs

---

# ✨ Features

## 🔐 User Authentication

- User registration
- User login
- JWT-based authentication
- Protected expense operations
- User-specific expense data

---

## 💸 Expense Management

Users can:

- Add expenses
- View expenses
- Edit expenses
- Delete expenses
- Categorize expenses
- Add descriptions to expenses
- Track total spending

Each user's expenses are isolated from other users.

---

## 🤖 AI Expense Assistant

The application includes an AI assistant that understands natural-language expense requests.

Examples:

```text
How much have I spent?

What are my expenses?

I spent ₹500 on groceries.

Change my grocery expense to ₹700.

Delete my shopping expense.

The AI agent can interact with the expense API to perform supported operations.

🧠 Natural Language Interaction

Instead of requiring users to remember database IDs or exact commands, the AI assistant can understand natural descriptions.

For example:

Delete my grocery expense

instead of:

Delete expense with ID 14

The application keeps database IDs internal and provides a more natural conversational experience.

🛡️ Delete Confirmation

The AI assistant asks for confirmation before deleting an expense.

Example:

User:
Delete my grocery expense.

AI:
I found your grocery expense. Do you want me to delete it?

User:
Yes

This prevents accidental deletion.

📊 Expense Analytics

The AI assistant can analyze expense data and provide information such as:

Total spending
Average expense
Spending by category
Category percentages
Largest spending category
Largest individual expense

Example:

How much have I spent on food?
🏗️ System Architecture
                    ┌──────────────────────┐
                    │      React App       │
                    │       Vercel         │
                    └──────────┬───────────┘
                               │
                               │ HTTP / REST
                               ▼
                    ┌──────────────────────┐
                    │     AI Agent API     │
                    │ FastAPI + LangChain  │
                    │        + Groq        │
                    │       Render         │
                    └──────────┬───────────┘
                               │
                               │ Authenticated API
                               ▼
                    ┌──────────────────────┐
                    │   Expense Tracker    │
                    │        API           │
                    │       FastAPI        │
                    │       Render         │
                    └──────────┬───────────┘
                               │
                               │ SQL
                               ▼
                    ┌──────────────────────┐
                    │    SQLite Database   │
                    └──────────────────────┘
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
CSS
Fetch API
Backend
Python
FastAPI
SQLite
Raw SQL
Pydantic
JWT Authentication
AI
LangChain
LangChain Core
LangChain Groq
Groq
openai/gpt-oss-120b
Deployment
Vercel — Frontend
Render — Backend APIs
GitHub — Source Control
📁 Project Structure
AI-agent-for-expense-tracking/
│
├── expense-tracker-api/
│   ├── main.py
│   ├── database.py
│   ├── schema.sql
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── expenses.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── expense_service.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   └── requirements.txt
│
├── ai-agent/
│   ├── main.py
│   ├── api.py
│   ├── requirements.txt
│   │
│   └── prompts/
│       └── system_prompt.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentSection.jsx
│   │   │   ├── AnalyticsDashboard.jsx
│   │   │   ├── ChatBox.jsx
│   │   │   ├── ExpenseForm.jsx
│   │   │   ├── ExpenseList.jsx
│   │   │   ├── FeatureCard.jsx
│   │   │   ├── Features.jsx
│   │   │   ├── FloatingCard.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── Wallet.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── home.jsx
│   │   │   ├── login.jsx
│   │   │   └── signup.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
🔐 Authentication Flow

The application uses JWT authentication.

User
 │
 │ Login / Signup
 ▼
FastAPI Authentication API
 │
 │ JWT Token
 ▼
React Frontend
 │
 │ Authorization: Bearer <token>
 ▼
Protected API Endpoints

The JWT token is used by the frontend when communicating with the backend APIs.

🔄 AI Request Flow

When the user sends a message to the AI assistant:

User Message
      │
      ▼
React Chat Interface
      │
      ▼
AI Agent API
      │
      ▼
LangChain + Groq
      │
      ▼
AI determines required action
      │
      ├───────────────┐
      │               │
      ▼               ▼
Find / Analyze     Add / Edit / Delete
      │               │
      └───────┬───────┘
              ▼
       Expense Tracker API
              │
              ▼
          SQLite DB
              │
              ▼
        Result returned
              │
              ▼
        Natural AI Response
🔌 API Endpoints
Authentication

The Expense Tracker API provides authentication endpoints for:

User registration
User login
Token-based authentication
Expenses

Supported expense operations include:

GET    /expenses
POST   /expenses
PATCH  /expenses/{expense_id}
DELETE /expenses/{expense_id}

The exact request and response schemas can be explored through the Swagger documentation.

API Documentation

https://ai-agent-for-expense-tracking.onrender.com/docs

🤖 AI Agent API

The AI Agent exposes a chat endpoint:

POST /chat

The endpoint accepts a natural-language message and uses the authenticated user's token when interacting with the Expense Tracker API.

AI Agent Documentation

https://ai-agent-for-expense-tracking-1.onrender.com/docs

⚙️ Local Development
1. Clone the repository
git clone https://github.com/sandamounisriharsh/AI-agent-for-expense-tracking.git
cd AI-agent-for-expense-tracking
🗄️ Run the Expense Tracker API

Navigate to:

cd expense-tracker-api

Create a Python virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the API:

uvicorn main:app --reload --port 8000

The API will be available at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs
🤖 Run the AI Agent

Open another terminal.

Navigate to:

cd ai-agent

Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_groq_api_key
BASE_URL=http://localhost:8000

Start the AI Agent:

uvicorn api:app --reload --port 8001

The AI Agent will be available at:

http://localhost:8001

Swagger documentation:

http://localhost:8001/docs
🌐 Run the Frontend

Navigate to:

cd frontend

Install dependencies:

npm install

Create a .env file:

VITE_EXPENSE_API_URL=http://localhost:8000
VITE_AI_API_URL=http://localhost:8001

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
🔑 Environment Variables

The project uses environment variables for configuration and secrets.

AI Agent
GROQ_API_KEY=your_groq_api_key
BASE_URL=https://ai-agent-for-expense-tracking.onrender.com
Frontend
VITE_EXPENSE_API_URL=https://ai-agent-for-expense-tracking.onrender.com
VITE_AI_API_URL=https://ai-agent-for-expense-tracking-1.onrender.com
Important

Never commit API keys or .env files to GitHub.

The repository's .gitignore excludes .env files.

🚀 Deployment
Frontend

The React frontend is deployed on:

Vercel

https://ai-agent-for-expense-tracking.vercel.app
Backend

The Expense Tracker API is deployed on:

Render

https://ai-agent-for-expense-tracking.onrender.com
AI Agent

The AI Agent API is deployed on:

Render

https://ai-agent-for-expense-tracking-1.onrender.com
🧪 Example AI Commands

The AI assistant supports natural-language interactions such as:

Add an expense
I spent ₹500 on groceries.
View expenses
What are my expenses?
Check spending
How much have I spent?
Category analysis
How much did I spend on food?
Edit an expense
Change my grocery expense to ₹700.
Delete an expense
Delete my shopping expense.

The AI asks for confirmation before deleting an expense.

🔒 Security Considerations

The application includes several security-related practices:

JWT-based authentication
Protected expense endpoints
User-specific expense access
Password hashing
Environment variables for secrets
CORS configuration
SQL parameterization
Database foreign-key constraints
Delete confirmation through the AI assistant

API keys are not stored in the source code.

📈 Future Improvements

Possible future improvements include:

Persistent production database such as PostgreSQL
Persistent conversation history
More advanced expense analytics
Monthly and yearly spending analysis
Budget tracking
Expense visualizations
Recurring expenses
Export expenses to CSV/PDF
Improved AI intent handling
Production-grade conversation storage
Better monitoring and logging
⚠️ Deployment Note

The current deployment uses Render's Free plan.

Free Render services may spin down after periods of inactivity, which can cause the first request after inactivity to take longer.

The current application also uses SQLite, which is suitable for development and demonstration purposes but is not ideal for highly persistent production workloads.

👨‍💻 Author

Sri Harsh

GitHub:

https://github.com/sandamounisriharsh

📄 License

This project is available for educational and personal use.


### One thing I'd change before committing

Your README currently says **"raw SQL"**, which is accurate for your backend architecture, and I've kept it that way.

After replacing your current `README.md` with this, run:

```powershell
git add README.md
git commit -m "Update project README"
git push origin main
