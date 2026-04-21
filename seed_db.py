from database import SessionLocal
import models

def seed():
    db = SessionLocal()
    
    # 1. Create Roles
    admin_role = models.Role(
        name="Admin", 
        permissions=["view:dashboard", "manage:assets", "manage:users", "manage:assignments"]
    )
    employee_role = models.Role(
        name="Employee", 
        permissions=["view:dashboard", "view:my_assets", "report:issue"]
    )
    
    db.add(admin_role)
    db.add(employee_role)
    db.commit()
    db.refresh(admin_role)
    db.refresh(employee_role)
    
    # 2. Create Users
    admin_user = models.Employee(
        employee_code="ADM001",
        first_name="Admin",
        last_name="User",
        email="admin@optiasset.com",
        department="IT",
        role_id=admin_role.id
    )
    
    standard_user = models.Employee(
        employee_code="EMP001",
        first_name="John",
        last_name="Doe",
        email="john@optiasset.com",
        department="Sales",
        role_id=employee_role.id
    )
    
    db.add(admin_user)
    db.add(standard_user)
    db.commit()
    
    print("Database seeded successfully!")
    print(f"Admin User ID: {admin_user.id}")
    print(f"Employee User ID: {standard_user.id}")
    db.close()

if __name__ == "__main__":
    seed()
