from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import (
    auth_routes,
    profile_routes,
    course_routes,
    assignment_routes,
    grade_routes,
    message_routes,
    admin_routes,
    utility_routes,
)

app = FastAPI(title="DAT250 SecureApp", debug=False, docs_url=None, redoc_url=None, openapi_url=None)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.include_router(auth_routes.router)
app.include_router(profile_routes.router)
app.include_router(course_routes.router)
app.include_router(assignment_routes.router)
app.include_router(grade_routes.router)
app.include_router(message_routes.router)
app.include_router(admin_routes.router)
app.include_router(utility_routes.router)