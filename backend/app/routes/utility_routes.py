import logging
import requests
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import get_user_from_session
from app.config import APP_ENV

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/status", response_class=HTMLResponse)
def status(request: Request):
    user = get_user_from_session(request)
    return templates.TemplateResponse(
        "status.html",
        {"request": request, "user": user, "env": APP_ENV, "python": "3.11", "service": "backend"},
    )


@router.get("/resources/import", response_class=HTMLResponse)
def import_resource_get(request: Request, url: str = ""):
    user = get_user_from_session(request)
    body = ""
    error = ""
    if url:
        try:
            r = requests.get(url, timeout=5)
            body = r.text[:2000]
        except Exception as exc:
            error = str(exc)
    return templates.TemplateResponse(
        "resource_import.html",
        {"request": request, "user": user, "body": body, "url": url, "error": error},
    )


@router.post("/resources/import", response_class=HTMLResponse)
def import_resource_post(request: Request, url: str = Form(...)):
    return import_resource_get(request, url)


@router.get("/error", response_class=HTMLResponse)
def trigger_error(request: Request):
    try:
        x = 1 / 0
        return {"x": x}
    except Exception:
        logger.exception("Unhandled error on /error")
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "details": "An internal error occurred. Please try again later"},
            status_code=500,
        )