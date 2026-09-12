# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./expenses.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)

Base.metadata.create_all(bind=engine)
app = FastAPI()

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str

@app.post("/expenses")
def add_expense(expense: ExpenseCreate):
    db = SessionLocal()
    e = Expense(**expense.dict())
    db.add(e); db.commit(); db.refresh(e)
    return {"id": e.id, "amount": e.amount, "category": e.category}

@app.get("/expenses")
def get_expenses(category: str = None):
    db = SessionLocal()
    q = db.query(Expense)
    if category:
        q = q.filter(Expense.category == category)
    return [{"id": e.id, "amount": e.amount, "category": e.category, "description": e.description} for e in q.all()]

@app.get("/expenses/total")
def get_total(category: str = None):
    db = SessionLocal()
    q = db.query(Expense)
    if category:
        q = q.filter(Expense.category == category)
    total = sum(e.amount for e in q.all())
    return {"category": category or "all", "total": total}