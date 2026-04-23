"""
Database Models Module
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    permissions = Column(JSON, nullable=False)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=True, default="password123") # Added password field
    phone_number = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    role = relationship("Role")

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    serial_number = Column(String(150), nullable=True)
    purchase_date = Column(Date, nullable=True)
    purchase_cost = Column(Float, nullable=True)
    status = Column(String(50), default="Available")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), index=True, nullable=False)
    assigned_by_id = Column(Integer, nullable=False)
    assignment_date = Column(Date, nullable=False)
    expected_return_date = Column(Date, nullable=True)
    actual_return_date = Column(Date, nullable=True)
    assignment_notes = Column(Text, nullable=True)
    return_notes = Column(Text, nullable=True)
    status = Column(String(50), default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    asset = relationship("Asset")
    employee = relationship("Employee")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    performed_by_id = Column(Integer, nullable=False)
    action = Column(String(255), nullable=False)
    target_table = Column(String(100), nullable=False)
    target_record_id = Column(Integer, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
