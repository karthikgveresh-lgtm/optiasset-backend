"""
Main Application Module
"""

from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db
import employees, assets, assignments, dashboard, models, schemas
from seed import seed_data

# --- EMERGENCY DATABASE MIGRATION ---
# This block ensures the 'password' column exists in the database
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE employees ADD COLUMN password TEXT DEFAULT 'password123'"))
        conn.commit()
        print("✅ Migration Successful: Added 'password' column.")
    except Exception:
        # If the column already exists, this will fail silently (which is fine)
        print("ℹ️ Migration Skipped: Column might already exist.")

# Create all database tables (for any completely new tables)
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

# REAL LOGIN ENDPOINT
@app.post("/api/auth/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    
    user = db.query(models.Employee).filter(models.Employee.email == email).first()
    
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Get role name
    role_name = "Employee"
    if user.role:
        role_name = user.role.name
    elif user.id == 1: # Fallback for our first admin
        role_name = "Admin"
        
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": role_name,
        "token": f"bearer_{user.id}"
    }

@app.get("/api/seed")
def trigger_seed():
    seed_data()
    return {"message": "Database seeded successfully with dummy data!"}

@app.get("/api/debug/employees")
def debug_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()
