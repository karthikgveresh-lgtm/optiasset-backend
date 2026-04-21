"""
Assets Router

This module contains the API endpoints for managing physical and digital assets.
It handles CRUD operations for the `assets` table.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db
from auth import RequirePrivilege

router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"]
)

@router.get("/", response_model=List[schemas.AssetResponse])
def get_all_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    View all assets in the system.
    
    - **skip**: The number of records to skip.
    - **limit**: The maximum number of records to return.
    - **Returns**: A list of asset records.
    """
    assets = db.query(models.Asset).offset(skip).limit(limit).all()
    return assets

@router.get("/{id}", response_model=schemas.AssetResponse)
def get_asset(id: int, db: Session = Depends(get_db)):
    """
    View a specific asset's details.
    
    - **id**: The internal database ID of the asset.
    - **Returns**: The asset record if found, else 404.
    """
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/", response_model=schemas.AssetResponse, status_code=201, dependencies=[Depends(RequirePrivilege('create:asset'))])
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    """
    Add a new asset to the system inventory.
    
    - **asset**: The details of the new asset.
    - **Returns**: The created asset record.
    """
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1,
        action="CREATE",
        target_table="assets",
        target_record_id=db_asset.id,
        details=f"Added new asset: {db_asset.name}"
    )
    db.add(log)
    db.commit()

    return db_asset

@router.put("/{id}", response_model=schemas.AssetResponse, dependencies=[Depends(RequirePrivilege('update:asset'))])
def update_asset(id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db)):
    """
    Update an existing asset's details.
    
    - **id**: The ID of the asset to update.
    - **asset_update**: Fields to update.
    - **Returns**: The updated asset record.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
        
    db.commit()
    db.refresh(db_asset)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1,
        action="UPDATE",
        target_table="assets",
        target_record_id=db_asset.id,
        details=f"Updated asset ID {id}"
    )
    db.add(log)
    db.commit()

    return db_asset

@router.patch("/{id}/status", response_model=schemas.AssetResponse, dependencies=[Depends(RequirePrivilege('update:asset_status'))])
def change_asset_status(id: int, status_update: schemas.AssetStatusUpdate, db: Session = Depends(get_db)):
    """
    Mark an asset as damaged, lost, or retired.
    
    - **id**: The ID of the asset.
    - **status_update**: The new status (e.g., 'Lost', 'In Maintenance').
    - **Returns**: The updated asset record.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_asset.status = status_update.status
    db.commit()
    db.refresh(db_asset)

    # Audit Log
    log = models.AuditLog(
        performed_by_id=1,
        action="STATUS_CHANGE",
        target_table="assets",
        target_record_id=db_asset.id,
        details=f"Changed asset ID {id} status to {status_update.status}"
    )
    db.add(log)
    db.commit()

    return db_asset
