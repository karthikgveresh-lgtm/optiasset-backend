"""
Employees Router

This module contains the API endpoints for managing employees.
It handles CRUD operations for the `employees` table.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db
from auth import RequirePrivilege

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)

@router.get("/", response_model=List[schemas.EmployeeResponse])
def get_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    View all employees.
    
    - **skip**: The number of records to skip (for pagination).
    - **limit**: The maximum number of records to return.
    - **Returns**: A list of employee records.
    """
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@router.get("/{id}", response_model=schemas.EmployeeResponse)
def get_employee(id: int, db: Session = Depends(get_db)):
    """
    View a specific employee's details by their ID.
    
    - **id**: The internal database ID of the employee.
    - **Returns**: The employee record if found, else raises 404.
    """
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=schemas.EmployeeResponse, status_code=201, dependencies=[Depends(RequirePrivilege('manage:users'))])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """
    Add a new employee to the system.
    
    Also logs this creation action in the `audit_logs` table.
    
    - **employee**: The details of the new employee.
    - **Returns**: The newly created employee record.
    """
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1, # Hardcoded for now, normally from auth context
        action="CREATE",
        target_table="employees",
        target_record_id=db_employee.id,
        details=f"Added new employee {db_employee.first_name} {db_employee.last_name}"
    )
    db.add(log)
    db.commit()

    return db_employee

@router.put("/{id}", response_model=schemas.EmployeeResponse, dependencies=[Depends(RequirePrivilege('manage:users'))])
def update_employee(id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing employee's details.
    
    - **id**: The ID of the employee to update.
    - **employee_update**: The fields to update (omitted fields remain unchanged).
    - **Returns**: The updated employee record.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
        
    db.commit()
    db.refresh(db_employee)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1,
        action="UPDATE",
        target_table="employees",
        target_record_id=db_employee.id,
        details=f"Updated employee ID {id}"
    )
    db.add(log)
    db.commit()

    return db_employee

@router.delete("/{id}", dependencies=[Depends(RequirePrivilege('delete:employee'))])
def deactivate_employee(id: int, db: Session = Depends(get_db)):
    """
    Deactivate an employee (Soft delete).
    
    Instead of removing the record, this endpoint sets `is_active = false`.
    
    - **id**: The ID of the employee to deactivate.
    - **Returns**: A success message.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee.is_active = False
    db.commit()

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1,
        action="DEACTIVATE",
        target_table="employees",
        target_record_id=id,
        details=f"Deactivated employee ID {id}"
    )
    db.add(log)
    db.commit()

    return {"message": "Employee deactivated successfully"}
