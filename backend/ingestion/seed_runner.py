import os
import json
import time
from ..db import init_db, SessionLocal
from ..db.schema import CareerPath, GovernmentExam
from .adapters.josaa_adapter import JoSAAAdapter
from .adapters.wbjee_adapter import WBJEEAdapter
from .adapters.comedk_adapter import COMEDKAdapter
from .adapters.vit_adapter import VITAdapter
from .adapters.bits_adapter import BITSAdapter
from .adapters.neet_adapter import NEETAdapter
from .adapters.clat_adapter import CLATAdapter
from .adapters.cuet_adapter import CUETAdapter
from .government_exams_data import GOVERNMENT_EXAMS_DATA
from .quality_auditor import QualityAuditor
from .career_metadata import CAREER_PATHS

def run_seed():
    print("==================================================")
    print("  CareerPath AI - Master Multi-Stream Data Pipeline  ")
    print("==================================================")
    init_db()
    db = SessionLocal()

    try:
        # Step 1: Seed / Update Career Paths across all 4 streams
        print("\n[Step 1/10] Seeding Multi-Stream Career Guidance Tracks (PCM, PCB, Commerce, Arts)...")
        for cp in CAREER_PATHS:
            existing = db.query(CareerPath).filter_by(slug=cp["slug"]).first()
            if not existing:
                path_obj = CareerPath(
                    title=cp["title"],
                    slug=cp["slug"],
                    stream=cp.get("stream", "PCM"),
                    domain=cp["domain"],
                    description=cp["description"],
                    required_skills=cp["required_skills"],
                    recommended_degrees=cp["recommended_degrees"],
                    relevant_branches=cp["relevant_branches"],
                    entrance_exams=cp["entrance_exams"],
                    roadmap_steps=json.dumps(cp["roadmap_steps"]),
                    average_starting_salary_lpa=cp["average_starting_salary_lpa"],
                    growth_outlook=cp["growth_outlook"]
                )
                db.add(path_obj)
            else:
                existing.stream = cp.get("stream", "PCM")
                existing.title = cp["title"]
                existing.domain = cp["domain"]
                existing.description = cp["description"]
                existing.required_skills = cp["required_skills"]
                existing.recommended_degrees = cp["recommended_degrees"]
                existing.relevant_branches = cp["relevant_branches"]
                existing.entrance_exams = cp["entrance_exams"]
                existing.roadmap_steps = json.dumps(cp["roadmap_steps"])
                existing.average_starting_salary_lpa = cp["average_starting_salary_lpa"]
                existing.growth_outlook = cp["growth_outlook"]
        db.commit()
        print(f"  -> Seeded {len(CAREER_PATHS)} career guidance pathways.")

        # Step 2: Seed Government Examinations
        print("\n[Step 2/10] Seeding Government Career Directory...")
        for g in GOVERNMENT_EXAMS_DATA:
            existing_gov = db.query(GovernmentExam).filter_by(code=g["code"]).first()
            if not existing_gov:
                gov_obj = GovernmentExam(
                    title=g["title"],
                    code=g["code"],
                    conducting_body=g["conducting_body"],
                    sector=g["sector"],
                    eligibility_education=g["eligibility_education"],
                    min_age=g["min_age"],
                    max_age=g["max_age"],
                    selection_stages=g["selection_stages"],
                    syllabus_overview=g["syllabus_overview"],
                    career_roles=g["career_roles"],
                    salary_scale=g["salary_scale"],
                    official_website=g["official_website"],
                    application_window=g["application_window"],
                    preparation_roadmap=g["preparation_roadmap"]
                )
                db.add(gov_obj)
        db.commit()
        print(f"  -> Seeded {len(GOVERNMENT_EXAMS_DATA)} premier government examination tracks.")

        # Step 3: JoSAA Ingestion (JEE Main & JEE Advanced)
        print("\n[Step 3/10] Executing JoSAA Adapter (Official 2024 Rounds)...")
        josaa_adapter = JoSAAAdapter()
        josaa_res = josaa_adapter.sync(db, year=2024)
        print(f"  -> JoSAA Result: {josaa_res}")

        # Step 4: WBJEE Ingestion
        print("\n[Step 4/10] Executing WBJEE Adapter...")
        wbjee_adapter = WBJEEAdapter()
        wbjee_res = wbjee_adapter.sync(db, year=2024)
        print(f"  -> WBJEE Result: {wbjee_res}")

        # Step 5: COMEDK UGET Ingestion
        print("\n[Step 5/10] Executing COMEDK UGET Adapter...")
        comedk_adapter = COMEDKAdapter()
        comedk_res = comedk_adapter.sync(db, year=2024)
        print(f"  -> COMEDK Result: {comedk_res}")

        # Step 6: VITEEE Ingestion
        print("\n[Step 6/10] Executing VITEEE Adapter...")
        vit_adapter = VITAdapter()
        vit_res = vit_adapter.sync(db, year=2024)
        print(f"  -> VITEEE Result: {vit_res}")

        # Step 7: BITSAT Ingestion
        print("\n[Step 7/10] Executing BITSAT Score Adapter...")
        bits_adapter = BITSAdapter()
        bits_res = bits_adapter.sync(db, year=2024)
        print(f"  -> BITSAT Result: {bits_res}")

        # Step 8: NEET-UG Ingestion (PCB)
        print("\n[Step 8/10] Executing NEET-UG Medical Admission Adapter (MCC AIQ)...")
        neet_adapter = NEETAdapter()
        neet_res = neet_adapter.sync(db, year=2024)
        print(f"  -> NEET-UG Result: {neet_res}")

        # Step 9: CLAT Ingestion (Arts / Law)
        print("\n[Step 9/10] Executing CLAT Law Admission Adapter (Consortium of NLUs)...")
        clat_adapter = CLATAdapter()
        clat_res = clat_adapter.sync(db, year=2024)
        print(f"  -> CLAT Result: {clat_res}")

        # Step 10: CUET-UG & IPMAT Ingestion (Commerce & Arts)
        print("\n[Step 10/10] Executing CUET-UG & IPMAT Central University Adapter...")
        cuet_adapter = CUETAdapter()
        cuet_res = cuet_adapter.sync(db, year=2024)
        print(f"  -> CUET-UG / IPMAT Result: {cuet_res}")

        # Quality & Completeness Audit
        print("\n--- Executing Automated Multi-Stream Quality Audits ---")
        for code in ["JEE_MAIN", "JEE_ADV", "WBJEE", "COMEDK", "VITEEE", "BITSAT"]:
            report = QualityAuditor.audit_exam(db, code, year=2024)
            print(f"  [{code}] Colleges: {report.get('total_colleges')}, Cutoffs: {report.get('total_cutoffs')}, Completeness: {report.get('completeness_score')}%")

        print("\n==================================================")
        print("  Master Multi-Stream Pipeline Completed Successfully! ")
        print("==================================================")

    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
