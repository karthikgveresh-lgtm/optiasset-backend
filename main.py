"""
Main Application Module
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import employees, assets, assignments, dashboard
from seed import seed_data # Import our seed function

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AssetTracker Pro API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"status": "OptiAsset API is Online", "version": "1.0.0"}

# MAGIC SEED ENDPOINT
@app.get("/api/seed")
def trigger_seed():
    seed_data()
    return {"message": "Database seeded successfully with dummy data!"}
