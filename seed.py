"""
Database Seeding Script (Enterprise Edition)
Populates the system with professional dummy data for a realistic dashboard.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine, Base
import models
from datetime import date, datetime

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # 1. ROLES
        admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
        if not admin_role:
            admin_role = models.Role(name="Admin", permissions=["*"])
            db.add(admin_role)
        
        emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
        if not emp_role:
            emp_role = models.Role(name="Employee", permissions=["view:own_assets"])
            db.add(emp_role)
        db.commit()

        # 2. EMPLOYEES (Professional List)
        employees_data = [
            ("Karthik", "V", "karthikgveresh@gmail.com", "Admin", "Management"),
            ("Alice", "Webb", "alice@optiasset.com", "Employee", "Engineering"),
            ("Bob", "Martin", "bob@optiasset.com", "Employee", "Design"),
            ("Charlie", "Day", "charlie@optiasset.com", "Employee", "Operations"),
            ("Jane", "Smith", "jane@optiasset.com", "Employee", "HR"),
            ("David", "Miller", "david@optiasset.com", "Employee", "Marketing"),
            ("Eva", "Green", "eva@optiasset.com", "Employee", "Sales"),
            ("Frank", "Castle", "frank@optiasset.com", "Employee", "Security"),
            ("Grace", "Hopper", "grace@optiasset.com", "Employee", "Engineering"),
            ("Henry", "Ford", "henry@optiasset.com", "Employee", "Logistics"),
        ]

        for f_name, l_name, email, r_name, dept in employees_data:
            existing = db.query(models.Employee).filter(models.Employee.email == email).first()
            if not existing:
                role = admin_role if r_name == "Admin" else emp_role
                emp = models.Employee(
                    first_name=f_name,
                    last_name=l_name,
                    email=email,
                    password="password123",
                    employee_code=f"EMP-{f_name.upper()[:3]}-{email.split('@')[0][-2:]}",
                    department=dept,
                    role_id=role.id,
                    is_active=True
                )
                db.add(emp)
        db.commit()

        # 3. ASSETS (High-End Inventory)
        assets_data = [
            ("MAC-001", "MacBook Pro 16\" M3", "Laptop", "Assigned"),
            ("MAC-002", "MacBook Air 15\" M2", "Laptop", "Assigned"),
            ("MAC-003", "MacBook Pro 14\" M3", "Laptop", "Available"),
            ("MON-101", "Dell UltraSharp 32\" 4K", "Monitor", "Assigned"),
            ("MON-102", "Dell UltraSharp 27\" QHD", "Monitor", "Assigned"),
            ("MON-103", "LG DualUp Monitor", "Monitor", "Maintenance"),
            ("PHN-501", "iPhone 15 Pro Max", "Phone", "Assigned"),
            ("PHN-502", "iPhone 15 Pro", "Phone", "Available"),
            ("ACC-201", "Apple Magic Keyboard", "Accessory", "Assigned"),
            ("ACC-202", "MX Master 3S Mouse", "Accessory", "Assigned"),
            ("ACC-203", "Sony WH-1000XM5", "Accessory", "Assigned"),
            ("ACC-204", "Herman Miller Aeron", "Furniture", "Assigned"),
        ]

        for tag, name, cat, status in assets_data:
            existing = db.query(models.Asset).filter(models.Asset.asset_id == tag).first()
            if not existing:
                asset = models.Asset(
                    asset_id=tag,
                    name=name,
                    category=cat,
                    status=status,
                    purchase_date=date(2023, 1, 15)
                )
                db.add(asset)
        db.commit()

        # 4. ASSIGNMENTS (Linking them together)
        # Fetch some employees and assets to link
        alice = db.query(models.Employee).filter(models.Employee.email == "alice@optiasset.com").first()
        bob = db.query(models.Employee).filter(models.Employee.email == "bob@optiasset.com").first()
        charlie = db.query(models.Employee).filter(models.Employee.email == "charlie@optiasset.com").first()
        jane = db.query(models.Employee).filter(models.Employee.email == "jane@optiasset.com").first()

        m1 = db.query(models.Asset).filter(models.Asset.asset_id == "MAC-001").first()
        m2 = db.query(models.Asset).filter(models.Asset.asset_id == "MAC-002").first()
        d1 = db.query(models.Asset).filter(models.Asset.asset_id == "MON-101").first()
        d2 = db.query(models.Asset).filter(models.Asset.asset_id == "MON-102").first()
        k1 = db.query(models.Asset).filter(models.Asset.asset_id == "ACC-201").first()
        s1 = db.query(models.Asset).filter(models.Asset.asset_id == "ACC-203").first()

        assign_list = [
            (m1, alice), (d1, alice),
            (m2, bob), (d2, bob),
            (k1, charlie),
            (s1, jane)
        ]

        for asset, emp in assign_list:
            if asset and emp:
                existing_assign = db.query(models.AssetAssignment).filter(
                    models.AssetAssignment.asset_id == asset.id,
                    models.AssetAssignment.employee_id == emp.id
                ).first()
                if not existing_assign:
                    assignment = models.AssetAssignment(
                        asset_id=asset.id,
                        employee_id=emp.id,
                        status="Active",
                        assigned_date=datetime.now()
                    )
                    db.add(assignment)
        
        db.commit()
        print("SEEDING COMPLETE: Enterprise database initialized.")

    except Exception as e:
        print(f"SEED ERROR: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
