"""
Assignments Router

This module contains the API endpoints for the Assignment & Returns workflow.
It handles assigning assets to employees and checking them back in.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

import models
import schemas
from database import get_db
from auth import RequirePrivilege

router = APIRouter(
    prefix="/api/assignments",
    tags=["Assignments & Workflow"]
)

@router.post("/", response_model=schemas.AssignmentResponse, status_code=201, dependencies=[Depends(RequirePrivilege('create:assignment'))])
def assign_asset(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    """
    Assign an available asset to an employee.
    
    This endpoint creates an assignment record and automatically updates 
    the asset's status to 'Assigned'.
    
    - **assignment**: The assignment details (who, what, when).
    - **Returns**: The created assignment record.
    """
    # Check if asset is available
    asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if not asset or asset.status != "Available":
        raise HTTPException(status_code=400, detail="Asset is not available for assignment")

    # Create assignment
    db_assignment = models.AssetAssignment(**assignment.model_dump())
    db.add(db_assignment)
    
    # Update asset status
    asset.status = "Assigned"
    
    db.commit()
    db.refresh(db_assignment)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=assignment.assigned_by_id,
        action="ASSIGN",
        target_table="asset_assignments",
        target_record_id=db_assignment.id,
        details=f"Assigned asset {asset.id} to employee {assignment.employee_id}"
    )
    db.add(log)
    db.commit()

    return db_assignment

@router.put("/{id}/return", response_model=schemas.AssignmentResponse, dependencies=[Depends(RequirePrivilege('update:assignment'))])
def return_asset(id: int, return_data: schemas.AssignmentReturn, db: Session = Depends(get_db)):
    """
    Return an assigned asset from an employee.
    
    This endpoint marks the assignment as 'Returned', sets the actual_return_date 
    to today, and updates the asset's status back to 'Available'.
    
    - **id**: The ID of the assignment record.
    - **return_data**: Optional notes regarding the condition upon return.
    - **Returns**: The updated assignment record.
    """
    assignment = db.query(models.AssetAssignment).filter(models.AssetAssignment.id == id).first()
    if not assignment or assignment.status == "Returned":
        raise HTTPException(status_code=400, detail="Invalid assignment or already returned")

    # Update assignment
    assignment.status = "Returned"
    assignment.actual_return_date = date.today()
    if return_data.return_notes:
        assignment.return_notes = return_data.return_notes

    # Update asset status
    asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if asset:
        asset.status = "Available"

    db.commit()
    db.refresh(assignment)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1, # Hardcoded
        action="RETURN",
        target_table="asset_assignments",
        target_record_id=assignment.id,
        details=f"Returned asset {assignment.asset_id} from employee {assignment.employee_id}"
    )
    db.add(log)
    db.commit()

    return assignment
