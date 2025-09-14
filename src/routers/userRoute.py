import os
from datetime import timedelta, datetime
from urllib import request

from fastapi import Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.db_conn import engine, SessionLocal, get_db
from src.models.user_model import Base, User

import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


router = APIRouter()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))


@router.post("/register")
def register_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)   # ✅ inject DB session properly
):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})

    # Hash password
    hashed_password = pwd_context.hash(password)

    # Create user
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()

    # Redirect to login or dashboard
    return RedirectResponse(url="/", status_code=303)

@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register User"})


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
       return templates.TemplateResponse("index.html", {"request": {}, "error": "Invalid username or password"})

    if not pwd_context.verify(password, user.password_hash):
        return templates.TemplateResponse("index.html", {"request": {}, "error": "Invalid username or password"})

    access_token = create_access_token(data={"sub": str(user.user_id)})
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # JS cannot read it, safer
        max_age=3600,  # 1 hour
        secure=False,  # set True if using HTTPS
        samesite="lax"
    )

    return response