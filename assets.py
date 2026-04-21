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
    assets = db.query(models.Asset).offset(skip).limit(limit).all()
    return assets

@router.post("/", response_model=schemas.AssetResponse, status_code=201, dependencies=[Depends(RequirePrivilege('manage:assets'))])
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.put("/{id}", response_model=schemas.AssetResponse, dependencies=[Depends(RequirePrivilege('manage:assets'))])
def update_asset(id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
        
    db.commit()
    db.refresh(db_asset)
    return db_asset
