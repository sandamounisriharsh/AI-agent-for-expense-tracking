import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from schemas import ExpenseCreate, ExpenseUpdate
from dependencies.auth import get_current_user


from services.expense_service import (
    create_expense,
    get_user_expenses,
    get_user_total,
    delete_expense,
    get_dashboard_stats,
    update_expense,
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("")
def add_expense(
    expense: ExpenseCreate,
    user_id: int = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    new_expense = create_expense(
        db=db,
        user_id=user_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description
    )

    return dict(new_expense)


@router.get("")
def get_expenses(
    category: str | None = None,
    user_id: int = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    expenses = get_user_expenses(
        db=db,
        user_id=user_id,
        category=category
    )

    return [dict(expense) for expense in expenses]


@router.get("/total")
def get_total(
    category: str | None = None,
    user_id: int = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    total = get_user_total(
        db=db,
        user_id=user_id,
        category=category
    )

    return {
        "category": category or "all",
        "total": total
    }


@router.get("/dashboard")
def dashboard(
    user_id: int = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    return get_dashboard_stats(
        db=db,
        user_id=user_id
    )

@router.patch("/{expense_id}")
def edit_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    user_id: int = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    updated = update_expense(
        db=db,
        user_id=user_id,
        expense_id=expense_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return dict(updated)

@router.delete("/{expense_id}")
def remove_expense(
    expense_id: int,
    user_id: int = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    deleted = delete_expense(
        db=db,
        user_id=user_id,
        expense_id=expense_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }

