from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import run_query, get_conn
from app.auth import get_user_from_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/admin", response_class=HTMLResponse)
def admin_home(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    if user["role"] not in ["admin", "teacher", "ta"]:
        return RedirectResponse("/dashboard", status_code=302)

    users_count = run_query("SELECT COUNT(*) as c FROM users", fetchone=True)
    submissions_count = run_query("SELECT COUNT(*) as c FROM submissions", fetchone=True)
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": user,
            "users_count": users_count["c"],
            "submissions_count": submissions_count["c"],
        },
    )


@router.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    if user["role"] not in ["admin", "teacher", "ta"]:
        return HTMLResponse("Forbidden", status_code=403)
    
    users = run_query("SELECT id, email, full_name, role FROM users ORDER BY id", fetchall=True)
    return templates.TemplateResponse("admin_users.html", {"request": request, "user": user, "users": users})

@router.post("/admin/users/{user_id}/role")
def update_role(request: Request, user_id: int, role: str = Form(...)):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    if user["role"] != "admin":
        return HTMLResponse("Forbidden", status_code=403)

    if role not in ["admin", "teacher", "ta", "student"]:
        return HTMLResponse("Invalid role", status_code=400)

    run_query(
        "UPDATE users SET role=%s WHERE id=%s",
        (role, user_id),
        commit=True,
    )

    return RedirectResponse("/admin/users", status_code=302)

@router.get("/admin/grades", response_class=HTMLResponse)
def admin_grades(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    if user["role"] not in ["admin", "teacher", "ta"]:
        return HTMLResponse("Forbidden", status_code=403)


    grades = run_query(
        """
        SELECT g.id, u.full_name as student_name, a.title as assignment_title, g.grade_value, g.feedback
        FROM grades g
        JOIN users u ON u.id = g.student_id
        JOIN assignments a ON a.id = g.assignment_id
        ORDER BY g.id DESC
        """,
        fetchall=True,
    )
    return templates.TemplateResponse("admin_grades.html", {"request": request, "user": user, "grades": grades})

@router.post("/admin/grades/{grade_id}/update")
def update_grade(
    request: Request,
    grade_id: int,
    grade_value: str = Form(...),
    feedback: str = Form(...),
):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    if user["role"] not in ["admin", "teacher", "ta"]:
        return HTMLResponse("Forbidden", status_code=403)

    run_query(
        "UPDATE grades SET grade_value=%s, feedback=%s, status='published' WHERE id=%s",
        (grade_value, feedback, grade_id),
        commit=True,
    )

    return RedirectResponse("/admin/grades", status_code=302)


@router.get("/admin/search-users", response_class=HTMLResponse)
def search_users(request: Request, q: str = ""):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    sql = f"SELECT id, email, full_name, role FROM users WHERE email ILIKE '%{q}%' OR full_name ILIKE '%{q}%'"
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            users = [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()

    return templates.TemplateResponse("admin_users.html", {"request": request, "user": user, "users": users, "q": q})



