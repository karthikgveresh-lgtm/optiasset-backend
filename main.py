"""
Main Application Module (Signup Edition)
"""

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

app = FastAPI(title="OptiAsset API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"status": "OptiAsset API is Online"}

# --- AUTH ENDPOINTS ---

@app.post("/api/auth/signup")
def signup(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    
    # Check if user already exists
    existing_user = db.query(models.Employee).filter(models.Employee.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Account already exists with this email")
    
    # Create new Employee
    new_user = models.Employee(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        employee_code=f"EMP-{email.split('@')[0]}", # Auto-generate code
        department="Unassigned",
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Account created successfully!", "id": new_user.id}

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
    elif user.id == 1:
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
