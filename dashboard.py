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
    prefix="/api/dashboard",
    tags=["Dashboard & Audit Logs"]
)

@router.get("/stats/", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    View high-level asset statistics for the dashboard.
    """
    total = db.query(models.Asset).count()
    assigned = db.query(models.Asset).filter(models.Asset.status == "Assigned").count()
    available = db.query(models.Asset).filter(models.Asset.status == "Available").count()
    maintenance = db.query(models.Asset).filter(models.Asset.status == "Maintenance").count()
    other = total - assigned - available - maintenance
    
    return {
        "total_assets": total,
        "assigned_assets": assigned,
        "available_assets": available,
        "maintenance_assets": maintenance + other # Sync with frontend
    }

@router.get("/audit-logs/", response_model=List[schemas.AuditLogResponse])
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    """
    View recent system activity.
    """
    logs = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    return logs

# Move employee assignments to a cleaner path or keep here for simplicity
@router.get("/personal-assignments/{id}/", response_model=List[schemas.AssignmentResponse])
def get_employee_assignments(id: int, db: Session = Depends(get_db)):
    """
    View an employee's currently assigned assets (Personal Portal).
    """
    assignments = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.employee_id == id,
        models.AssetAssignment.status == "Active"
    ).all()
    return assignments
