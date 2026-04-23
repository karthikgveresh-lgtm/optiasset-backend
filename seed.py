"""
Database Seeding Script (Super-Admin Version)
Ensures YOU are the primary Admin in the system.
"""

from sqlalchemy.orm import Session
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

        # 2. Add YOU as the Super-Admin
        me = db.query(models.Employee).filter(models.Employee.email == "karthikgveresh@gmail.com").first()
        if not me:
            me = models.Employee(
                employee_code="ADMIN-001", 
                first_name="Karthik", 
                last_name="Veresh", 
                email="karthikgveresh@gmail.com", 
                password="password123", # Your new secure password
                department="Management", 
                role_id=admin_role.id
            )
            db.add(me)
        else:
            # Ensure the password is set correctly even if the user exists
            me.password = "password123"
            me.role_id = admin_role.id
        
        # 3. Add Jane (Employee)
        jane = db.query(models.Employee).filter(models.Employee.employee_code == "EMP-002").first()
        if not jane:
            jane = models.Employee(
                employee_code="EMP-002", 
                first_name="Jane", 
                last_name="Smith", 
                email="jane@optiasset.com", 
                password="password123",
                department="Human Resources", 
                role_id=emp_role.id
            )
            db.add(jane)
        
        db.commit()
        db.refresh(me)

        # 4. Add some sample gear for you
        macbook = db.query(models.Asset).filter(models.Asset.asset_tag == "LAP-001").first()
        if not macbook:
            macbook = models.Asset(asset_tag="LAP-001", name="MacBook Pro 16\"", category="Laptop", status="Assigned")
            db.add(macbook)
            db.commit()
            db.refresh(macbook)

        asg = db.query(models.AssetAssignment).filter(models.AssetAssignment.employee_id == me.id).first()
        if not asg:
            db.add(models.AssetAssignment(asset_id=macbook.id, employee_id=me.id, assigned_by_id=me.id, assignment_date=date.today(), status="Active"))

        db.commit()
        print(f"✅ Success! Super-Admin {me.email} is ready.")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
