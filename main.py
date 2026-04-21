"""
Main Application Module

This is the entry point for the FastAPI application.
It initializes the app, creates the database tables (if they don't exist),
and includes all the sub-routers for different modules.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import employees, assets, assignments, dashboard

# Create all database tables based on our SQLAlchemy models
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app with metadata for Swagger UI
app = FastAPI(
    title="AssetTracker Pro API",
    description="An industrial-grade asset management system API. Built for tracking company assets across 1000+ employees.",
    version="1.0.0",
)

# Enable CORS for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the API routers
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint verifying the API is online.
    """
    return {"message": "Welcome to the AssetTracker Pro API! Navigate to /docs for the interactive documentation."}
