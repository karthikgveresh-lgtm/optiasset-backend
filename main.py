"""
Main Application Module (Ultimate Stability Fix)
"""

import time
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db
import employees, assets, assignments, dashboard, models, schemas
from seed import seed_data

# --- EMERGENCY DATABASE MIGRATION ---
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE employees ADD COLUMN password TEXT DEFAULT 'password123'"))
        conn.commit()
    except Exception:
        pass

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OptiAsset API", version="1.5.0")

# ENHANCED CORS: Allowing everything specifically to stop those 0 numbers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"status": "OptiAsset API is Online"}

@app.post("/api/auth/signup")
def signup(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    requested_role = data.get("role", "Employee")
    
    # Check if user already exists
    existing_user = db.query(models.Employee).filter(models.Employee.email == email).first()
    if existing_user:
        # If they already exist, just update their role and password instead of failing
        existing_user.password = password
        db.commit()
        return {"message": "Account updated successfully!", "id": existing_user.id}
    
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()

    assigned_role_id = emp_role.id if emp_role else None
    if requested_role == "Admin" or email.lower() == "karthikgveresh@gmail.com":
        assigned_role_id = admin_role.id if admin_role else None

    # UNIQUE CODE: Added timestamp to prevent "Already Exists" 400 errors
    unique_code = f"EMP-{int(time.time()) % 100000}"

    new_user = models.Employee(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        employee_code=unique_code,
        department="Staff",
        role_id=assigned_role_id,
        is_active=True
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "Account created successfully!", "id": new_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/auth/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    
    user = db.query(models.Employee).filter(models.Employee.email == email).first()
    
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    role_name = "Employee"
    if user.role:
        role_name = user.role.name
    if email.lower() == "karthikgveresh@gmail.com":
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
    return {"message": "Database seeded successfully!"}
