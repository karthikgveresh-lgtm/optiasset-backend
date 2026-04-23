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
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE employees ADD COLUMN password TEXT DEFAULT 'password123'"))
        conn.commit()
    except Exception:
        pass

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AssetTracker Pro API", version="1.0.0")

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

@app.post("/api/auth/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    
    print(f"🔍 Login Attempt: {email}") # DEBUG LOG
    
    user = db.query(models.Employee).filter(models.Employee.email == email).first()
    
    if not user:
        print(f"❌ User not found: {email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if user.password != password:
        print(f"❌ Password mismatch for {email}. Expected '{user.password}', got '{password}'")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    role_name = "Employee"
    if user.role:
        role_name = user.role.name
    elif user.id == 1:
        role_name = "Admin"
        
    print(f"✅ Login Success: {email} ({role_name})")
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
