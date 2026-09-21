from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc
from ..db.database import get_db
from ..db.schema import (
    Examination, College, Branch, BranchAlias, Cutoff, CollegePlacement,
    AdmissionSystem, AdmissionSystemInstitute,
    MedicalCollege, MedicalCourse, NeetCutoff, MedicalPlacement,
    UniversityCollege, UniversityCourse, UniversityCutoff
)

router = APIRouter(prefix="/api/cutoffs", tags=["Predictor"])

@router.get("/search")
def search_cutoffs(
    exam_code: str = Query(..., description="e.g. JEE_MAIN, JEE_ADV, WBJEE, COMEDK, VITEEE"),
    counselling: Optional[str] = Query(None, description="e.g. JOSAA, CSAB, WBJEE_COUNSELLING, COMEDK_COUNSELLING, VITEEE_COUNSELLING"),
    search_id: Optional[str] = Query(None, description="Client search session/request identifier for stale-response protection"),
    year: int = Query(2024),
    rank: int = Query(..., description="Student rank (integer > 0)"),
    category: str = Query("OPEN", description="OPEN, OBC-NCL, EWS, SC, ST, etc."),
    quota: Optional[str] = Query("All", description="AI, HS, OS, All"),
    home_state: Optional[str] = Query(None, description="Student's home state e.g. Maharashtra, Tamil Nadu"),
    gender: Optional[str] = Query("Gender-Neutral", description="Gender-Neutral, Female-only"),
    round: Optional[str] = Query("Any", description="1, 2, 3, 4, 5, or Any"),
    mode: str = Query("A", description="A: All Branches, B: Specific Branch, C: Branch Comparison"),
    branch: Optional[str] = Query(None, description="Branch name or comma-separated branch list for Mode B/C"),
    strategy: Optional[str] = Query("all", description="all, all_eligible, range_match, conservative, ambitious"),
    college_type: Optional[str] = Query("All", description="IIT, NIT, IIIT, GFTI, State-Govt, All"),
    state: Optional[str] = Query(None, description="Filter colleges by location state"),
    sort_by: Optional[str] = Query("closing_rank_asc", description="closing_rank_asc, closing_rank_desc, orank_asc, median_package_desc, college_name_asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    if rank <= 0:
        raise HTTPException(status_code=400, detail="Rank must be a positive integer greater than 0.")

    exam = db.query(Examination).filter_by(code=exam_code).first()
    if not exam:
        raise HTTPException(status_code=404, detail=f"Examination '{exam_code}' not found.")

    # Resolve Admission / Counselling System (with cross-exam protection and fallback)
    adm_system = None
    if counselling:
        # Validate that the requested admission system belongs to this exam
        adm_system = db.query(AdmissionSystem).filter(
            AdmissionSystem.code == counselling,
            AdmissionSystem.exam_id == exam.id
        ).first()

    if not adm_system:
        # Default to canonical admission system for this exam
        if exam_code in ["JEE_MAIN", "JEE_ADV"]:
            adm_system = db.query(AdmissionSystem).filter(AdmissionSystem.code == "JOSAA", AdmissionSystem.exam_id == exam.id).first()
        elif exam_code == "WBJEE":
            adm_system = db.query(AdmissionSystem).filter(AdmissionSystem.code == "WBJEE_COUNSELLING", AdmissionSystem.exam_id == exam.id).first()
        elif exam_code == "COMEDK":
            adm_system = db.query(AdmissionSystem).filter(AdmissionSystem.code == "COMEDK_COUNSELLING", AdmissionSystem.exam_id == exam.id).first()
        elif exam_code == "VITEEE":
            adm_system = db.query(AdmissionSystem).filter(AdmissionSystem.code == "VITEEE_COUNSELLING", AdmissionSystem.exam_id == exam.id).first()
        
        if not adm_system:
            adm_system = db.query(AdmissionSystem).filter_by(exam_id=exam.id).first()

    if not adm_system:
        raise HTTPException(status_code=404, detail=f"No active admission system found for examination '{exam_code}'.")

    # Strict relational query requiring verified institute participation:
    # Cutoff -> AdmissionSystem -> AdmissionSystemInstitute (CONFIRMED for this year) -> College -> Branch
    query = (
        db.query(Cutoff, College, Branch)
        .join(AdmissionSystem, Cutoff.admission_system_id == AdmissionSystem.id)
        .join(
            AdmissionSystemInstitute,
            and_(
                AdmissionSystemInstitute.admission_system_id == AdmissionSystem.id,
                AdmissionSystemInstitute.college_id == Cutoff.college_id,
                AdmissionSystemInstitute.year == Cutoff.year,
                AdmissionSystemInstitute.participation_status == "CONFIRMED"
            )
        )
        .join(College, Cutoff.college_id == College.id)
        .join(Branch, Cutoff.branch_id == Branch.id)
        .filter(
            Cutoff.exam_id == exam.id,
            Cutoff.admission_system_id == adm_system.id,
            Cutoff.year == year
        )
    )

    # 1. Category Filter with Universal Normalization & Fallback
    available_categories = [
        c[0] for c in db.query(Cutoff.category)
        .filter(Cutoff.exam_id == exam.id, Cutoff.year == year)
        .distinct().all()
    ]
    
    cat_upper = category.strip().upper() if category else "OPEN"
    effective_category = None
    
    # Direct case-insensitive match
    for ac in available_categories:
        if ac.upper() == cat_upper:
            effective_category = ac
            break
            
    if not effective_category:
        general_synonyms = {"OPEN", "GENERAL", "GEN", "UR", "UNRESERVED", "GENERAL MERIT", "GM", "CATEGORY 1"}
        if cat_upper in general_synonyms:
            for pref in ["OPEN", "General", "General Merit", "Category 1"]:
                if pref in available_categories:
                    effective_category = pref
                    break
        elif "OBC" in cat_upper:
            for pref in ["OBC-NCL", "OBC-A", "OBC", "General"]:
                if pref in available_categories:
                    effective_category = pref
                    break
        elif "SC" in cat_upper and "SC" in available_categories:
            effective_category = "SC"
        elif "ST" in cat_upper and "ST" in available_categories:
            effective_category = "ST"
        elif "EWS" in cat_upper and "EWS" in available_categories:
            effective_category = "EWS"

    # Fallback to canonical open/general if still not resolved
    if not effective_category:
        for pref in ["OPEN", "General", "General Merit", "Category 1"]:
            if pref in available_categories:
                effective_category = pref
                break
        if not effective_category and available_categories:
            effective_category = available_categories[0]

    if effective_category:
        query = query.filter(Cutoff.category == effective_category)

    # 2. Gender Filter
    available_genders = [
        g[0] for g in db.query(Cutoff.gender)
        .filter(Cutoff.exam_id == exam.id, Cutoff.year == year)
        .distinct().all()
    ]
    if "Female-only" in available_genders:
        if gender == "Female-only":
            query = query.filter(Cutoff.gender.in_(["Gender-Neutral", "Female-only"]))
        elif gender == "Gender-Neutral":
            query = query.filter(Cutoff.gender == "Gender-Neutral")

    # 3. Round Filter with Graceful Cap
    if round and round != "Any":
        try:
            r_int = int(round)
            available_rounds = [
                r[0] for r in db.query(Cutoff.round)
                .filter(Cutoff.exam_id == exam.id, Cutoff.year == year)
                .distinct().all()
            ]
            if r_int in available_rounds:
                query = query.filter(Cutoff.round == r_int)
            # If requested round doesn't exist for this exam (e.g. Round 5 in WBJEE), do not artificially restrict round
        except ValueError:
            pass

    # 4. Quota & Home State Logic with Cross-Exam Normalization
    available_quotas = [
        q[0] for q in db.query(Cutoff.quota)
        .filter(Cutoff.exam_id == exam.id, Cutoff.year == year)
        .distinct().all()
    ]
    if quota and quota not in ["All", "Any"]:
        q_upper = quota.strip().upper()
        matched_quota = None
        for aq in available_quotas:
            if aq.upper() == q_upper:
                matched_quota = aq
                break
        if not matched_quota:
            if q_upper in ["AI", "ALL INDIA"]:
                if "AI" in available_quotas:
                    matched_quota = "AI"
                elif "All India" in available_quotas and not exam.has_home_state_quota:
                    matched_quota = "All India"
            elif q_upper in ["HS", "HOME STATE"]:
                if "HS" in available_quotas:
                    matched_quota = "HS"
                elif "Home State" in available_quotas:
                    matched_quota = "Home State"
        
        if matched_quota:
            query = query.filter(Cutoff.quota == matched_quota)
    elif home_state and exam.has_home_state_quota:
        hs_quota_name = "HS" if "HS" in available_quotas else ("Home State" if "Home State" in available_quotas else None)
        os_quota_name = "OS" if "OS" in available_quotas else None
        ai_quota_name = "AI" if "AI" in available_quotas else ("All India" if "All India" in available_quotas else None)
        
        conditions = []
        if ai_quota_name:
            conditions.append(Cutoff.quota == ai_quota_name)
        if hs_quota_name:
            conditions.append(and_(College.state == home_state, Cutoff.quota == hs_quota_name))
        if os_quota_name:
            conditions.append(and_(College.state != home_state, Cutoff.quota == os_quota_name))
        if conditions:
            query = query.filter(or_(*conditions))

    # 5. College Type Filter
    if college_type and college_type != "All":
        query = query.filter(College.type == college_type)

    # 6. College State Filter
    if state and state != "All":
        query = query.filter(College.state == state)

    # 7. Branch Modes (Mode A, Mode B, Mode C)
    if mode == "B" and branch:
        # Specific branch: match canonical name or code or alias
        b_clean = branch.strip()
        query = query.filter(
            or_(
                Branch.canonical_name.ilike(f"%{b_clean}%"),
                Branch.code == b_clean.upper()
            )
        )
    elif mode == "C" and branch:
        # Branch Comparison: multi-select comma separated
        branches_list = [b.strip() for b in branch.split(",") if b.strip()]
        if branches_list:
            conditions = []
            for b in branches_list:
                conditions.append(Branch.canonical_name.ilike(f"%{b}%"))
                conditions.append(Branch.code == b.upper())
            query = query.filter(or_(*conditions))

    # 8. Rank / Score Strategy Filtering
    is_score_based = (exam.scoring_type == "Score" or exam.code == "BITSAT")
    if is_score_based:
        # In score-based admission (e.g. BITSAT out of 390): closing_rank is the minimum required score
        # A candidate with score >= closing_rank is eligible
        if strategy in ["all_eligible", "eligible"]:
            query = query.filter(Cutoff.closing_rank <= rank)
        elif strategy == "range_match":
            query = query.filter(Cutoff.closing_rank <= rank)
        elif strategy in ["conservative", "safe"]:
            query = query.filter(Cutoff.closing_rank <= max(0, rank - 15))
        elif strategy in ["ambitious", "reach"]:
            query = query.filter(Cutoff.closing_rank > rank, Cutoff.closing_rank <= rank + 15)
        else:
            # Default 'all': eligible + reach within 15 marks
            query = query.filter(Cutoff.closing_rank <= rank + 15)
    else:
        # Conventional rank-based admission: lower numerical rank is better
        if strategy in ["all_eligible", "eligible"]:
            query = query.filter(Cutoff.closing_rank >= rank)
        elif strategy == "range_match":
            query = query.filter(
                Cutoff.opening_rank <= rank,
                Cutoff.closing_rank >= rank
            )
        elif strategy in ["conservative", "safe"]:
            query = query.filter(Cutoff.closing_rank >= int(rank * 1.15))
        elif strategy in ["ambitious", "reach"]:
            query = query.filter(
                Cutoff.closing_rank >= int(rank * 0.75),
                Cutoff.closing_rank < rank
            )
        else:
            # Default 'all': include all eligible programs plus reach programs up to 0.75 * rank
            query = query.filter(Cutoff.closing_rank >= int(rank * 0.75))

    total_count = query.count()
    from sqlalchemy import func
    total_colleges_count = query.with_entities(func.count(func.distinct(Cutoff.college_id))).scalar() or 0

    # 9. Sorting
    if is_score_based:
        if sort_by == "closing_rank_asc":
            query = query.order_by(desc(Cutoff.closing_rank)) # Highest cutoff score first
        elif sort_by == "closing_rank_desc":
            query = query.order_by(asc(Cutoff.closing_rank))
        elif sort_by == "college_name_asc":
            query = query.order_by(asc(College.name))
        else:
            query = query.order_by(desc(Cutoff.closing_rank))
    else:
        if sort_by == "closing_rank_asc":
            query = query.order_by(asc(Cutoff.closing_rank))
        elif sort_by == "closing_rank_desc":
            query = query.order_by(desc(Cutoff.closing_rank))
        elif sort_by == "orank_asc":
            query = query.order_by(asc(Cutoff.opening_rank))
        elif sort_by == "college_name_asc":
            query = query.order_by(asc(College.name))
        else:
            query = query.order_by(asc(Cutoff.closing_rank))

    # 10. Pagination
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    # Pre-fetch placements for returned colleges
    college_ids = list(set(col.id for _, col, _ in results))
    placements = db.query(CollegePlacement).filter(CollegePlacement.college_id.in_(college_ids)).all()
    placement_map = {p.college_id: p for p in placements}

    # Format Output Items
    items = []
    for cutoff, college, branch_obj in results:
        crank = cutoff.closing_rank
        orank = cutoff.opening_rank

        # Determine strategy label and badge
        if is_score_based:
            if rank >= crank:
                if rank >= crank + 15:
                    strategy_label = "High Merit / Safe"
                    strategy_badge = "safe"
                    strategy_desc = f"Your score ({rank}) comfortably clears the cutoff score ({crank})."
                else:
                    strategy_label = "Historical Cutoff Match"
                    strategy_badge = "match"
                    strategy_desc = f"Your score ({rank}) meets the historical cutoff score ({crank})."
            else:
                strategy_label = "Reach (Ambitious)"
                strategy_badge = "ambitious"
                strategy_desc = f"Your score ({rank}) is within reach of historical cutoff ({crank})."
        else:
            if crank >= rank:
                if orank and rank < orank:
                    strategy_label = "High Merit / Safe"
                    strategy_badge = "safe"
                    strategy_desc = "Your rank is higher than the historical opening rank."
                else:
                    strategy_label = "Historical Range Match"
                    strategy_badge = "match"
                    strategy_desc = "Your rank falls within the historical admission range."
            else:
                strategy_label = "Reach (Ambitious)"
                strategy_badge = "ambitious"
                strategy_desc = "Cutoff was slightly ahead of your rank in historical counselling."

        place_obj = placement_map.get(college.id)
        placement_data = None
        if place_obj:
            placement_data = {
                "median_package_lpa": place_obj.median_package_lpa,
                "average_package_lpa": place_obj.average_package_lpa,
                "highest_package_lpa": place_obj.highest_package_lpa,
                "placement_percentage": place_obj.placement_percentage,
                "students_graduated": place_obj.students_graduated,
                "students_placed": place_obj.students_placed,
                "is_branch_level": place_obj.is_branch_level,
                "label": "Branch-level placement statistics" if place_obj.is_branch_level else "College-level placement data (NIRF verified) — branch-wise data not published by institute",
                "source_name": place_obj.source_name,
                "source_url": place_obj.source_url
            }

        items.append({
            "cutoff_id": cutoff.id,
            "college": {
                "id": college.id,
                "name": college.name,
                "short_name": college.short_name or college.name,
                "code": college.code,
                "type": college.type,
                "state": college.state,
                "city": college.city,
                "established_year": college.established_year,
                "official_website": college.official_website,
                "nirf_rank": college.nirf_rank
            },
            "branch": {
                "id": branch_obj.id,
                "canonical_name": branch_obj.canonical_name,
                "code": branch_obj.code,
                "degree": branch_obj.degree,
                "duration_years": branch_obj.duration_years,
                "discipline": branch_obj.discipline
            },
            "cutoff": {
                "opening_rank": cutoff.opening_rank,
                "closing_rank": cutoff.closing_rank,
                "rank_type": cutoff.rank_type or "OVERALL_RANK",
                "counselling": adm_system.code,
                "counselling_name": adm_system.name,
                "quota": cutoff.quota,
                "category": cutoff.category,
                "seat_type": cutoff.seat_type,
                "gender": cutoff.gender,
                "round": cutoff.round,
                "year": cutoff.year,
                "source_name": cutoff.source_name,
                "source_url": cutoff.source_url,
                "published_date": cutoff.published_date,
                "last_verified_at": cutoff.last_verified_at.isoformat() if cutoff.last_verified_at else None
            },
            "placement": placement_data,
            "strategy": {
                "label": strategy_label,
                "badge": strategy_badge,
                "description": strategy_desc
            }
        })

    return {
        "search_id": search_id,
        "admission_system": {
            "id": adm_system.id,
            "code": adm_system.code,
            "name": adm_system.name,
            "conducting_body": adm_system.conducting_body,
            "website_url": adm_system.website_url
        },
        "search_parameters": {
            "exam_code": exam.code,
            "exam_name": exam.name,
            "counselling": adm_system.code,
            "counselling_name": adm_system.name,
            "year": year,
            "rank": rank,
            "category": category,
            "quota": quota,
            "home_state": home_state,
            "gender": gender,
            "round": round,
            "mode": mode,
            "strategy": strategy,
            "disclaimer": "Based on historical/published cutoff data — not a guarantee of admission."
        },
        "pagination": {
            "total_count": total_count,
            "total_colleges_count": total_colleges_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit if total_count > 0 else 1
        },
        "results": items
    }

@router.get("/neet")
def search_neet_cutoffs(
    rank: int = Query(..., description="NEET All India Rank (AIR, >0)"),
    year: int = Query(2024),
    category: str = Query("OPEN", description="OPEN, OBC, EWS, SC, ST"),
    quota: str = Query("All India", description="All India, State Quota"),
    course: str = Query("MBBS", description="MBBS, BDS, or All"),
    round: int = Query(1),
    state: Optional[str] = Query(None),
    strategy: Optional[str] = Query("all", description="all, all_eligible, range_match, conservative, ambitious"),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    if rank <= 0:
        raise HTTPException(status_code=400, detail="Rank must be a positive integer greater than 0.")

    query = (
        db.query(NeetCutoff, MedicalCollege, MedicalCourse)
        .join(MedicalCollege, NeetCutoff.college_id == MedicalCollege.id)
        .join(MedicalCourse, NeetCutoff.course_id == MedicalCourse.id)
        .filter(NeetCutoff.year == year)
    )

    # Category normalization
    cat_upper = category.strip().upper()
    if cat_upper in ["GENERAL", "GEN", "UR", "OPEN"]:
        query = query.filter(NeetCutoff.category == "OPEN")
    elif "OBC" in cat_upper:
        query = query.filter(NeetCutoff.category == "OBC")
    elif "EWS" in cat_upper:
        query = query.filter(NeetCutoff.category == "EWS")
    elif "SC" in cat_upper:
        query = query.filter(NeetCutoff.category == "SC")
    elif "ST" in cat_upper:
        query = query.filter(NeetCutoff.category == "ST")

    # Quota filter
    if quota and quota not in ["All", "Any"]:
        query = query.filter(NeetCutoff.quota.ilike(f"%{quota}%"))

    # Course filter
    if course and course not in ["All", "Any"]:
        query = query.filter(MedicalCourse.code == course.upper())

    # State filter
    if state and state != "All":
        query = query.filter(MedicalCollege.state == state)

    # Strategy filtering
    if strategy in ["all_eligible", "eligible"]:
        query = query.filter(NeetCutoff.closing_rank >= rank)
    elif strategy == "range_match":
        query = query.filter(NeetCutoff.opening_rank <= rank, NeetCutoff.closing_rank >= rank)
    elif strategy in ["conservative", "safe"]:
        query = query.filter(NeetCutoff.closing_rank >= int(rank * 1.15))
    elif strategy in ["ambitious", "reach"]:
        query = query.filter(NeetCutoff.closing_rank >= int(rank * 0.75), NeetCutoff.closing_rank < rank)
    else:
        query = query.filter(NeetCutoff.closing_rank >= int(rank * 0.75))

    total_count = query.count()
    from sqlalchemy import func
    total_colleges_count = query.with_entities(func.count(func.distinct(NeetCutoff.college_id))).scalar() or 0

    query = query.order_by(asc(NeetCutoff.closing_rank))
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    # Pre-fetch medical placements/stipends
    med_ids = list(set(col.id for _, col, _ in results))
    placements = db.query(MedicalPlacement).filter(MedicalPlacement.college_id.in_(med_ids)).all()
    place_map = {p.college_id: p for p in placements}

    items = []
    for cutoff, college, course_obj in results:
        crank = cutoff.closing_rank
        orank = cutoff.opening_rank

        if crank >= rank:
            if orank and rank < orank:
                strat_label = "High Merit / Safe"
                strat_badge = "safe"
                strat_desc = f"Your NEET rank ({rank:,}) is ahead of historical opening rank ({orank:,})."
            else:
                strat_label = "Historical Range Match"
                strat_badge = "match"
                strat_desc = f"Your NEET rank ({rank:,}) falls comfortably within historical range ({orank:,} - {crank:,})."
        else:
            strat_label = "Reach (Ambitious)"
            strat_badge = "ambitious"
            strat_desc = f"Cutoff was slightly ahead ({crank:,}) in historical counselling."

        p_info = place_map.get(college.id)
        placement_data = None
        if p_info:
            placement_data = {
                "monthly_internship_stipend_inr": p_info.monthly_internship_stipend_inr,
                "junior_resident_starting_salary_pm": p_info.junior_resident_starting_salary_pm,
                "compulsory_rural_service_years": p_info.compulsory_rural_service_years,
                "bond_penalty_amount_lakhs": p_info.bond_penalty_amount_lakhs,
                "source_name": p_info.source_name
            }

        items.append({
            "cutoff_id": cutoff.id,
            "college": {
                "id": college.id,
                "name": college.name,
                "short_name": college.short_name or college.name,
                "code": college.code,
                "type": college.type,
                "state": college.state,
                "city": college.city,
                "established_year": college.established_year,
                "official_website": college.official_website,
                "nirf_medical_rank": college.nirf_medical_rank,
                "annual_tuition_fee_inr": college.annual_tuition_fee_inr
            },
            "course": {
                "id": course_obj.id,
                "name": course_obj.name,
                "code": course_obj.code,
                "degree": course_obj.degree,
                "duration_years": course_obj.duration_years,
                "requires_neet": course_obj.requires_neet
            },
            "cutoff": {
                "opening_rank": cutoff.opening_rank,
                "closing_rank": cutoff.closing_rank,
                "neet_score_approx": cutoff.neet_score_approx,
                "rank_type": "ALL_INDIA_RANK",
                "counselling": "MCC",
                "counselling_name": "Medical Counselling Committee (MCC)",
                "quota": cutoff.quota,
                "category": cutoff.category,
                "round": cutoff.round,
                "year": cutoff.year,
                "source_name": cutoff.source_name,
                "source_url": cutoff.source_url,
                "last_verified_at": cutoff.last_verified_at.isoformat() if cutoff.last_verified_at else None
            },
            "placement": placement_data,
            "strategy": {
                "label": strat_label,
                "badge": strat_badge,
                "description": strat_desc
            }
        })

    return {
        "search_parameters": {
            "exam_code": "NEET_UG",
            "exam_name": "NEET (UG)",
            "counselling": "MCC",
            "year": year,
            "rank": rank,
            "category": category,
            "quota": quota,
            "course": course,
            "round": round,
            "strategy": strategy,
            "disclaimer": "Based on authentic MCC NEET-UG 2024 All India Quota seat allotment reports."
        },
        "pagination": {
            "total_count": total_count,
            "total_colleges_count": total_colleges_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit if total_count > 0 else 1
        },
        "results": items
    }

@router.get("/university")
def search_university_cutoffs(
    exam_code: str = Query("CUET_UG", description="CUET_UG, IPMAT, CLAT"),
    score: float = Query(..., description="Normalized score / Composite Score / Rank"),
    year: int = Query(2024),
    category: str = Query("OPEN", description="OPEN, OBC, EWS, SC, ST"),
    course: Optional[str] = Query(None),
    stream: Optional[str] = Query(None, description="COMMERCE, ARTS, LAW, MANAGEMENT"),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = (
        db.query(UniversityCutoff, UniversityCollege, UniversityCourse)
        .join(UniversityCollege, UniversityCutoff.college_id == UniversityCollege.id)
        .join(UniversityCourse, UniversityCutoff.course_id == UniversityCourse.id)
        .filter(UniversityCutoff.exam_code == exam_code, UniversityCutoff.year == year)
    )

    # Category filter
    cat_upper = category.strip().upper()
    if cat_upper in ["OPEN", "GENERAL", "GEN", "UR"]:
        query = query.filter(UniversityCutoff.category == "OPEN")
    elif "OBC" in cat_upper:
        query = query.filter(UniversityCutoff.category == "OBC")
    elif "EWS" in cat_upper:
        query = query.filter(UniversityCutoff.category == "EWS")
    elif "SC" in cat_upper:
        query = query.filter(UniversityCutoff.category == "SC")
    elif "ST" in cat_upper:
        query = query.filter(UniversityCutoff.category == "ST")

    if stream and stream != "All":
        query = query.filter(UniversityCollege.stream == stream.upper())

    if course and course not in ["All", "Any"]:
        query = query.filter(UniversityCourse.name.ilike(f"%{course}%"))

    # In CLAT, score represents Rank (lower is better)
    # In CUET / IPMAT, score represents test marks (higher is better)
    is_rank_based = (exam_code == "CLAT")

    if is_rank_based:
        query = query.filter(UniversityCutoff.max_cutoff_value >= score)
        query = query.order_by(asc(UniversityCutoff.max_cutoff_value))
    else:
        # Score based: student score should meet min_cutoff_value (or within 20 points for reach)
        query = query.filter(UniversityCutoff.min_cutoff_value <= (score + 25.0))
        query = query.order_by(desc(UniversityCutoff.min_cutoff_value))

    total_count = query.count()
    from sqlalchemy import func
    total_colleges_count = query.with_entities(func.count(func.distinct(UniversityCutoff.college_id))).scalar() or 0

    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    items = []
    for cutoff, college, course_obj in results:
        cutoff_val = cutoff.min_cutoff_value
        max_val = cutoff.max_cutoff_value

        if is_rank_based:
            if max_val and score <= max_val:
                strat_label = "Eligible / Historical Match"
                strat_badge = "safe"
                strat_desc = f"Your CLAT rank ({int(score):,}) falls within historical NLU cutoff ({int(max_val):,})."
            else:
                strat_label = "Reach / Close Range"
                strat_badge = "ambitious"
                strat_desc = f"Cutoff closed at rank {int(max_val):,}."
        else:
            if score >= cutoff_val:
                strat_label = "Eligible / Above Cutoff"
                strat_badge = "safe"
                strat_desc = f"Your score ({score}) meets the published cutoff ({cutoff_val})."
            else:
                strat_label = "Reach (Ambitious)"
                strat_badge = "ambitious"
                strat_desc = f"Cutoff was {cutoff_val} marks."

        items.append({
            "cutoff_id": cutoff.id,
            "college": {
                "id": college.id,
                "name": college.name,
                "short_name": college.short_name or college.name,
                "code": college.code,
                "type": college.type,
                "stream": college.stream,
                "state": college.state,
                "city": college.city,
                "established_year": college.established_year,
                "official_website": college.official_website,
                "nirf_rank": college.nirf_rank,
                "annual_tuition_fee_inr": college.annual_tuition_fee_inr,
                "median_package_lpa": college.median_package_lpa,
                "highest_package_lpa": college.highest_package_lpa,
                "placement_source": college.placement_source
            },
            "course": {
                "id": course_obj.id,
                "name": course_obj.name,
                "code": course_obj.code,
                "degree": course_obj.degree,
                "stream": course_obj.stream,
                "duration_years": course_obj.duration_years
            },
            "cutoff": {
                "cutoff_score": cutoff.min_cutoff_value,
                "opening_rank": int(cutoff.min_cutoff_value) if is_rank_based else None,
                "closing_rank": int(cutoff.max_cutoff_value) if (is_rank_based and cutoff.max_cutoff_value) else None,
                "rank_type": cutoff.rank_type,
                "category": cutoff.category,
                "year": cutoff.year,
                "round": cutoff.round,
                "source_name": cutoff.source_name,
                "source_url": cutoff.source_url
            },
            "strategy": {
                "label": strat_label,
                "badge": strat_badge,
                "description": strat_desc
            }
        })

    return {
        "search_parameters": {
            "exam_code": exam_code,
            "score": score,
            "category": category,
            "stream": stream,
            "year": year
        },
        "pagination": {
            "total_count": total_count,
            "total_colleges_count": total_colleges_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit if total_count > 0 else 1
        },
        "results": items
    }
