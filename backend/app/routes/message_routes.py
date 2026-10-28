from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import run_query
from app.auth import get_user_from_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/messages", response_class=HTMLResponse)
def messages(request: Request):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    inbox = run_query(
        """
        SELECT m.*, u.full_name as sender_name
        FROM messages m
        JOIN users u ON u.id = m.sender_id
        WHERE recipient_id=%s
        ORDER BY m.created_at DESC
        """,
        (user["id"],),
        fetchall=True,
    )
    users = run_query("SELECT id, full_name, email FROM users ORDER BY full_name", fetchall=True)
    return templates.TemplateResponse(
        "messages.html", {"request": request, "user": user, "messages": inbox, "users": users}
    )


@router.post("/messages")
def send_message(request: Request, recipient_id: int = Form(...), content: str = Form(...)):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    run_query(
        "INSERT INTO messages (sender_id, recipient_id, content) VALUES (%s, %s, %s)",
        (user["id"], recipient_id, content),
        commit=True,
    )
    return RedirectResponse("/messages", status_code=302)


@router.get("/messages/{message_id}", response_class=HTMLResponse)
def message_detail(request: Request, message_id: int):
    user = get_user_from_session(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    message = run_query(
        """
        SELECT m.*, s.full_name as sender_name, r.full_name as recipient_name
        FROM messages m
        JOIN users s ON s.id = m.sender_id
        JOIN users r ON r.id = m.recipient_id
        WHERE m.id=%s
        """,
        (message_id,),
        fetchone=True,
    )
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found.")
    
    if message["sender_id"] != user["id"] and message["recipient_id"] != user["id"]:
            raise HTTPException(
                status_code=403, 
                detail="You are not authorized to view this message."
                )
    
    return templates.TemplateResponse("message_detail.html", {"request": request, "user": user, "message": message})
