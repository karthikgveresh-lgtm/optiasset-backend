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

@router.get("/", response_model=List[schemas.AssignmentResponse], dependencies=[Depends(RequirePrivilege('view:dashboard'))])
def get_assignments(db: Session = Depends(get_db)):
    return db.query(models.AssetAssignment).all()

@router.post("/", response_model=schemas.AssignmentResponse, status_code=201, dependencies=[Depends(RequirePrivilege('manage:assignments'))])
def assign_asset(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if not asset or asset.status != "Available":
        raise HTTPException(status_code=400, detail="Asset is not available for assignment")

    db_assignment = models.AssetAssignment(**assignment.model_dump())
    db.add(db_assignment)
    asset.status = "Assigned"
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
