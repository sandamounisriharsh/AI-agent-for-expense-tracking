from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str

class ExpenseUpdate(BaseModel):
    amount: float | None = None
    category: str | None = None
    description: str | None = None