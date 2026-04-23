"""
Dashboard Router (Stability Upgrade)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard & Audit Logs"]
)

@router.get("/stats/", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    try:
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
    except Exception:
        return {"total_assets": 0, "assigned_assets": 0, "available_assets": 0, "maintenance_assets": 0}

@router.get("/recent-assignments/")
def get_recent_assignments(db: Session = Depends(get_db)):
    """
    Fetch the 5 most recent asset assignments with enhanced error safety.
    """
    try:
        results = (
            db.query(models.AssetAssignment)
            .order_by(models.AssetAssignment.id.desc())
            .limit(5)
            .all()
        )
        
        formatted_data = []
        for item in results:
            # Handle potential nulls or string dates gracefully
            date_str = "N/A"
            if item.assigned_date:
                if isinstance(item.assigned_date, str):
                    date_str = item.assigned_date[:10] # Just get YYYY-MM-DD
                else:
                    date_str = item.assigned_date.strftime("%Y-%m-%d")

            formatted_data.append({
                "id": item.id,
                "asset_id": item.asset.asset_id if item.asset else "N/A",
                "asset_name": item.asset.name if item.asset else "Unknown Asset",
                "employee_name": f"{item.employee.first_name} {item.employee.last_name}" if item.employee else "N/A",
                "status": item.status or "Active",
                "date": date_str
            })
            
        return formatted_data
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return []

@router.get("/audit-logs/", response_model=List[schemas.AuditLogResponse])
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    return logs
