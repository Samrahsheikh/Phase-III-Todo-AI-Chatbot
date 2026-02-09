from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from passlib.context import CryptContext
from pydantic import BaseModel

from models.user import User
from core.db import get_session
from services.auth_service import create_user_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# =========================
# Pydantic Models
# =========================

class UserSignup(BaseModel):
    email: str
    password: str
    name: str | None = None


class UserSignin(BaseModel):
    email: str
    password: str


# =========================
# Helper
# =========================

def truncate_password(password: str) -> str:
    """bcrypt max 72 bytes safe"""
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


# =========================
# Signup
# =========================

@router.post("/signup")
def signup(user: UserSignup, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(truncate_password(user.password))

    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "id": str(new_user.id),
        "email": new_user.email,
        "name": new_user.name
    }


# =========================
# Signin
# =========================

@router.post("/signin")
def signin(user: UserSignin, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()

    if not db_user or not pwd_context.verify(
        truncate_password(user.password),
        db_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_user_access_token(db_user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
