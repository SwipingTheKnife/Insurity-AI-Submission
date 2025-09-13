import os
from urllib import request

from fastapi import FastAPI, Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.db_conn import engine, SessionLocal
from src.models.user_model import Base, User

router = APIRouter()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

    return templates.TemplateResponse("dashboard.html", {"request": {}, "title": "Dashboard"})