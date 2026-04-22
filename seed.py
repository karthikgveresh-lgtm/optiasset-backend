"""
Database Seeding Script (Forceful Version)
Ensures dummy gear is assigned regardless of existing data.
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

        # 2. Add Employees (If missing)
        karthik = db.query(models.Employee).filter(models.Employee.employee_code == "EMP-001").first()
        if not karthik:
            karthik = models.Employee(employee_code="EMP-001", first_name="Karthik", last_name="Veresh", email="karthik@optiasset.com", department="Engineering", role_id=admin_role.id)
            db.add(karthik)
        
        jane = db.query(models.Employee).filter(models.Employee.employee_code == "EMP-002").first()
        if not jane:
            jane = models.Employee(employee_code="EMP-002", first_name="Jane", last_name="Smith", email="jane@optiasset.com", department="Human Resources", role_id=emp_role.id)
            db.add(jane)
        
        db.commit()
        db.refresh(karthik)
        db.refresh(jane)

        # 3. Add Assets (If missing)
        macbook = db.query(models.Asset).filter(models.Asset.asset_tag == "LAP-001").first()
        if not macbook:
            macbook = models.Asset(asset_tag="LAP-001", name="MacBook Pro 16\"", category="Laptop", status="Assigned")
            db.add(macbook)

        monitor = db.query(models.Asset).filter(models.Asset.asset_tag == "MON-001").first()
        if not monitor:
            monitor = models.Asset(asset_tag="MON-001", name="Dell UltraSharp 27\"", category="Monitor", status="Assigned")
            db.add(monitor)
        
        db.commit()
        db.refresh(macbook)
        db.refresh(monitor)

        # 4. FORCE ASSIGNMENTS
        # Check if Karthik has the MacBook
        k_asg = db.query(models.AssetAssignment).filter(models.AssetAssignment.employee_id == karthik.id, models.AssetAssignment.asset_id == macbook.id).first()
        if not k_asg:
            db.add(models.AssetAssignment(asset_id=macbook.id, employee_id=karthik.id, assigned_by_id=1, assignment_date=date.today(), status="Active"))
        
        # Check if Jane has the Monitor
        j_asg = db.query(models.AssetAssignment).filter(models.AssetAssignment.employee_id == jane.id, models.AssetAssignment.asset_id == monitor.id).first()
        if not j_asg:
            db.add(models.AssetAssignment(asset_id=monitor.id, employee_id=jane.id, assigned_by_id=1, assignment_date=date.today(), status="Active"))

        db.commit()
        print("✅ Forceful seed complete! Gear should now be visible.")

    except Exception as e:
        print(f"❌ Error during forceful seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
