"""
Main Application Module
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import employees, assets, assignments, dashboard, models
from seed import seed_data

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AssetTracker Pro API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"status": "OptiAsset API is Online", "version": "1.0.0"}

# MAGIC SEED ENDPOINT
@app.get("/api/seed")
def trigger_seed():
    seed_data()
    return {"message": "Database seeded successfully with dummy data!"}

# DEBUG ENDPOINT
@app.get("/api/debug/employees")
def debug_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()
