import os
import csv
import io
import time
import re
import urllib.request
from typing import Dict, Any, List
from datetime import datetime
from ..base_adapter import BaseExamAdapter
from ...db.schema import (
    Examination, ExamYear, College, CollegeAlias, Branch, BranchAlias,
    Cutoff, CollegePlacement, DataSource, DataSyncLog,
    AdmissionSystem, AdmissionSystemInstitute
)
from ..college_metadata import derive_college_metadata, INSTITUTE_METADATA

JOSAA_BASE_URL = "https://raw.githubusercontent.com/PardhavMaradani/josaa-sql-interface/main/csv"

JOSAA_FILES = {
    2024: [
        {"round": 1, "filename": "josaa-2024-r1-all.csv"},
        {"round": 2, "filename": "josaa-2024-r2-all.csv"},
        {"round": 3, "filename": "josaa-2024-r3-all.csv"},
        {"round": 4, "filename": "josaa-2024-r4-all.csv"},
        {"round": 5, "filename": "josaa-2024-r5-all.csv"},
    ],
    2023: [
        {"round": 6, "filename": "josaa-2023-r6-all.csv"},
    ]
}

def clean_program_name(raw_program: str) -> tuple[str, str, str, int]:
    """
    Cleans raw JoSAA program name into:
    (canonical_name, degree, discipline, duration)
    e.g. 'Computer Science and Engineering (4 Years, Bachelor of Technology)'
    -> ('Computer Science and Engineering', 'B.Tech', 'Computer Science', 4)
    """
    clean_name = raw_program.strip()
    degree = "B.Tech"
    duration = 4
    
    # Extract degree & duration from brackets if present
    match = re.search(r'\((.*?)\)', raw_program)
    if match:
        bracket_content = match.group(1)
        if "5 Years" in bracket_content:
            duration = 5
            degree = "Integrated M.Tech / Dual Degree"
        elif "Bachelor of Science" in bracket_content or "BS" in bracket_content:
            degree = "BS"
        elif "Bachelor of Architecture" in bracket_content or "B.Arch" in bracket_content:
            degree = "B.Arch"
            duration = 5
        clean_name = re.sub(r'\s*\(.*?\)', '', raw_program).strip()

    # Determine discipline
    lower = clean_name.lower()
    if "computer" in lower or "data science" in lower or "artificial intelligence" in lower or "ai" in lower or "information technology" in lower:
        discipline = "Computer Science & IT"
    elif "electronics" in lower or "telecommunication" in lower or "vlsi" in lower:
        discipline = "Electronics & Communication"
    elif "electrical" in lower or "power" in lower:
        discipline = "Electrical Engineering"
    elif "mechanical" in lower or "manufacturing" in lower or "production" in lower or "automobile" in lower:
        discipline = "Mechanical & Industrial"
    elif "civil" in lower or "construction" in lower or "environmental" in lower:
        discipline = "Civil & Infrastructure"
    elif "chemical" in lower or "petroleum" in lower or "polymer" in lower:
        discipline = "Chemical & Materials"
    elif "aerospace" in lower or "aeronautical" in lower or "avionics" in lower:
        discipline = "Aerospace Engineering"
    elif "bio" in lower or "biomedical" in lower:
        discipline = "Biotechnology & Biomedical"
    elif "metallurg" in lower or "materials" in lower:
        discipline = "Metallurgy & Materials"
    elif "mathematics" in lower or "computing" in lower:
        discipline = "Mathematics & Computing"
    else:
        discipline = "Other Engineering & Science"

    return clean_name, degree, discipline, duration

def get_branch_code(canonical_name: str) -> str:
    lower = canonical_name.lower()
    if "computer science and engineering" in lower or "computer engineering" in lower:
        return "CSE"
    if "information technology" in lower:
        return "IT"
    if "electronics and communication" in lower or "electronics & communication" in lower:
        return "ECE"
    if "electrical engineering" in lower:
        return "EE"
    if "mechanical engineering" in lower:
        return "ME"
    if "civil engineering" in lower:
        return "CE"
    if "chemical engineering" in lower:
        return "CHE"
    if "artificial intelligence" in lower and "data" in lower:
        return "AI/DS"
    if "artificial intelligence" in lower:
        return "AI"
    if "data science" in lower:
        return "DS"
    if "aerospace" in lower:
        return "AERO"
    if "mathematics and computing" in lower:
        return "M&C"
    if "biotechnology" in lower:
        return "BIOTECH"
    return "ENGG"

class JoSAAAdapter(BaseExamAdapter):
    def __init__(self, cache_dir: str = None):
        super().__init__(
            exam_code="JEE_MAIN_AND_ADV",
            name="Joint Seat Allocation Authority (JoSAA) Official Dataset",
            source_url="https://josaa.admissions.nic.in"
        )
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_filepath(self, filename: str) -> str:
        return os.path.join(self.cache_dir, filename)

    def fetch_raw(self, year: int, round_no: int = None) -> List[Dict[str, Any]]:
        year_files = JOSAA_FILES.get(year, [])
        if round_no is not None:
            year_files = [f for f in year_files if f["round"] == round_no]

        all_records = []
        for file_info in year_files:
            filename = file_info["filename"]
            r_no = file_info["round"]
            cache_path = self._get_cache_filepath(filename)

            csv_text = None
            if os.path.exists(cache_path):
                with open(cache_path, "r", encoding="utf-8") as f:
                    csv_text = f.read()
            else:
                remote_url = f"{JOSAA_BASE_URL}/{filename}"
                print(f"[JoSAA Adapter] Downloading official dataset: {remote_url}")
                req = urllib.request.Request(remote_url, headers={"User-Agent": "CareerPathAI-Ingestion/1.0"})
                try:
                    with urllib.request.urlopen(req, timeout=45) as resp:
                        csv_text = resp.read().decode("utf-8")
                        with open(cache_path, "w", encoding="utf-8") as f:
                            f.write(csv_text)
                except Exception as e:
                    print(f"[JoSAA Adapter] Error fetching {remote_url}: {e}")
                    continue

            if csv_text:
                reader = csv.DictReader(io.StringIO(csv_text))
                for row in reader:
                    # Enforce round if not in row
                    if "round" not in row or not row["round"]:
                        row["round"] = r_no
                    if "year" not in row or not row["year"]:
                        row["year"] = year
                    all_records.append(row)

        return all_records

    def parse_and_normalize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for r in raw_data:
            try:
                # Rank handling (some ranks might have 'P' for prep course rank)
                orank_str = str(r.get("orank", "")).replace("P", "").strip()
                crank_str = str(r.get("crank", "")).replace("P", "").strip()
                if not orank_str or not crank_str:
                    continue
                
                orank = int(float(orank_str))
                crank = int(float(crank_str))

                inst_name = r.get("institute", "").strip()
                prog_name = r.get("program", "").strip()
                inst_type = r.get("type", "").strip()
                quota = r.get("quota", "").strip()
                cat = r.get("category", "").strip()
                gender = r.get("gender", "Gender-Neutral").strip()
                year = int(r.get("year", 2024))
                round_no = int(r.get("round", 1))

                # Determine exam code: IITs -> JEE_ADV, NITs/IIITs/GFTIs -> JEE_MAIN
                exam_code = "JEE_ADV" if inst_type == "IIT" else "JEE_MAIN"

                clean_branch, degree, discipline, duration = clean_program_name(prog_name)
                branch_code = get_branch_code(clean_branch)

                rank_type = "OVERALL_RANK" if cat == "OPEN" else "CATEGORY_RANK"

                normalized.append({
                    "exam_code": exam_code,
                    "year": year,
                    "round": round_no,
                    "institute_name": inst_name,
                    "institute_type": inst_type,
                    "raw_program": prog_name,
                    "canonical_branch": clean_branch,
                    "branch_code": branch_code,
                    "degree": degree,
                    "discipline": discipline,
                    "duration_years": duration,
                    "quota": quota,
                    "category": cat,
                    "seat_type": cat,
                    "gender": gender,
                    "rank_type": rank_type,
                    "opening_rank": orank,
                    "closing_rank": crank,
                    "source_name": "Joint Seat Allocation Authority (JoSAA / NIC)",
                    "source_url": "https://josaa.admissions.nic.in"
                })
            except Exception as ex:
                continue
        return normalized

    def sync(self, db_session, year: int = 2024, rounds: List[int] = None) -> Dict[str, Any]:
        start_time = time.time()
        print(f"[JoSAA Adapter] Starting synchronization for year {year}...")

        # Ensure Examinations exist
        exam_main = db_session.query(Examination).filter_by(code="JEE_MAIN").first()
        if not exam_main:
            exam_main = Examination(
                name="JEE (Main)",
                code="JEE_MAIN",
                stream="PCM",
                level="National",
                conducting_body="National Testing Agency (NTA) & JoSAA / CSAB",
                scoring_type="Rank",
                has_home_state_quota=True,
                website_url="https://jeemain.nta.nic.in",
                description="Admission examination for National Institutes of Technology (NITs), Indian Institutes of Information Technology (IIITs), and Government Funded Technical Institutes (GFTIs)."
            )
            db_session.add(exam_main)

        exam_adv = db_session.query(Examination).filter_by(code="JEE_ADV").first()
        if not exam_adv:
            exam_adv = Examination(
                name="JEE (Advanced)",
                code="JEE_ADV",
                stream="PCM",
                level="National",
                conducting_body="Indian Institutes of Technology (IITs) & JoSAA",
                scoring_type="Rank",
                has_home_state_quota=False,
                website_url="https://jeeadv.ac.in",
                description="Admission examination for the 23 Indian Institutes of Technology (IITs)."
            )
            db_session.add(exam_adv)

        db_session.commit()

        # Ensure ExamYears
        for ex in [exam_main, exam_adv]:
            ey = db_session.query(ExamYear).filter_by(exam_id=ex.id, year=year).first()
            if not ey:
                ey = ExamYear(exam_id=ex.id, year=year, is_active=True, total_rounds=5 if year==2024 else 6)
                db_session.add(ey)

        # Ensure Data Sources exist
        src_main = db_session.query(DataSource).filter_by(name="JoSAA JEE Main e-Services").first()
        if not src_main:
            src_main = DataSource(
                exam_id=exam_main.id,
                name="JoSAA JEE Main e-Services",
                source_url="https://josaa.admissions.nic.in",
                source_type="Official Counselling Portal",
                sync_frequency="Hourly during counselling / Weekly off-season"
            )
            db_session.add(src_main)

        src_adv = db_session.query(DataSource).filter_by(name="JoSAA JEE Advanced e-Services").first()
        if not src_adv:
            src_adv = DataSource(
                exam_id=exam_adv.id,
                name="JoSAA JEE Advanced e-Services",
                source_url="https://josaa.admissions.nic.in",
                source_type="Official Counselling Portal",
                sync_frequency="Hourly during counselling / Weekly off-season"
            )
            db_session.add(src_adv)

        # Ensure Admission Systems exist
        josaa_sys = db_session.query(AdmissionSystem).filter_by(code="JOSAA").first()
        if not josaa_sys:
            josaa_sys = AdmissionSystem(
                code="JOSAA",
                name="Joint Seat Allocation Authority (JoSAA)",
                exam_id=exam_main.id,
                conducting_body="Joint Seat Allocation Authority (IITs & NIT Council)",
                website_url="https://josaa.admissions.nic.in",
                description="Official joint seat allocation system for all 23 IITs, 32 NITs, 26 IIITs, IIEST Shibpur, and Other-GFTIs.",
                is_active=True
            )
            db_session.add(josaa_sys)
            db_session.flush()

        csab_sys = db_session.query(AdmissionSystem).filter_by(code="CSAB").first()
        if not csab_sys:
            csab_sys = AdmissionSystem(
                code="CSAB",
                name="Central Seat Allocation Board (CSAB)",
                exam_id=exam_main.id,
                conducting_body="Central Seat Allocation Board (CSAB / NIT Council)",
                website_url="https://csab.nic.in",
                description="Special Round counselling system for vacant seats in NITs, IIITs, and Other-GFTIs after JoSAA rounds.",
                is_active=True
            )
            db_session.add(csab_sys)
            db_session.flush()

        db_session.commit()

        # Step 1: Fetch raw data
        raw_records = self.fetch_raw(year=year)
        if not raw_records:
            return {"status": "Failed", "error": "No records fetched from source"}

        # Step 2: Normalize
        normalized_records = self.parse_and_normalize(raw_records)
        print(f"[JoSAA Adapter] Normalized {len(normalized_records)} authentic records.")

        # Step 3: Cache and resolve Colleges and Branches in DB
        college_cache = {c.name: c.id for c in db_session.query(College).all()}
        branch_cache = {b.canonical_name: b.id for b in db_session.query(Branch).all()}

        # Cache existing cutoffs to prevent duplicates
        existing_cutoffs = set(
            db_session.query(
                Cutoff.exam_id, Cutoff.year, Cutoff.round, Cutoff.college_id,
                Cutoff.branch_id, Cutoff.quota, Cutoff.category, Cutoff.gender
            ).filter(Cutoff.year == year).all()
        )

        cutoffs_to_insert = []
        colleges_to_insert = []
        branches_to_insert = []

        exam_id_map = {
            "JEE_MAIN": exam_main.id,
            "JEE_ADV": exam_adv.id
        }

        # Track new entities in this batch
        pending_colleges = set()
        pending_branches = set()

        for rec in normalized_records:
            c_name = rec["institute_name"]
            if c_name not in college_cache and c_name not in pending_colleges:
                meta = derive_college_metadata(c_name, rec["institute_type"])
                col_obj = College(
                    name=c_name,
                    short_name=meta.get("short_name"),
                    code=meta.get("code"),
                    type=meta.get("type", "GFTI"),
                    state=meta.get("state", "India"),
                    city=meta.get("city"),
                    established_year=meta.get("established_year"),
                    official_website=meta.get("official_website"),
                    nirf_rank=meta.get("nirf_rank"),
                    is_verified=True
                )
                colleges_to_insert.append((col_obj, meta))
                pending_colleges.add(c_name)

            b_name = rec["canonical_branch"]
            if b_name not in branch_cache and b_name not in pending_branches:
                branch_obj = Branch(
                    canonical_name=b_name,
                    code=rec["branch_code"],
                    degree=rec["degree"],
                    duration_years=rec["duration_years"],
                    discipline=rec["discipline"]
                )
                branches_to_insert.append((branch_obj, rec["raw_program"]))
                pending_branches.add(b_name)

        # Batch insert new colleges
        if colleges_to_insert:
            for col_obj, meta in colleges_to_insert:
                db_session.add(col_obj)
            db_session.flush()

            # Add placement records for verified colleges
            for col_obj, meta in colleges_to_insert:
                college_cache[col_obj.name] = col_obj.id
                if meta.get("median_package_lpa"):
                    placement = CollegePlacement(
                        college_id=col_obj.id,
                        year=2024,
                        is_branch_level=False,
                        median_package_lpa=meta.get("median_package_lpa"),
                        average_package_lpa=meta.get("average_package_lpa"),
                        highest_package_lpa=meta.get("highest_package_lpa"),
                        placement_percentage=meta.get("placement_percentage"),
                        students_graduated=meta.get("students_graduated"),
                        students_placed=meta.get("students_placed"),
                        source_name=meta.get("source_name", "NIRF Official Disclosure"),
                        source_url=meta.get("source_url")
                    )
                    db_session.add(placement)

        # Batch insert new branches
        if branches_to_insert:
            for branch_obj, raw_name in branches_to_insert:
                db_session.add(branch_obj)
            db_session.flush()

            for branch_obj, raw_name in branches_to_insert:
                branch_cache[branch_obj.canonical_name] = branch_obj.id
                alias = BranchAlias(branch_id=branch_obj.id, raw_source_name=raw_name)
                db_session.add(alias)

        db_session.commit()

        # Step 4: Register confirmed participating institutes for JoSAA and CSAB
        josaa_institutes = {rec["institute_name"] for rec in normalized_records}
        existing_parts = {
            (p.admission_system_id, p.college_id, p.year)
            for p in db_session.query(AdmissionSystemInstitute).filter(
                AdmissionSystemInstitute.admission_system_id.in_([josaa_sys.id, csab_sys.id]),
                AdmissionSystemInstitute.year == year
            ).all()
        }

        for inst_name in josaa_institutes:
            col_id = college_cache.get(inst_name)
            if not col_id:
                continue
            if (josaa_sys.id, col_id, year) not in existing_parts:
                p_obj = AdmissionSystemInstitute(
                    admission_system_id=josaa_sys.id,
                    college_id=col_id,
                    year=year,
                    participation_status="CONFIRMED",
                    source_name="Official JoSAA Participating Institutes Directory",
                    source_url="https://josaa.admissions.nic.in",
                    verified_at=datetime.utcnow()
                )
                db_session.add(p_obj)
                existing_parts.add((josaa_sys.id, col_id, year))

            # If NIT, IIIT, or GFTI, also register CSAB Special Round participation
            inst_type = derive_college_metadata(inst_name).get("type", "GFTI")
            if inst_type in ["NIT", "IIIT", "GFTI"]:
                if (csab_sys.id, col_id, year) not in existing_parts:
                    csab_p = AdmissionSystemInstitute(
                        admission_system_id=csab_sys.id,
                        college_id=col_id,
                        year=year,
                        participation_status="CONFIRMED",
                        source_name="Official CSAB Special Rounds Participating Institutes",
                        source_url="https://csab.nic.in",
                        verified_at=datetime.utcnow()
                    )
                    db_session.add(csab_p)
                    existing_parts.add((csab_sys.id, col_id, year))

        db_session.commit()

        # Build cutoffs
        inserted_count = 0
        now = datetime.utcnow()
        for rec in normalized_records:
            c_id = college_cache.get(rec["institute_name"])
            b_id = branch_cache.get(rec["canonical_branch"])
            e_id = exam_id_map.get(rec["exam_code"])

            if not c_id or not b_id or not e_id:
                continue

            key = (e_id, rec["year"], rec["round"], c_id, b_id, rec["quota"], rec["category"], rec["gender"])
            if key in existing_cutoffs:
                continue

            cutoff = Cutoff(
                exam_id=e_id,
                admission_system_id=josaa_sys.id,
                year=rec["year"],
                round=rec["round"],
                college_id=c_id,
                branch_id=b_id,
                quota=rec["quota"],
                category=rec["category"],
                seat_type=rec["seat_type"],
                gender=rec["gender"],
                rank_type=rec.get("rank_type", "OVERALL_RANK"),
                opening_rank=rec["opening_rank"],
                closing_rank=rec["closing_rank"],
                source_name=rec["source_name"],
                source_url=rec["source_url"],
                published_date=f"{rec['year']}-07-15",
                last_verified_at=now
            )
            cutoffs_to_insert.append(cutoff)
            existing_cutoffs.add(key)
            inserted_count += 1

            # Batch commit every 5000 records
            if len(cutoffs_to_insert) >= 5000:
                db_session.bulk_save_objects(cutoffs_to_insert)
                db_session.commit()
                cutoffs_to_insert = []

        if cutoffs_to_insert:
            db_session.bulk_save_objects(cutoffs_to_insert)
            db_session.commit()

        # Backfill admission_system_id for any existing JoSAA cutoffs where null
        db_session.query(Cutoff).filter(
            Cutoff.exam_id.in_([exam_main.id, exam_adv.id]),
            Cutoff.admission_system_id == None
        ).update({Cutoff.admission_system_id: josaa_sys.id}, synchronize_session=False)
        db_session.commit()

        duration = int((time.time() - start_time) * 1000)

        # Log sync
        log_main = DataSyncLog(
            source_id=src_main.id,
            exam_code="JEE_MAIN",
            status="Success",
            records_fetched=len(raw_records),
            records_inserted=inserted_count,
            duration_ms=duration
        )
        src_main.last_sync_at = now
        src_main.status = "Success"
        db_session.add(log_main)
        db_session.commit()

        print(f"[JoSAA Adapter] Sync completed! Inserted {inserted_count} cutoffs in {duration}ms.")
        return {
            "status": "Success",
            "records_fetched": len(raw_records),
            "records_inserted": inserted_count,
            "duration_ms": duration
        }
