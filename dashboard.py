"""
Dashboard Router (Final Connectivity Fix)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard & Audit Logs"]
)

@router.get("/stats", response_model=schemas.DashboardStats)
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

@router.get("/recent-assignments")
def get_recent_assignments(db: Session = Depends(get_db)):
    try:
        results = (
            db.query(models.AssetAssignment)
            .order_by(models.AssetAssignment.id.desc())
            .limit(5)
            .all()
        )
        
        formatted_data = []
        for item in results:
            date_str = "N/A"
            if item.assigned_date:
                date_str = str(item.assigned_date)[:10]

            formatted_data.append({
                "id": item.id,
                "asset_id": item.asset.asset_id if item.asset else "N/A",
                "asset_name": item.asset.name if item.asset else "Unknown Asset",
                "employee_name": f"{item.employee.first_name} {item.employee.last_name}" if item.employee else "N/A",
                "status": item.status or "Active",
                "date": date_str
            })
            
        return formatted_data
    except Exception:
        return []

@router.get("/personal-assignments/{id}")
def get_employee_assignments(id: int, db: Session = Depends(get_db)):
    """
    Fetch assignments for a specific employee.
    """
    try:
        assignments = db.query(models.AssetAssignment).filter(
            models.AssetAssignment.employee_id == id
        ).all()
        
        return [{
            "id": a.id,
            "asset_name": a.asset.name if a.asset else "Unknown",
            "asset_id": a.asset.asset_id if a.asset else "N/A",
            "assigned_date": str(a.assigned_date)[:10] if a.assigned_date else "N/A",
            "status": a.status
        } for a in assignments]
    except Exception:
        return []
