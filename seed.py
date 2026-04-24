"""
Database Seeding Script (Fortune 500 Edition)
Generates 500 Employees and 1000 Assets for stress-testing and massive dashboards.
"""

import random
import time
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from datetime import date, datetime, timedelta

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        print("INITIALIZING MEGA-SEED...")
        
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

        # 2. GENERATE 500 EMPLOYEES
        first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
        depts = ["Engineering", "Product", "Sales", "HR", "Marketing", "Finance", "Legal", "Operations", "Design", "Customer Success"]

        print("Generating 500 Employees...")
        # Always keep you as Admin
        admin_user = db.query(models.Employee).filter(models.Employee.email == "karthikgveresh@gmail.com").first()
        if not admin_user:
            admin_user = models.Employee(
                first_name="Karthik", last_name="V", email="karthikgveresh@gmail.com",
                password="password123", employee_code="ADMIN-001", department="Executive",
                role_id=admin_role.id, is_active=True
            )
            db.add(admin_user)

        for i in range(500):
            f_name = random.choice(first_names)
            l_name = random.choice(last_names)
            email = f"{f_name.lower()}.{l_name.lower()}.{i}@optiasset.com"
            
            existing = db.query(models.Employee).filter(models.Employee.email == email).first()
            if not existing:
                emp = models.Employee(
                    first_name=f_name,
                    last_name=l_name,
                    email=email,
                    password="password123",
                    employee_code=f"EMP-{1000+i}",
                    department=random.choice(depts),
                    role_id=emp_role.id,
                    is_active=True
                )
                db.add(emp)
        db.commit()

        # 3. GENERATE 1000 ASSETS
        categories = ["Laptop", "Monitor", "Phone", "Accessory", "Furniture", "Server", "Tablet"]
        models_list = {
            "Laptop": ["MacBook Pro 16", "MacBook Air 15", "Dell XPS 15", "ThinkPad X1 Carbon", "HP EliteBook"],
            "Monitor": ["Dell 27 UltraSharp", "LG 34 UltraWide", "Samsung Odyssey G9", "ASUS ProArt"],
            "Phone": ["iPhone 15 Pro", "Samsung S24 Ultra", "Pixel 8 Pro", "iPhone 14"],
            "Accessory": ["Magic Mouse", "MX Master 3S", "Keychron K2", "Sony XM5 Headphones"],
            "Furniture": ["Herman Miller Aeron", "Steelcase Gesture", "Standing Desk Pro"],
            "Server": ["Dell PowerEdge R750", "HP ProLiant DL380", "AWS Outpost"],
            "Tablet": ["iPad Pro 12.9", "Galaxy Tab S9", "Surface Pro 9"]
        }
        statuses = ["Available", "Assigned", "Maintenance", "Retired"]

        print("Generating 1000 Assets...")
        for i in range(1000):
            cat = random.choice(categories)
            name = random.choice(models_list[cat])
            tag = f"{cat[:3].upper()}-{2000+i}"
            
            existing = db.query(models.Asset).filter(models.Asset.asset_id == tag).first()
            if not existing:
                asset = models.Asset(
                    asset_id=tag,
                    name=name,
                    category=cat,
                    status=random.choice(statuses),
                    purchase_date=date.today() - timedelta(days=random.randint(0, 730))
                )
                db.add(asset)
        db.commit()

        # 4. RANDOM ASSIGNMENTS (Let's assign ~400 assets)
        print("Creating ~400 Assignments...")
        all_emps = db.query(models.Employee).filter(models.Employee.email != "karthikgveresh@gmail.com").all()
        available_assets = db.query(models.Asset).filter(models.Asset.status == "Assigned").all()
        
        for i in range(min(len(all_emps), len(available_assets), 400)):
            asset = available_assets[i]
            emp = all_emps[i]
            
            existing_assign = db.query(models.AssetAssignment).filter(
                models.AssetAssignment.asset_id == asset.id
            ).first()
            
            if not existing_assign:
                assignment = models.AssetAssignment(
                    asset_id=asset.id,
                    employee_id=emp.id,
                    status="Active",
                    assigned_date=datetime.now() - timedelta(days=random.randint(0, 100))
                )
                db.add(assignment)
        
        db.commit()
        print("MEGA-SEED COMPLETE: 500 Users & 1000 Assets initialized.")

    except Exception as e:
        print(f"MEGA-SEED ERROR: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
