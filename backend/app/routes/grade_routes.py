from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import run_query
from app.auth import get_user_from_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/grades", response_class=HTMLResponse)
def grades(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    grade_rows = run_query(
        """
        SELECT g.*, a.title as assignment_title
        FROM grades g
        JOIN assignments a ON a.id = g.assignment_id
        WHERE g.student_id=%s
        ORDER BY g.id DESC
        """,
        (user["id"],),
        fetchall=True,
    )
    return templates.TemplateResponse("grades.html", {"request": request, "user": user, "grades": grade_rows})


@router.get("/grades/{grade_id}", response_class=HTMLResponse)
def grade_detail(request: Request, grade_id: int):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    # grade = run_query(
    #     """
    #     SELECT g.*, a.title as assignment_title, u.full_name as student_name
    #     FROM grades g
    #     JOIN assignments a ON a.id=g.assignment_id
    #     JOIN users u ON u.id=g.student_id
    #     WHERE g.id=%s
    #     """,
    #     (grade_id,),
    #     fetchone=True,
    # )

    grade = run_query(
             """
            SELECT g.*, a.title as assignment_title, u.full_name as student_name
             FROM grades g
             JOIN assignments a ON a.id=g.assignment_id
            JOIN users u ON u.id=g.student_id
             WHERE g.id=%s
             AND g.student_id = %s
             """,
             (grade_id,user["id"]),
            fetchone=True,
         )
    if grade is None:
        raise HTTPException(
             status_code=404,
             detail= "Grade not found",
         )

    return templates.TemplateResponse("grade_detail.html", {"request": request, "user": user, "grade": grade})
