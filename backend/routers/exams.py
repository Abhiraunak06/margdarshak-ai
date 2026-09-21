from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db.database import get_db
from ..db.schema import (
    Examination, ExamYear, Cutoff, College,
    MedicalCollege, MedicalCourse, NeetCutoff,
    UniversityCollege, UniversityCourse, UniversityCutoff
)

router = APIRouter(prefix="/api/exams", tags=["Examinations"])

@router.get("")
def list_exams(stream: str = None, db: Session = Depends(get_db)):
    query = db.query(Examination).filter(Examination.is_active == True)
    if stream:
        st_upper = stream.upper()
        if st_upper in ["PCM", "ENGINEERING"]:
            query = query.filter(Examination.stream == "PCM")
        elif st_upper in ["PCB", "MEDICAL"]:
            query = query.filter(Examination.stream == "PCB")
        elif st_upper in ["COMMERCE", "FINANCE"]:
            query = query.filter(Examination.stream == "COMMERCE")
        elif st_upper in ["ARTS", "HUMANITIES"]:
            query = query.filter(Examination.stream == "ARTS")
        else:
            query = query.filter(Examination.stream == stream)
    exams = query.all()

    results = []
    for e in exams:
        years = [y.year for y in db.query(ExamYear).filter(ExamYear.exam_id == e.id, ExamYear.is_active == True).order_by(ExamYear.year.desc()).all()]
        if not years:
            years = [2024]

        # Calculate authentic cutoffs count across schema types
        if e.code == "NEET_UG":
            cutoff_count = db.query(NeetCutoff).count()
        elif e.code in ["CLAT", "CUET_UG", "IPMAT"]:
            cutoff_count = db.query(UniversityCutoff).filter(UniversityCutoff.exam_code == e.code).count()
        else:
            cutoff_count = db.query(Cutoff).filter(Cutoff.exam_id == e.id).count()

        results.append({
            "id": e.id,
            "name": e.name,
            "code": e.code,
            "stream": e.stream,
            "level": e.level,
            "conducting_body": e.conducting_body,
            "scoring_type": e.scoring_type,
            "default_rank_type": e.default_rank_type or "OVERALL_RANK",
            "has_home_state_quota": e.has_home_state_quota,
            "website_url": e.website_url,
            "description": e.description,
            "available_years": years,
            "total_cutoffs": cutoff_count
        })
    return results

@router.get("/{exam_code}/meta")
def get_exam_metadata(exam_code: str, year: int = 2024, db: Session = Depends(get_db)):
    exam = db.query(Examination).filter(Examination.code == exam_code).first()
    if not exam:
        raise HTTPException(status_code=404, detail=f"Examination '{exam_code}' not found")

    if exam.code == "NEET_UG":
        neet_q = db.query(NeetCutoff).filter(NeetCutoff.year == year)
        categories = [r[0] for r in neet_q.with_entities(NeetCutoff.category).distinct().order_by(NeetCutoff.category).all()]
        quotas = [r[0] for r in neet_q.with_entities(NeetCutoff.quota).distinct().order_by(NeetCutoff.quota).all()]
        rounds = [r[0] for r in neet_q.with_entities(NeetCutoff.round).distinct().order_by(NeetCutoff.round).all()]
        genders = ["Gender-Neutral"]
        states = [r[0] for r in db.query(MedicalCollege.state).distinct().order_by(MedicalCollege.state).all()]
        types = [r[0] for r in db.query(MedicalCollege.type).distinct().order_by(MedicalCollege.type).all()]
        courses = [r[0] for r in db.query(MedicalCourse.name).distinct().order_by(MedicalCourse.name).all()]
        guidance = "Enter your All India Rank (AIR) from your official NTA NEET Scorecard."

        from ..db.schema import AdmissionSystem
        adm_systems = db.query(AdmissionSystem).filter(AdmissionSystem.exam_id == exam.id).all()
        adm_list = [
            {"id": s.id, "code": s.code, "name": s.name, "conducting_body": s.conducting_body, "website_url": s.website_url, "description": s.description, "participating_institutes_count": db.query(MedicalCollege).count()}
            for s in adm_systems
        ]
        return {
            "exam_id": exam.id,
            "name": exam.name,
            "code": exam.code,
            "stream": exam.stream,
            "year": year,
            "default_rank_type": "OVERALL_RANK",
            "rank_guidance": guidance,
            "has_home_state_quota": exam.has_home_state_quota,
            "admission_systems": adm_list,
            "default_counselling": adm_list[0]["code"] if adm_list else "MCC_AIQ",
            "categories": categories or ["OPEN", "OBC", "EWS", "SC", "ST"],
            "quotas": quotas or ["All India", "State Quota"],
            "rounds": rounds or [1, 2, 3],
            "genders": genders,
            "states": states,
            "college_types": types,
            "courses": courses
        }

    elif exam.code in ["CLAT", "CUET_UG", "IPMAT"]:
        univ_q = db.query(UniversityCutoff).filter(UniversityCutoff.exam_code == exam.code, UniversityCutoff.year == year)
        categories = [r[0] for r in univ_q.with_entities(UniversityCutoff.category).distinct().order_by(UniversityCutoff.category).all()]
        quotas = ["All India"]
        rounds = [1]
        genders = ["Gender-Neutral"]
        college_ids = [r[0] for r in univ_q.with_entities(UniversityCutoff.college_id).distinct().all()]
        states = [r[0] for r in db.query(UniversityCollege.state).filter(UniversityCollege.id.in_(college_ids)).distinct().order_by(UniversityCollege.state).all()]
        types = [r[0] for r in db.query(UniversityCollege.type).filter(UniversityCollege.id.in_(college_ids)).distinct().order_by(UniversityCollege.type).all()]
        
        guidance = "Enter your score / percentile."
        if exam.code == "CLAT":
            guidance = "Enter your CLAT All India Rank (AIR)."
        elif exam.code == "CUET_UG":
            guidance = "Enter your normalized NTA CUET-UG score (e.g. 780 out of 800) or percentile."
        elif exam.code == "IPMAT":
            guidance = "Enter your IPMAT Composite Aptitude Score."

        return {
            "exam_id": exam.id,
            "name": exam.name,
            "code": exam.code,
            "stream": exam.stream,
            "year": year,
            "default_rank_type": exam.default_rank_type or "SCORE",
            "rank_guidance": guidance,
            "has_home_state_quota": exam.has_home_state_quota,
            "admission_systems": [{"id": 1, "code": exam.code, "name": f"{exam.name} Counselling", "conducting_body": exam.conducting_body, "website_url": exam.website_url, "description": exam.description, "participating_institutes_count": len(college_ids)}],
            "default_counselling": exam.code,
            "categories": categories or ["OPEN", "OBC", "EWS", "SC", "ST"],
            "quotas": quotas,
            "rounds": rounds,
            "genders": genders,
            "states": states,
            "college_types": types
        }

    # Conventional Engineering (JoSAA, WBJEE, COMEDK, VITEEE, BITSAT)
    cutoffs_q = db.query(Cutoff).filter(Cutoff.exam_id == exam.id, Cutoff.year == year)

    categories = [r[0] for r in cutoffs_q.with_entities(Cutoff.category).distinct().order_by(Cutoff.category).all()]
    quotas = [r[0] for r in cutoffs_q.with_entities(Cutoff.quota).distinct().order_by(Cutoff.quota).all()]
    rounds = [r[0] for r in cutoffs_q.with_entities(Cutoff.round).distinct().order_by(Cutoff.round).all()]
    genders = [r[0] for r in cutoffs_q.with_entities(Cutoff.gender).distinct().order_by(Cutoff.gender).all()]

    college_ids = [r[0] for r in cutoffs_q.with_entities(Cutoff.college_id).distinct().all()]
    states = [r[0] for r in db.query(College.state).filter(College.id.in_(college_ids), College.state != "India").distinct().order_by(College.state).all()]
    types = [r[0] for r in db.query(College.type).filter(College.id.in_(college_ids)).distinct().order_by(College.type).all()]

    guidance = "Enter your Overall Rank / Common Merit Rank (GMR)."
    if exam.code in ["JEE_MAIN", "JEE_ADV"]:
        guidance = "For OPEN category, enter your CRL (Common Rank List). For reserved categories (OBC-NCL, EWS, SC, ST, PwD), JoSAA cutoffs use Category Rank — enter your Category Rank as published on your official scorecard."
    elif exam.code == "COMEDK":
        guidance = "Enter your COMEDK General Merit (GM) Rank."
    elif exam.code == "WBJEE":
        guidance = "Enter your WBJEE General Merit Rank (GMR)."
    elif exam.code == "VITEEE":
        guidance = "Enter your VITEEE Equated Rank."
    elif exam.code == "BITSAT":
        guidance = "Enter your BITSAT Score (out of 390 marks)."

    from ..db.schema import AdmissionSystem, AdmissionSystemInstitute
    from sqlalchemy import or_, and_

    adm_systems = db.query(AdmissionSystem).filter(
        or_(
            AdmissionSystem.exam_id == exam.id,
            and_(exam.code == "JEE_ADV", AdmissionSystem.code == "JOSAA")
        ),
        AdmissionSystem.is_active == True
    ).all()

    admission_systems_list = [
        {
            "id": s.id,
            "code": s.code,
            "name": s.name,
            "conducting_body": s.conducting_body,
            "website_url": s.website_url,
            "description": s.description,
            "participating_institutes_count": db.query(AdmissionSystemInstitute).filter_by(admission_system_id=s.id, year=year).count()
        }
        for s in adm_systems
    ]

    return {
        "exam_id": exam.id,
        "name": exam.name,
        "code": exam.code,
        "stream": exam.stream,
        "year": year,
        "default_rank_type": exam.default_rank_type or "OVERALL_RANK",
        "rank_guidance": guidance,
        "has_home_state_quota": exam.has_home_state_quota,
        "admission_systems": admission_systems_list,
        "default_counselling": admission_systems_list[0]["code"] if admission_systems_list else None,
        "categories": categories,
        "quotas": quotas,
        "rounds": rounds,
        "genders": genders,
        "states": states,
        "college_types": types
    }
