"""
Authentication and RBAC Module

Handles mock user authentication and Role-Based Access Control (RBAC).
"""

from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

import models
from database import get_db

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    Mock authentication dependency.
    Expects header like: `Authorization: Bearer <employee_id>`
    For example: `Authorization: Bearer 1`
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header. Use 'Bearer <employee_id>'")
    
    try:
        user_id = int(authorization.split(" ")[1])
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format. Expected integer employee ID.")

    user = db.query(models.Employee).filter(models.Employee.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

class RequirePrivilege:
    """
    Dependency class for Role-Based Access Control (RBAC).
    Usage: `Depends(RequirePrivilege('delete:asset'))`
    """
    def __init__(self, required_privilege: str):
        self.required_privilege = required_privilege

    def __call__(self, current_user: models.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
        if not current_user.role_id:
            raise HTTPException(status_code=403, detail="User has no assigned role")
            
        role = db.query(models.Role).filter(models.Role.id == current_user.role_id).first()
        if not role:
            raise HTTPException(status_code=403, detail="Role not found")
            
        if self.required_privilege not in role.permissions:
            raise HTTPException(
                status_code=403, 
                detail=f"Insufficient permissions. Requires '{self.required_privilege}'"
            )
            
        return current_user
