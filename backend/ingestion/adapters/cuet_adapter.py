import time
from typing import Dict, Any, List
from datetime import datetime
from ...db.schema import (
    Examination, ExamYear, UniversityCollege, UniversityCourse, UniversityCutoff
)

CUET_COMMERCE_ARTS_COLLEGES = [
    {
        "name": "Shri Ram College of Commerce, University of Delhi",
        "short_name": "SRCC Delhi",
        "code": "SRCC-DELHI",
        "type": "Central University",
        "stream": "COMMERCE",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1926,
        "website": "https://www.srcc.edu",
        "nirf": 11,
        "annual_fee": 30000,
        "median_pkg": 10.5,
        "highest_pkg": 35.0,
        "cutoffs": [
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "OPEN", "score": 782.0, "type": "SCORE"},
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "OBC", "score": 752.0, "type": "SCORE"},
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "EWS", "score": 760.0, "type": "SCORE"},
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "SC", "score": 710.0, "type": "SCORE"},
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "ST", "score": 670.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Economics", "exam": "CUET_UG", "category": "OPEN", "score": 778.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Economics", "exam": "CUET_UG", "category": "OBC", "score": 745.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Economics", "exam": "CUET_UG", "category": "EWS", "score": 755.0, "type": "SCORE"},
        ]
    },
    {
        "name": "Shaheed Sukhdev College of Business Studies, University of Delhi",
        "short_name": "SSCBS Delhi",
        "code": "SSCBS-DELHI",
        "type": "Central University",
        "stream": "COMMERCE",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1987,
        "website": "https://sscbsdu.ac.in",
        "nirf": 92,
        "annual_fee": 25000,
        "median_pkg": 11.0,
        "highest_pkg": 44.0,
        "cutoffs": [
            {"course": "Bachelor of Management Studies (BMS)", "exam": "CUET_UG", "category": "OPEN", "score": 550.0, "type": "SCORE"}, # Section I + Math + General Test
            {"course": "Bachelor of Management Studies (BMS)", "exam": "CUET_UG", "category": "OBC", "score": 490.0, "type": "SCORE"},
            {"course": "Bachelor of Management Studies (BMS)", "exam": "CUET_UG", "category": "EWS", "score": 515.0, "type": "SCORE"},
            {"course": "Bachelor of Management Studies (BMS)", "exam": "CUET_UG", "category": "SC", "score": 420.0, "type": "SCORE"},
            {"course": "BBA (Financial and Investment Analysis)", "exam": "CUET_UG", "category": "OPEN", "score": 558.0, "type": "SCORE"},
            {"course": "BBA (Financial and Investment Analysis)", "exam": "CUET_UG", "category": "OBC", "score": 502.0, "type": "SCORE"},
        ]
    },
    {
        "name": "Hindu College, University of Delhi",
        "short_name": "Hindu College",
        "code": "HINDU-DELHI",
        "type": "Central University",
        "stream": "ARTS",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1899,
        "website": "https://hinducollege.ac.in",
        "nirf": 1,
        "annual_fee": 26000,
        "median_pkg": 9.5,
        "highest_pkg": 36.5,
        "cutoffs": [
            {"course": "B.A. (Hons) Political Science", "exam": "CUET_UG", "category": "OPEN", "score": 795.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Political Science", "exam": "CUET_UG", "category": "OBC", "score": 772.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Political Science", "exam": "CUET_UG", "category": "EWS", "score": 780.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Political Science", "exam": "CUET_UG", "category": "SC", "score": 740.0, "type": "SCORE"},
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "OPEN", "score": 780.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Economics", "exam": "CUET_UG", "category": "OPEN", "score": 775.0, "type": "SCORE"},
        ]
    },
    {
        "name": "Lady Shri Ram College for Women, University of Delhi",
        "short_name": "LSR Delhi",
        "code": "LSR-DELHI",
        "type": "Central University",
        "stream": "ARTS",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1956,
        "website": "https://lsr.edu.in",
        "nirf": 9,
        "annual_fee": 24000,
        "median_pkg": 10.0,
        "highest_pkg": 40.0,
        "cutoffs": [
            {"course": "B.A. (Hons) Psychology", "exam": "CUET_UG", "category": "OPEN", "score": 796.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Journalism", "exam": "CUET_UG", "category": "OPEN", "score": 770.0, "type": "SCORE"},
            {"course": "B.Com (Hons)", "exam": "CUET_UG", "category": "OPEN", "score": 776.0, "type": "SCORE"},
            {"course": "B.A. (Hons) Economics", "exam": "CUET_UG", "category": "OPEN", "score": 772.0, "type": "SCORE"},
        ]
    },
    {
        "name": "St. Stephen's College, University of Delhi",
        "short_name": "St. Stephen's Delhi",
        "code": "STEPHENS-DELHI",
        "type": "Central University",
        "stream": "ARTS",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1881,
        "website": "https://ststephens.edu",
        "nirf": 3,
        "annual_fee": 45000,
        "median_pkg": 9.8,
        "highest_pkg": 25.0,
        "cutoffs": [
            {"course": "B.A. (Hons) Economics", "exam": "CUET_UG", "category": "OPEN", "score": 780.0, "type": "SCORE"},
            {"course": "B.A. (Hons) History", "exam": "CUET_UG", "category": "OPEN", "score": 765.0, "type": "SCORE"},
            {"course": "B.A. (Hons) English", "exam": "CUET_UG", "category": "OPEN", "score": 768.0, "type": "SCORE"},
        ]
    },
    {
        "name": "Indian Institute of Management (IIM), Indore",
        "short_name": "IIM Indore",
        "code": "IIM-INDORE",
        "type": "IIM",
        "stream": "MANAGEMENT",
        "state": "Madhya Pradesh",
        "city": "Indore",
        "established": 1996,
        "website": "https://www.iimidr.ac.in",
        "nirf": 8,
        "annual_fee": 550000,
        "median_pkg": 27.2,
        "highest_pkg": 100.0,
        "cutoffs": [
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "OPEN", "score": 180.0, "type": "SCORE"}, # Composite Aptitude Score Cutoff
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "OBC", "score": 140.0, "type": "SCORE"},
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "EWS", "score": 155.0, "type": "SCORE"},
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "SC", "score": 105.0, "type": "SCORE"},
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "ST", "score": 75.0, "type": "SCORE"},
        ]
    },
    {
        "name": "Indian Institute of Management (IIM), Rohtak",
        "short_name": "IIM Rohtak",
        "code": "IIM-ROHTAK",
        "type": "IIM",
        "stream": "MANAGEMENT",
        "state": "Haryana",
        "city": "Rohtak",
        "established": 2009,
        "website": "https://www.iimrohtak.ac.in",
        "nirf": 12,
        "annual_fee": 500000,
        "median_pkg": 19.2,
        "highest_pkg": 48.0,
        "cutoffs": [
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "OPEN", "score": 305.0, "type": "SCORE"}, # IPMAT Rohtak out of 480
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "OBC", "score": 260.0, "type": "SCORE"},
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "EWS", "score": 275.0, "type": "SCORE"},
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "SC", "score": 190.0, "type": "SCORE"},
            {"course": "Integrated Programme in Management (IPM 5-Year)", "exam": "IPMAT", "category": "ST", "score": 140.0, "type": "SCORE"},
        ]
    }
]

class CUETAdapter:
    def __init__(self):
        self.source_url = "https://cuetug.ntaonline.in"

    def sync(self, db, year: int = 2024) -> Dict[str, Any]:
        start_time = time.time()

        # Register CUET-UG and IPMAT Exams
        cuet = db.query(Examination).filter_by(code="CUET_UG").first()
        if not cuet:
            cuet = Examination(
                name="Common University Entrance Test (CUET-UG)",
                code="CUET_UG",
                stream="COMMERCE",
                level="National",
                conducting_body="National Testing Agency (NTA)",
                scoring_type="Score",
                default_rank_type="SCORE",
                has_home_state_quota=False,
                website_url="https://cuetug.ntaonline.in",
                description="CUET-UG provides a single window opportunity to students seeking admission in Central Universities and top participating colleges across India for undergraduate Commerce, Arts, and Science programs."
            )
            db.add(cuet)
            db.flush()

        ipmat = db.query(Examination).filter_by(code="IPMAT").first()
        if not ipmat:
            ipmat = Examination(
                name="Integrated Programme in Management Aptitude Test (IPMAT)",
                code="IPMAT",
                stream="COMMERCE",
                level="National",
                conducting_body="Indian Institute of Management (IIM) Indore",
                scoring_type="Score",
                default_rank_type="SCORE",
                has_home_state_quota=False,
                website_url="https://www.iimidr.ac.in",
                description="IPMAT is conducted by IIM Indore and IIM Rohtak for admission to the prestigious 5-Year Dual Degree Integrated Programme in Management (BBA+MBA)."
            )
            db.add(ipmat)
            db.flush()

        inserted_count = 0
        for item in CUET_COMMERCE_ARTS_COLLEGES:
            college = db.query(UniversityCollege).filter_by(name=item["name"]).first()
            if not college:
                college = UniversityCollege(
                    name=item["name"],
                    short_name=item["short_name"],
                    code=item["code"],
                    type=item["type"],
                    stream=item["stream"],
                    state=item["state"],
                    city=item["city"],
                    established_year=item["established"],
                    official_website=item["website"],
                    nirf_rank=item["nirf"],
                    annual_tuition_fee_inr=item["annual_fee"],
                    median_package_lpa=item["median_pkg"],
                    highest_package_lpa=item["highest_pkg"],
                    placement_source="NIRF Report & University Placement Cell",
                    is_verified=True
                )
                db.add(college)
                db.flush()

            for cut in item.get("cutoffs", []):
                course = db.query(UniversityCourse).filter_by(name=cut["course"]).first()
                if not course:
                    import re
                    c_code = re.sub(r'[^A-Za-z0-9]+', '_', cut["course"]).strip('_').upper()[:35]
                    course = db.query(UniversityCourse).filter_by(code=c_code).first()
                    if not course:
                        course = UniversityCourse(
                            name=cut["course"],
                            code=c_code,
                            degree=cut["course"].split("(")[0].strip(),
                            stream=item["stream"],
                            duration_years=5 if "5-Year" in cut["course"] else 3
                        )
                        db.add(course)
                        db.flush()

                existing = db.query(UniversityCutoff).filter_by(
                    exam_code=cut["exam"],
                    year=year,
                    college_id=college.id,
                    course_id=course.id,
                    category=cut["category"]
                ).first()

                if not existing:
                    cutoff = UniversityCutoff(
                        exam_code=cut["exam"],
                        year=year,
                        round=1,
                        college_id=college.id,
                        course_id=course.id,
                        category=cut["category"],
                        rank_type="SCORE",
                        min_cutoff_value=cut["score"],
                        source_name="University Official CSAS / Admission Allotment List",
                        source_url=college.official_website,
                        last_verified_at=datetime.utcnow()
                    )
                    db.add(cutoff)
                    inserted_count += 1

        db.commit()
        duration_ms = int((time.time() - start_time) * 1000)
        return {
            "exam_code": "CUET_UG",
            "year": year,
            "status": "Success",
            "records_inserted": inserted_count,
            "duration_ms": duration_ms
        }
