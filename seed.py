"""
Database Seeding Script (Smarter Version)
Populates the OptiAsset database while avoiding duplicate errors.
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
            db.flush() # Get ID without committing

        emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
        if not emp_role:
            emp_role = models.Role(name="Employee", permissions=["view:own_assets"])
            db.add(emp_role)
            db.flush()

        db.commit()

        # 2. Add Employees (if not already there)
        if db.query(models.Employee).count() == 0:
            employees = [
                models.Employee(employee_code="EMP-001", first_name="Karthik", last_name="Veresh", email="karthik@optiasset.com", department="Engineering", role_id=admin_role.id),
                models.Employee(employee_code="EMP-002", first_name="Jane", last_name="Smith", email="jane@optiasset.com", department="Human Resources", role_id=emp_role.id),
                models.Employee(employee_code="EMP-003", first_name="Mike", last_name="Ross", email="mike@optiasset.com", department="Legal", role_id=emp_role.id),
            ]
            db.add_all(employees)
            db.commit()

        # 3. Add Assets (if not already there)
        if db.query(models.Asset).count() == 0:
            assets = [
                models.Asset(asset_tag="LAP-001", name="MacBook Pro 16\"", category="Laptop", serial_number="SN-X123", status="Assigned"),
                models.Asset(asset_tag="LAP-002", name="MacBook Air M2", category="Laptop", serial_number="SN-M202", status="Available"),
                models.Asset(asset_tag="MON-001", name="Dell UltraSharp 27\"", category="Monitor", serial_number="SN-D789", status="Assigned"),
                models.Asset(asset_tag="MOB-001", name="iPhone 15 Pro", category="Mobile", serial_number="SN-I555", status="Available"),
                models.Asset(asset_tag="LAP-003", name="Lenovo ThinkPad X1", category="Laptop", serial_number="SN-L009", status="Maintenance"),
            ]
            db.add_all(assets)
            db.commit()

        # 4. Add Assignments (if not already there)
        if db.query(models.AssetAssignment).count() == 0:
            # Re-fetch to get IDs
            karthik = db.query(models.Employee).filter(models.Employee.employee_code == "EMP-001").first()
            jane = db.query(models.Employee).filter(models.Employee.employee_code == "EMP-002").first()
            macbook = db.query(models.Asset).filter(models.Asset.asset_tag == "LAP-001").first()
            monitor = db.query(models.Asset).filter(models.Asset.asset_tag == "MON-001").first()

            if karthik and macbook:
                db.add(models.AssetAssignment(asset_id=macbook.id, employee_id=karthik.id, assigned_by_id=1, assignment_date=date.today(), status="Active"))
            if jane and monitor:
                db.add(models.AssetAssignment(asset_id=monitor.id, employee_id=jane.id, assigned_by_id=1, assignment_date=date.today(), status="Active"))
            
            db.commit()

        print("✅ Database check complete! All data is present.")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
