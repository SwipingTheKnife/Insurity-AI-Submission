import os

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Dashboard"})