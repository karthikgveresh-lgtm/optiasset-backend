"""
Dashboard Router

This module contains the API endpoints for dashboard statistics and audit logs.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Dashboard & Audit Logs"]
)

@router.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    View high-level asset statistics for the dashboard.
    
    Calculates the total number of assets, how many are assigned, 
    how many are available, and how many are lost/in maintenance.
    
    - **Returns**: A summary statistics object.
    """
    total = db.query(models.Asset).count()
    assigned = db.query(models.Asset).filter(models.Asset.status == "Assigned").count()
    available = db.query(models.Asset).filter(models.Asset.status == "Available").count()
    other = total - assigned - available
    
    return {
        "total_assets": total,
        "assigned_assets": assigned,
        "available_assets": available,
        "lost_or_maintenance": other
    }

@router.get("/audit-logs", response_model=List[schemas.AuditLogResponse])
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    """
    View recent system activity.
    
    - **limit**: Maximum number of logs to retrieve (default 50).
    - **Returns**: A list of recent audit log records ordered by date descending.
    """
    logs = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    return logs

# --- Personal Portal Endpoint (Mixed domain, placed here for simplicity) ---

@router.get("/employees/{id}/assignments", response_model=List[schemas.AssignmentResponse])
def get_employee_assignments(id: int, db: Session = Depends(get_db)):
    """
    View an employee's currently assigned assets (Personal Portal).
    
    - **id**: The ID of the employee.
    - **Returns**: A list of active assignments for this employee.
    """
    assignments = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.employee_id == id,
        models.AssetAssignment.status == "Active"
    ).all()
    return assignments
