from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from ..db.database import get_db
from ..db.schema import (
    College, Branch, Cutoff, CollegePlacement, Examination
)

router = APIRouter(tags=["Colleges & Branches"])

@router.get("/api/colleges")
def list_colleges(
    q: Optional[str] = Query(None, description="Search college name, short name or city"),
    type: Optional[str] = Query(None, description="IIT, NIT, IIIT, GFTI, State-Govt"),
    state: Optional[str] = Query(None, description="Filter by Indian State"),
    has_placement: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query("nirf_asc", description="nirf_asc, name_asc, placement_desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(College)

    if q:
        query = query.filter(
            (College.name.ilike(f"%{q}%")) |
            (College.short_name.ilike(f"%{q}%")) |
            (College.city.ilike(f"%{q}%"))
        )

    if type and type != "All":
        query = query.filter(College.type == type)

    if state and state != "All":
        query = query.filter(College.state == state)

    if sort_by == "nirf_asc":
        # Nulls last
        query = query.order_by(College.nirf_rank.asc().nullslast())
    elif sort_by == "name_asc":
        query = query.order_by(College.name.asc())

    total = query.count()
    offset = (page - 1) * limit
    colleges = query.offset(offset).limit(limit).all()

    # Pre-fetch placements
    col_ids = [c.id for c in colleges]
    placements = {p.college_id: p for p in db.query(CollegePlacement).filter(CollegePlacement.college_id.in_(col_ids)).all()}

    results = []
    for c in colleges:
        p = placements.get(c.id)
        results.append({
            "id": c.id,
            "name": c.name,
            "short_name": c.short_name or c.name,
            "code": c.code,
            "type": c.type,
            "state": c.state,
            "city": c.city,
            "established_year": c.established_year,
            "official_website": c.official_website,
            "nirf_rank": c.nirf_rank,
            "is_verified": c.is_verified,
            "placement": {
                "median_package_lpa": p.median_package_lpa if p else None,
                "average_package_lpa": p.average_package_lpa if p else None,
                "highest_package_lpa": p.highest_package_lpa if p else None,
                "placement_percentage": p.placement_percentage if p else None,
                "source_name": p.source_name if p else None,
                "source_url": p.source_url if p else None,
                "is_branch_level": p.is_branch_level if p else False,
                "label": "College-level placement data (NIRF verified) — branch-wise data not published by institute" if (p and not p.is_branch_level) else None
            } if p else None
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1,
        "colleges": results
    }

@router.get("/api/colleges/{college_id}")
def get_college_details(college_id: int, db: Session = Depends(get_db)):
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")

    placements = db.query(CollegePlacement).filter(CollegePlacement.college_id == college.id).all()
    placement_info = None
    if placements:
        p = placements[0]
        placement_info = {
            "median_package_lpa": p.median_package_lpa,
            "average_package_lpa": p.average_package_lpa,
            "highest_package_lpa": p.highest_package_lpa,
            "placement_percentage": p.placement_percentage,
            "students_graduated": p.students_graduated,
            "students_placed": p.students_placed,
            "source_name": p.source_name,
            "source_url": p.source_url,
            "is_branch_level": p.is_branch_level,
            "label": "College-level placement data (NIRF verified) — branch-wise data not published by institute" if not p.is_branch_level else "Branch-wise official placement statistics"
        }

    # Available branches in this college
    branch_rows = (
        db.query(Branch)
        .join(Cutoff, Cutoff.branch_id == Branch.id)
        .filter(Cutoff.college_id == college.id)
        .distinct()
        .all()
    )

    branches_offered = [{
        "id": b.id,
        "canonical_name": b.canonical_name,
        "code": b.code,
        "degree": b.degree,
        "discipline": b.discipline
    } for b in branch_rows]

    # Sample latest cutoffs
    sample_cutoffs = (
        db.query(Cutoff, Branch)
        .join(Branch, Cutoff.branch_id == Branch.id)
        .filter(Cutoff.college_id == college.id, Cutoff.round == 5)
        .limit(20)
        .all()
    )

    cutoffs_list = [{
        "branch": b.canonical_name,
        "category": c.category,
        "quota": c.quota,
        "gender": c.gender,
        "round": c.round,
        "opening_rank": c.opening_rank,
        "closing_rank": c.closing_rank,
        "year": c.year
    } for c, b in sample_cutoffs]

    return {
        "id": college.id,
        "name": college.name,
        "short_name": college.short_name,
        "code": college.code,
        "type": college.type,
        "state": college.state,
        "city": college.city,
        "established_year": college.established_year,
        "official_website": college.official_website,
        "nirf_rank": college.nirf_rank,
        "placement": placement_info,
        "branches_count": len(branches_offered),
        "branches": branches_offered,
        "sample_cutoffs": cutoffs_list
    }

@router.get("/api/colleges/{college_id}/trends")
def get_cutoff_trends(
    college_id: int,
    branch_id: int,
    category: str = "OPEN",
    quota: str = "AI",
    gender: str = "Gender-Neutral",
    db: Session = Depends(get_db)
):
    """
    Returns historical cutoffs progression across rounds/years for visual graphs.
    """
    cutoffs = (
        db.query(Cutoff)
        .filter(
            Cutoff.college_id == college_id,
            Cutoff.branch_id == branch_id,
            Cutoff.category == category,
            Cutoff.gender == gender
        )
        .order_by(Cutoff.year.asc(), Cutoff.round.asc())
        .all()
    )

    trends = []
    for c in cutoffs:
        trends.append({
            "year": c.year,
            "round": f"Round {c.round}",
            "opening_rank": c.opening_rank,
            "closing_rank": c.closing_rank,
            "quota": c.quota,
            "category": c.category
        })

    return {
        "college_id": college_id,
        "branch_id": branch_id,
        "category": category,
        "quota": quota,
        "gender": gender,
        "trends": trends,
        "disclaimer": "Historical trends are for guidance only and do not guarantee future seat cutoffs."
    }

@router.get("/api/branches")
def list_branches(q: Optional[str] = None, discipline: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Branch)
    if q:
        query = query.filter(Branch.canonical_name.ilike(f"%{q}%") | Branch.code.ilike(f"%{q}%"))
    if discipline and discipline != "All":
        query = query.filter(Branch.discipline == discipline)

    branches = query.order_by(Branch.canonical_name.asc()).all()

    # Get distinct disciplines
    disciplines = [r[0] for r in db.query(Branch.discipline).distinct().order_by(Branch.discipline).all() if r[0]]

    return {
        "disciplines": disciplines,
        "total": len(branches),
        "branches": [{
            "id": b.id,
            "name": b.canonical_name,
            "code": b.code,
            "degree": b.degree,
            "duration_years": b.duration_years,
            "discipline": b.discipline
        } for b in branches]
    }

@router.get("/api/colleges/medical")
def list_medical_colleges(
    q: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    from ..db.schema import MedicalCollege, MedicalPlacement
    query = db.query(MedicalCollege)
    if q:
        query = query.filter(MedicalCollege.name.ilike(f"%{q}%") | MedicalCollege.city.ilike(f"%{q}%"))
    if state and state != "All":
        query = query.filter(MedicalCollege.state == state)
    if type and type != "All":
        query = query.filter(MedicalCollege.type == type)

    total = query.count()
    offset = (page - 1) * limit
    colleges = query.order_by(MedicalCollege.nirf_medical_rank.asc().nullslast(), MedicalCollege.name.asc()).offset(offset).limit(limit).all()

    # Placement / Stipend map
    c_ids = [c.id for c in colleges]
    placements = {p.college_id: p for p in db.query(MedicalPlacement).filter(MedicalPlacement.college_id.in_(c_ids)).all()}

    results = []
    for c in colleges:
        p = placements.get(c.id)
        results.append({
            "id": c.id,
            "name": c.name,
            "short_name": c.short_name or c.name,
            "code": c.code,
            "type": c.type,
            "state": c.state,
            "city": c.city,
            "established_year": c.established_year,
            "official_website": c.official_website,
            "nirf_medical_rank": c.nirf_medical_rank,
            "annual_tuition_fee_inr": c.annual_tuition_fee_inr,
            "stipend_pm": p.monthly_internship_stipend_inr if p else None,
            "jr_salary_pm": p.junior_resident_starting_salary_pm if p else None
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1,
        "colleges": results
    }

@router.get("/api/colleges/university")
def list_university_colleges(
    q: Optional[str] = Query(None),
    stream: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    from ..db.schema import UniversityCollege
    query = db.query(UniversityCollege)
    if q:
        query = query.filter(UniversityCollege.name.ilike(f"%{q}%") | UniversityCollege.city.ilike(f"%{q}%"))
    if stream and stream != "All":
        query = query.filter(UniversityCollege.stream == stream.upper())
    if state and state != "All":
        query = query.filter(UniversityCollege.state == state)

    total = query.count()
    offset = (page - 1) * limit
    colleges = query.order_by(UniversityCollege.nirf_rank.asc().nullslast(), UniversityCollege.name.asc()).offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1,
        "colleges": [{
            "id": c.id,
            "name": c.name,
            "short_name": c.short_name or c.name,
            "code": c.code,
            "type": c.type,
            "stream": c.stream,
            "state": c.state,
            "city": c.city,
            "established_year": c.established_year,
            "official_website": c.official_website,
            "nirf_rank": c.nirf_rank,
            "annual_tuition_fee_inr": c.annual_tuition_fee_inr,
            "median_package_lpa": c.median_package_lpa,
            "highest_package_lpa": c.highest_package_lpa
        } for c in colleges]
    }
