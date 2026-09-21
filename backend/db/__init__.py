from .database import engine, SessionLocal, Base, get_db
from .schema import (
    Examination, ExamYear, College, CollegeAlias, Branch, BranchAlias,
    Cutoff, CollegePlacement, DataSource, DataSyncLog, DataQualityReport, CareerPath,
    MedicalCollege, MedicalCourse, NeetCutoff, MedicalPlacement,
    UniversityCollege, UniversityCourse, UniversityCutoff, GovernmentExam
)

def init_db():
    Base.metadata.create_all(bind=engine)
