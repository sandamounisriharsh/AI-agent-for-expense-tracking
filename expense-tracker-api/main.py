from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


from database import init_db
from routers.auth import router as auth_router
from dependencies.auth import get_current_user
from routers.expenses import router as expenses_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Expense Tracker API",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8001",
        "https://ai-agent-for-expense-tracking.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(expenses_router)


@app.get("/")
def root():
    return {
        "message": "Expense Tracker API is running"
    }


@app.get("/test-auth")
def test_auth(
    user_id: int = Depends(get_current_user)
):
    return {
        "message": "Authentication successful",
        "user_id": user_id
    }