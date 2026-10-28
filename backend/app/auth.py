import hashlib
import logging
import secrets
import time
from collections import defaultdict
from fastapi import Request
from app.database import run_query

logger = logging.getLogger("auth")

# --- Login rate limiting (fix for: Credential brute force, /login) ---
# In-memory per-email failed-attempt tracker. Resets on app restart; for a
# real deployment this would move to Redis/DB, but this is enough to stop
# the unthrottled Hydra brute force demonstrated in Assignment 1.
LOGIN_ATTEMPT_WINDOW_SECONDS = 60
LOGIN_MAX_ATTEMPTS = 5

_failed_login_attempts = defaultdict(list)


def _prune_old_attempts(email: str) -> list:
    now = time.time()
    recent = [t for t in _failed_login_attempts[email] if now - t < LOGIN_ATTEMPT_WINDOW_SECONDS]
    _failed_login_attempts[email] = recent
    return recent


def is_login_locked(email: str) -> bool:
    return len(_prune_old_attempts(email)) >= LOGIN_MAX_ATTEMPTS


def record_failed_login(email: str):
    recent = _prune_old_attempts(email)
    recent.append(time.time())
    _failed_login_attempts[email] = recent
    logger.warning(
        "Failed login attempt for %s (%d in last %ds)",
        email, len(recent), LOGIN_ATTEMPT_WINDOW_SECONDS,
    )


def clear_failed_logins(email: str):
    _failed_login_attempts.pop(email, None)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_session(user_id: int) -> str:
    token = secrets.token_hex(16)
    run_query(
        "INSERT INTO sessions (user_id, session_token) VALUES (%s, %s)",
        (user_id, token),
        commit=True,
    )
    return token


def get_user_from_session(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    session = run_query(
        """
        SELECT u.* FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.session_token = %s
        """,
        (session_token,),
        fetchone=True,
    )
    return session


def clear_session(token: str):
    run_query("DELETE FROM sessions WHERE session_token = %s", (token,), commit=True)
