# app/main.py

from fastapi import FastAPI
from app.core.config import API_TITLE, API_DESCRIPTION, API_VERSION
from app.routers import event_router, user_router, email_logs_router # Import routers

# --- FastAPI App Initialization ---
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# --- Include Routers ---
app.include_router(user_router.router)
app.include_router(event_router.router)
app.include_router(email_logs_router.router)  # Assuming you have an email router

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the User and Event Management API!"}