import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from schemas import SignupRequest
from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(
    request: SignupRequest,
    db: sqlite3.Connection = Depends(get_db)
):
    existing_user = db.execute(
        "SELECT id FROM users WHERE email = ?",
        (request.email,)
    ).fetchone()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    password_hash = hash_password(request.password)

    cursor = db.execute(
        """
        INSERT INTO users (email, password_hash)
        VALUES (?, ?)
        """,
        (request.email, password_hash)
    )

    db.commit()

    user_id = cursor.lastrowid

    token = create_access_token(user_id)

    return {
        "message": "Signup successful",
        "user_id": user_id,
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: sqlite3.Connection = Depends(get_db)
):
    user = db.execute(
        """
        SELECT id, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (form_data.username,)
    ).fetchone()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user["id"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }