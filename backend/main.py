import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, SessionLocal
from .db.schema import Examination, Cutoff, College
from .routers import exams, predictor, colleges, careers, admin, chatbot

app = FastAPI(
    title="CareerPath AI - Indian College Predictor & Career Guidance API",
    description="Production-grade, data-driven college prediction and career guidance platform for Indian students based on authentic JoSAA, NIRF, and State counselling cutoff records.",
    version="1.0.0"
)

# Configure CORS for local development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(exams.router)
app.include_router(predictor.router)
app.include_router(colleges.router)
app.include_router(careers.router)
app.include_router(admin.router)
app.include_router(chatbot.router)

@app.on_event("startup")
def startup_event():
    init_db()
    db = SessionLocal()
    try:
        cutoff_count = db.query(Cutoff).count()
        college_count = db.query(College).count()
        print(f"[CareerPath AI Backend] Database initialized with {college_count} colleges and {cutoff_count:,} cutoff records.")
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    db = SessionLocal()
    try:
        cutoff_count = db.query(Cutoff).count()
        college_count = db.query(College).count()
        return {
            "status": "Healthy",
            "environment": "Production-Ready",
            "database": {
                "total_colleges": college_count,
                "total_cutoffs": cutoff_count,
                "data_integrity": "Authentic Official Records Only"
            }
        }
    finally:
        db.close()

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException

@app.get("/api")
def api_root():
    return {
        "message": "Welcome to CareerPath AI API - Indian College Prediction and Career Guidance Platform.",
        "docs_url": "/docs",
        "health_url": "/api/health",
        "download_url": "/api/download/project"
    }

@app.get("/api/download/project")
def download_project_zip():
    zip_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "careerpath-ai-platform.zip")
    if os.path.exists(zip_path):
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="careerpath-ai-platform.zip"
        )
    raise HTTPException(status_code=404, detail="Project zip archive not found.")

@app.get("/api/download/report")
def download_project_report_docx():
    doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Margdarshak_AI_Project_Report.docx")
    if os.path.exists(doc_path):
        return FileResponse(
            doc_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Margdarshak_AI_Project_Report.docx"
        )
    raise HTTPException(status_code=404, detail="Project report Word document not found.")

# Mount built production frontend on root so http://localhost:8000/ and http://127.0.0.1:8000/ serve the full React application
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

