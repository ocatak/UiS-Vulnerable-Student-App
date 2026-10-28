import os
from uuid import uuid4
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import run_query
from app.auth import get_user_from_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIR = "app/uploads"


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    courses = run_query(
        """
        SELECT c.* FROM courses c
        JOIN course_registrations cr ON cr.course_id = c.id
        WHERE cr.user_id = %s
        """,
        (user["id"],),
        fetchall=True,
    )
    messages = run_query(
        "SELECT * FROM messages WHERE recipient_id=%s ORDER BY created_at DESC LIMIT 5",
        (user["id"],),
        fetchall=True,
    )
    grades = run_query(
        "SELECT * FROM grades WHERE student_id=%s ORDER BY updated_at DESC LIMIT 5",
        (user["id"],),
        fetchall=True,
    )
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "courses": courses, "messages": messages, "grades": grades},
    )


@router.get("/profile", response_class=HTMLResponse)
def my_profile(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "profile": user})


@router.get("/profile/{user_id}", response_class=HTMLResponse)
def profile_by_id(request: Request, user_id: int):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    profile = run_query("SELECT * FROM users WHERE id=%s", (user_id,), fetchone=True)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "profile": profile})

@router.post("/profile/update")
def update_profile(
    request: Request,
    full_name: str = Form(""),
    phone: str = Form(""),
    address: str = Form(""),
    bio: str = Form(""),
):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    run_query(
        """
        UPDATE users
        SET full_name=%s, phone=%s, address=%s, bio=%s
        WHERE id=%s
        """,
        (full_name, phone, address, bio, user["id"]),
        commit=True,
    )

    return RedirectResponse(f"/profile/{user['id']}", status_code=302)



@router.post("/profile/avatar")
def upload_avatar(request: Request, avatar: UploadFile = File(...)):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"avatar_{user['id']}_{uuid4().hex}_{avatar.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(avatar.file.read())

    run_query("UPDATE users SET avatar_path=%s WHERE id=%s", (filename, user["id"]), commit=True)
    return RedirectResponse(f"/profile/{user['id']}", status_code=302)
