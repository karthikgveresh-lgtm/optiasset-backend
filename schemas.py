"""
Pydantic Schemas Module

This module defines Pydantic models (schemas) used for validating incoming API requests
and serializing outgoing API responses. They ensure data integrity and automatic documentation.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# --- Role Schemas ---
class RoleBase(BaseModel):
    name: str
    permissions: List[str]

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# --- Employee Schemas ---
class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    department: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class EmployeeSimple(BaseModel):
    first_name: str
    last_name: str
    class Config:
        from_attributes = True

# --- Asset Schemas ---
class AssetBase(BaseModel):
    asset_tag: str
    name: str
    category: str
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = None
    status: Optional[str] = "Available"
    notes: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    serial_number: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AssetStatusUpdate(BaseModel):
    status: str

class AssetResponse(AssetBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class AssetSimple(BaseModel):
    name: str
    asset_tag: str
    class Config:
        from_attributes = True

# --- Assignment Schemas ---
class AssignmentCreate(BaseModel):
    asset_id: int
    employee_id: int
    assigned_by_id: int
    assignment_date: date
    expected_return_date: Optional[date] = None
    assignment_notes: Optional[str] = None

class AssignmentReturn(BaseModel):
    return_notes: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: int
    asset_id: int
    employee_id: int
    assigned_by_id: int
    assignment_date: date
    expected_return_date: Optional[date] = None
    actual_return_date: Optional[date] = None
    assignment_notes: Optional[str] = None
    return_notes: Optional[str] = None
    status: str
    created_at: datetime
    
    # NESTED DATA for frontend display
    asset: Optional[AssetSimple] = None
    employee: Optional[EmployeeSimple] = None

    class Config:
        orm_mode = True
        from_attributes = True

# --- Audit Log Schemas ---
class AuditLogResponse(BaseModel):
    id: int
    performed_by_id: int
    action: str
    target_table: str
    target_record_id: int
    details: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class DashboardStats(BaseModel):
    total_assets: int
    assigned_assets: int
    available_assets: int
    maintenance_assets: int # Sync with frontend key
