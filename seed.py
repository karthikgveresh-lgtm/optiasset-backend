"""
Database Seeding Script
Populates the OptiAsset database with dummy data for testing.
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
        # 1. Create Roles
        admin_role = models.Role(name="Admin", permissions=["*"])
        emp_role = models.Role(name="Employee", permissions=["view:own_assets"])
        db.add_all([admin_role, emp_role])
        db.commit()

        # 2. Create Employees
        employees = [
            models.Employee(employee_code="EMP-001", first_name="Karthik", last_name="Veresh", email="karthik@optiasset.com", department="Engineering", role_id=admin_role.id),
            models.Employee(employee_code="EMP-002", first_name="Jane", last_name="Smith", email="jane@optiasset.com", department="Human Resources", role_id=emp_role.id),
            models.Employee(employee_code="EMP-003", first_name="Mike", last_name="Ross", email="mike@optiasset.com", department="Legal", role_id=emp_role.id),
        ]
        db.add_all(employees)
        db.commit()

        # 3. Create Assets
        assets = [
            models.Asset(asset_tag="LAP-001", name="MacBook Pro 16\"", category="Laptop", serial_number="SN-X123", status="Assigned"),
            models.Asset(asset_tag="LAP-002", name="MacBook Air M2", category="Laptop", serial_number="SN-M202", status="Available"),
            models.Asset(asset_tag="MON-001", name="Dell UltraSharp 27\"", category="Monitor", serial_number="SN-D789", status="Assigned"),
            models.Asset(asset_tag="MOB-001", name="iPhone 15 Pro", category="Mobile", serial_number="SN-I555", status="Available"),
            models.Asset(asset_tag="LAP-003", name="Lenovo ThinkPad X1", category="Laptop", serial_number="SN-L009", status="Maintenance"),
        ]
        db.add_all(assets)
        db.commit()

        # 4. Create Assignments
        assignments = [
            models.AssetAssignment(asset_id=assets[0].id, employee_id=employees[0].id, assigned_by_id=1, assignment_date=date.today(), status="Active"),
            models.AssetAssignment(asset_id=assets[2].id, employee_id=employees[1].id, assigned_by_id=1, assignment_date=date.today(), status="Active"),
        ]
        db.add_all(assignments)
        db.commit()

        print("✅ Database successfully seeded with dummy data!")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
