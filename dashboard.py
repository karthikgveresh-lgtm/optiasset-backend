"""
Dashboard Router (Recent Assignments Edition)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard & Audit Logs"]
)

@router.get("/stats/", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(models.Asset).count()
    assigned = db.query(models.Asset).filter(models.Asset.status == "Assigned").count()
    available = db.query(models.Asset).filter(models.Asset.status == "Available").count()
    maintenance = db.query(models.Asset).filter(models.Asset.status == "Maintenance").count()
    
    return {
        "total_assets": total,
        "assigned_assets": assigned,
        "available_assets": available,
        "maintenance_assets": maintenance
    }

@router.get("/recent-assignments/")
def get_recent_assignments(db: Session = Depends(get_db)):
    """
    Fetch the 5 most recent asset assignments for the dashboard table.
    """
    results = (
        db.query(models.AssetAssignment)
        .order_by(models.AssetAssignment.id.desc())
        .limit(5)
        .all()
    )
    
    formatted_data = []
    for item in results:
        formatted_data.append({
            "id": item.id,
            "asset_id": item.asset.asset_id if item.asset else "N/A",
            "asset_name": item.asset.name if item.asset else "Unknown Asset",
            "employee_name": f"{item.employee.first_name} {item.employee.last_name}" if item.employee else "Unknown",
            "status": item.status,
            "date": item.assigned_date.strftime("%Y-%m-%d") if item.assigned_date else "N/A"
        })
        
    return formatted_data

@router.get("/audit-logs/", response_model=List[schemas.AuditLogResponse])
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    return logs

@router.get("/personal-assignments/{id}/")
def get_employee_assignments(id: int, db: Session = Depends(get_db)):
    assignments = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.employee_id == id,
        models.AssetAssignment.status == "Active"
    ).all()
    
    # Simple manual mapping to avoid schema conflicts in rapid dev
    return [{
        "id": a.id,
        "asset_name": a.asset.name,
        "asset_id": a.asset.asset_id,
        "assigned_date": a.assigned_date
    } for a in assignments]
