"""
Database Seeding Script (SQL Hammer Version)
Uses direct SQL to ensure passwords are set correctly.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine, Base
import models
from datetime import date

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # 1. Get or Create Roles
        admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
        if not admin_role:
            admin_role = models.Role(name="Admin", permissions=["*"])
            db.add(admin_role)
            db.flush()

        emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
        if not emp_role:
            emp_role = models.Role(name="Employee", permissions=["view:own_assets"])
            db.add(emp_role)
            db.flush()

        db.commit()

        # 2. Force Add/Update YOU as the Super-Admin
        # We use raw SQL to be 100% sure the column is written correctly
        db.execute(text("""
            INSERT OR REPLACE INTO employees (id, employee_code, first_name, last_name, email, password, department, role_id, is_active)
            VALUES (1, 'ADMIN-001', 'Karthik', 'Veresh', 'karthikgveresh@gmail.com', 'password123', 'Management', :role_id, 1)
        """), {"role_id": admin_role.id})
        
        db.commit()
        print("✅ SQL Hammer: Super-Admin karthikgveresh@gmail.com forced with password 'password123'")

    except Exception as e:
        print(f"❌ Error during SQL seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
