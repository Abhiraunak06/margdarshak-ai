import json
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import func
from ..db.schema import (
    Examination, College, Branch, Cutoff, CollegePlacement, DataQualityReport
)

# Standard expected categories in Indian national counselling
STANDARD_CATEGORIES = ["OPEN", "OBC-NCL", "EWS", "SC", "ST"]

# Standard benchmark engineering branches that should be audited
BENCHMARK_BRANCHES = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering"
]

class QualityAuditor:
    @staticmethod
    def audit_exam(db_session, exam_code: str, year: int = 2024) -> Dict[str, Any]:
        exam = db_session.query(Examination).filter_by(code=exam_code).first()
        if not exam:
            return {"error": f"Exam {exam_code} not found."}

        # Query all cutoffs for this exam & year
        cutoffs_q = db_session.query(Cutoff).filter(Cutoff.exam_id == exam.id, Cutoff.year == year)
        total_cutoffs = cutoffs_q.count()

        # Unique colleges with cutoffs
        college_ids = [r[0] for r in cutoffs_q.with_entities(Cutoff.college_id).distinct().all()]
        total_colleges = len(college_ids)

        # Unique branches with cutoffs
        branch_ids = [r[0] for r in cutoffs_q.with_entities(Cutoff.branch_id).distinct().all()]
        total_branches = len(branch_ids)

        # Categories present
        categories_found = sorted([r[0] for r in cutoffs_q.with_entities(Cutoff.category).distinct().all()])
        quotas_found = sorted([r[0] for r in cutoffs_q.with_entities(Cutoff.quota).distinct().all()])
        rounds_found = sorted([r[0] for r in cutoffs_q.with_entities(Cutoff.round).distinct().all()])

        # Missing categories check
        missing_categories = [c for c in STANDARD_CATEGORIES if c not in categories_found]

        # Missing benchmark branches check
        branches_found_names = [
            b.canonical_name for b in db_session.query(Branch).filter(Branch.id.in_(branch_ids)).all()
        ]
        missing_branches = [b for b in BENCHMARK_BRANCHES if not any(b.lower() in found.lower() for found in branches_found_names)]

        # Duplicate check: tuples of (college_id, branch_id, round, quota, category, gender)
        dup_subq = (
            db_session.query(
                Cutoff.college_id, Cutoff.branch_id, Cutoff.round, Cutoff.quota, Cutoff.category, Cutoff.gender,
                func.count(Cutoff.id).label("count")
            )
            .filter(Cutoff.exam_id == exam.id, Cutoff.year == year)
            .group_by(Cutoff.college_id, Cutoff.branch_id, Cutoff.round, Cutoff.quota, Cutoff.category, Cutoff.gender)
            .having(func.count(Cutoff.id) > 1)
            .all()
        )
        duplicate_count = sum(r.count - 1 for r in dup_subq)

        # Invalid rank check (closing rank < opening rank or rank <= 0)
        invalid_ranks_count = cutoffs_q.filter((Cutoff.closing_rank < Cutoff.opening_rank) | (Cutoff.opening_rank <= 0)).count()

        # Check colleges missing official websites or placement info
        colleges_missing_website = db_session.query(College).filter(
            College.id.in_(college_ids),
            (College.official_website == None) | (College.official_website == "")
        ).count()

        colleges_with_placements = db_session.query(CollegePlacement.college_id).filter(
            CollegePlacement.college_id.in_(college_ids)
        ).distinct().count()
        colleges_missing_placements = total_colleges - colleges_with_placements

        # Calculate completeness score
        # Basis:
        # Category completeness: 30%
        # Core branch coverage: 30%
        # Round coverage: 20%
        # Data integrity (zero duplicates & valid ranks): 20%
        category_score = max(0, 30 * (len(STANDARD_CATEGORIES) - len(missing_categories)) / len(STANDARD_CATEGORIES))
        branch_score = max(0, 30 * (len(BENCHMARK_BRANCHES) - len(missing_branches)) / len(BENCHMARK_BRANCHES))
        round_score = min(20, (len(rounds_found) / 5.0) * 20.0) if rounds_found else 0
        integrity_penalty = (duplicate_count * 2) + (invalid_ranks_count * 5)
        integrity_score = max(0, 20 - integrity_penalty)

        completeness_score = round(min(100.0, category_score + branch_score + round_score + integrity_score), 1)

        # Save report
        report = DataQualityReport(
            exam_code=exam_code,
            year=year,
            total_colleges=total_colleges,
            total_branches=total_branches,
            total_cutoffs=total_cutoffs,
            categories_present=",".join(categories_found),
            quotas_present=",".join(quotas_found),
            rounds_present=",".join(map(str, rounds_found)),
            missing_categories=",".join(missing_categories) if missing_categories else None,
            missing_branches=",".join(missing_branches) if missing_branches else None,
            duplicate_records_count=duplicate_count,
            invalid_ranks_count=invalid_ranks_count,
            completeness_score=completeness_score,
            created_at=datetime.utcnow()
        )
        db_session.add(report)
        db_session.commit()

        return {
            "exam_code": exam_code,
            "exam_name": exam.name,
            "year": year,
            "total_cutoffs": total_cutoffs,
            "total_colleges": total_colleges,
            "total_branches": total_branches,
            "categories_present": categories_found,
            "quotas_present": quotas_found,
            "rounds_present": rounds_found,
            "missing_categories": missing_categories,
            "missing_branches": missing_branches,
            "duplicate_records_count": duplicate_count,
            "invalid_ranks_count": invalid_ranks_count,
            "colleges_missing_website": colleges_missing_website,
            "colleges_missing_placements": colleges_missing_placements,
            "completeness_score": completeness_score,
            "status": "Healthy" if completeness_score >= 85 else "Action Required"
        }
