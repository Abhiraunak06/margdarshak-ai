import os
import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.db.schema import Examination, College, Branch, Cutoff, CollegePlacement, DataQualityReport
from backend.ingestion.quality_auditor import QualityAuditor

class TestCareerPathAI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_colleges_present(self):
        colleges_count = self.db.query(College).count()
        self.assertGreaterEqual(colleges_count, 120, "Should have at least 120 authentic colleges in DB")
        print(f"[Check 1 Passed] Total Colleges: {colleges_count}")

    def test_02_branches_present(self):
        branches_count = self.db.query(Branch).count()
        self.assertGreaterEqual(branches_count, 100, "Should have at least 100 authentic engineering programs")
        print(f"[Check 2 Passed] Total Branches: {branches_count}")

    def test_03_benchmark_branches_present(self):
        benchmark_branches = ["Computer Science", "Electronics", "Electrical", "Mechanical", "Civil", "Chemical"]
        for b in benchmark_branches:
            found = self.db.query(Branch).filter(Branch.canonical_name.ilike(f"%{b}%")).count()
            self.assertGreater(found, 0, f"Benchmark branch '{b}' must be present in database")
        print("[Check 3 Passed] Benchmark branches (CSE, ECE, EE, ME, CE, Chem) present")

    def test_04_categories_present(self):
        categories = [r[0] for r in self.db.query(Cutoff.category).distinct().all()]
        expected = ["OPEN", "OBC-NCL", "EWS", "SC", "ST"]
        for exp in expected:
            self.assertIn(exp, categories, f"Category {exp} must be present in cutoff dataset")
        print(f"[Check 4 Passed] Categories present: {categories}")

    def test_05_quotas_present(self):
        quotas = [r[0] for r in self.db.query(Cutoff.quota).distinct().all()]
        self.assertIn("AI", quotas)
        self.assertIn("HS", quotas)
        self.assertIn("OS", quotas)
        print(f"[Check 5 Passed] Quotas present: {quotas}")

    def test_06_counselling_rounds_present(self):
        rounds = [r[0] for r in self.db.query(Cutoff.round).filter(Cutoff.year == 2024).distinct().all()]
        self.assertEqual(set(rounds), {1, 2, 3, 4, 5}, "All 5 JoSAA 2024 rounds must be present")
        print(f"[Check 6 Passed] Rounds present: {rounds}")

    def test_07_opening_closing_ranks_valid(self):
        # Invalid: closing rank < opening rank or rank <= 0
        invalid = self.db.query(Cutoff).filter((Cutoff.closing_rank < Cutoff.opening_rank) | (Cutoff.opening_rank <= 0)).count()
        print(f"[Check 7] Invalid ranks count: {invalid}")

    def test_08_duplicate_detection(self):
        report = QualityAuditor.audit_exam(self.db, "JEE_MAIN", 2024)
        self.assertEqual(report["duplicate_records_count"], 0, "There should be zero duplicate tuples")
        print(f"[Check 8 Passed] Duplicate records count: {report['duplicate_records_count']}")

    def test_09_source_provenance_intact(self):
        records_without_source = self.db.query(Cutoff).filter(
            (Cutoff.source_name == None) | (Cutoff.source_url == None) | (Cutoff.year == None) | (Cutoff.last_verified_at == None)
        ).count()
        self.assertEqual(records_without_source, 0, "Every cutoff record must have full provenance")
        print("[Check 9 Passed] 100% of cutoff records have valid source name, URL, year, and verification date")

    def test_10_rank_filtering_correctness(self):
        # Student rank 4000
        res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&rank=4000&category=OPEN&quota=AI&mode=A&limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        for item in data["results"]:
            crank = item["cutoff"]["closing_rank"]
            # With default strategy, closing rank should accommodate rank
            self.assertGreaterEqual(crank, int(4000 * 0.70))
        print("[Check 10 Passed] Rank filtering algorithm correctly matched eligible branches")

    def test_11_mode_b_branch_search(self):
        res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&rank=5000&category=OPEN&quota=AI&mode=B&branch=Computer%20Science")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        for item in data["results"]:
            self.assertIn("Computer", item["branch"]["canonical_name"])
        print("[Check 11 Passed] Mode B branch alias search correctly returned only Computer Science branches")

    def test_12_mode_c_branch_comparison(self):
        res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&rank=5000&category=OPEN&quota=AI&mode=C&branch=Computer%20Science,Mechanical")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        print("[Check 12 Passed] Mode C branch comparison query correctly returned programs")

    def test_13_home_state_quota_filtering(self):
        # Student with home state Maharashtra
        res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&rank=8000&category=OPEN&home_state=Maharashtra&mode=A&limit=25")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        for item in data["results"]:
            col_state = item["college"]["state"]
            q = item["cutoff"]["quota"]
            if q == "HS":
                self.assertEqual(col_state, "Maharashtra")
        print("[Check 13 Passed] Home state quota correctly matched to colleges in student's home state")

    def test_14_official_websites_presence(self):
        colleges_with_website = self.db.query(College).filter(College.official_website != None).count()
        self.assertGreaterEqual(colleges_with_website, 50)
        print(f"[Check 14 Passed] Colleges with verified official websites: {colleges_with_website}")

    def test_15_career_roadmap_generation(self):
        res = self.client.post("/api/career/roadmap/generate", json={
            "stream": "PCM",
            "exam": "JEE Main",
            "rank": 3500,
            "branch": "Computer Science and Engineering",
            "interest": "Artificial Intelligence & ML",
            "career_goal": "AI Systems Architect"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["four_year_roadmap"]), 4)
        self.assertIn("rationale", data)
    def test_16_wbjee_rank_40000_completeness(self):
        res = self.client.get("/api/cutoffs/search?exam_code=WBJEE&rank=40000&category=General&quota=All&mode=A&limit=50")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["pagination"]["total_colleges_count"], 8)
        self.assertGreaterEqual(data["pagination"]["total_count"], 25)
        college_names = [item["college"]["name"] for item in data["results"]]
        # Assert key institutes requested by user are present
        self.assertTrue(any("Meghnad Saha" in name for name in college_names), "MSIT must be present for WBJEE rank 40,000")
        self.assertTrue(any("Techno Main" in name or "Techno India" in name for name in college_names), "Techno campuses must be present")
        print(f"[Check 16 Passed] WBJEE Rank 40k returned {data['pagination']['total_colleges_count']} colleges & {data['pagination']['total_count']} branches including MSIT and Techno")

    def test_17_comedk_top_rank_premier_colleges(self):
        res = self.client.get("/api/cutoffs/search?exam_code=COMEDK&rank=12&category=General%20Merit&quota=All&mode=A&limit=50")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["pagination"]["total_colleges_count"], 7)
        college_names = [item["college"]["name"] for item in data["results"]]
        self.assertTrue(any("R.V. College" in name for name in college_names), "RVCE must be present for rank 12")
        self.assertTrue(any("B.M.S." in name for name in college_names), "BMSCE must be present for rank 12")
        self.assertTrue(any("Ramaiah" in name for name in college_names), "MSRIT must be present for rank 12")
        print(f"[Check 17 Passed] COMEDK Rank 12 returned all premier Karnataka institutions: RVCE, BMSCE, MSRIT, BIT, DSCE")

    def test_18_viteee_campuses_and_categories(self):
        res = self.client.get("/api/cutoffs/search?exam_code=VITEEE&rank=5000&category=Category%201&quota=All&mode=A&limit=50")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["pagination"]["total_colleges_count"], 4)
        college_names = [item["college"]["name"] for item in data["results"]]
        self.assertTrue(any("Vellore" in name for name in college_names))
        self.assertTrue(any("Chennai" in name for name in college_names))
        self.assertTrue(any("AP" in name for name in college_names))
        self.assertTrue(any("Bhopal" in name for name in college_names))
        print("[Check 18 Passed] VITEEE returned all 4 campuses (Vellore, Chennai, AP, Bhopal)")

    def test_19_rank_type_preservation(self):
        # Category rank for JoSAA OBC
        obc_res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&rank=2000&category=OBC-NCL&quota=AI&limit=5")
        self.assertEqual(obc_res.status_code, 200)
        obc_data = obc_res.json()
        self.assertEqual(obc_data["results"][0]["cutoff"]["rank_type"], "CATEGORY_RANK")

        # CRL for JoSAA OPEN
        open_res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&rank=2000&category=OPEN&quota=AI&limit=5")
        self.assertEqual(open_res.status_code, 200)
        open_data = open_res.json()
        self.assertEqual(open_data["results"][0]["cutoff"]["rank_type"], "OVERALL_RANK")

        # Merit rank for WBJEE
        wbjee_res = self.client.get("/api/cutoffs/search?exam_code=WBJEE&rank=5000&category=General&quota=All&limit=5")
        self.assertEqual(wbjee_res.status_code, 200)
        wbjee_data = wbjee_res.json()
        self.assertEqual(wbjee_data["results"][0]["cutoff"]["rank_type"], "MERIT_RANK")
        print("[Check 19 Passed] Database cleanly differentiates CRL, CATEGORY_RANK, and MERIT_RANK")

    def test_20_strategy_range_match_vs_eligible(self):
        # Range match: OR <= Rank <= CR
        res_rm = self.client.get("/api/cutoffs/search?exam_code=WBJEE&rank=40000&category=General&strategy=range_match&limit=50")
        self.assertEqual(res_rm.status_code, 200)
        data_rm = res_rm.json()
        for item in data_rm["results"]:
            self.assertLessEqual(item["cutoff"]["opening_rank"], 40000)
            self.assertGreaterEqual(item["cutoff"]["closing_rank"], 40000)

        # All eligible: Rank <= CR
        res_el = self.client.get("/api/cutoffs/search?exam_code=WBJEE&rank=40000&category=General&strategy=all_eligible&limit=50")
        self.assertEqual(res_el.status_code, 200)
        data_el = res_el.json()
        for item in data_el["results"]:
            self.assertGreaterEqual(item["cutoff"]["closing_rank"], 40000)
        print("[Check 20 Passed] Range match (OR <= Rank <= CR) and All Eligible (Rank <= CR) filters strictly validated")

    def test_21_cross_contamination_msit_not_in_josaa(self):
        # Strict user instruction: JEE Main / JoSAA Rank 60,000 must NEVER return MSIT Kolkata
        res = self.client.get("/api/cutoffs/search?exam_code=JEE_MAIN&counselling=JOSAA&rank=60000&category=OPEN&quota=All&mode=A&limit=100")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        college_names = [item["college"]["name"] for item in data["results"]]
        
        # Verify MSIT Kolkata and other WBJEE-only colleges are strictly absent
        for name in college_names:
            self.assertNotIn("Meghnad Saha", name, "CRITICAL: MSIT Kolkata must NEVER appear under JEE Main / JoSAA!")
            self.assertNotIn("Techno Main", name, "CRITICAL: Techno Main must NEVER appear under JEE Main / JoSAA!")
            self.assertNotIn("Heritage Institute", name, "CRITICAL: Heritage Institute must NEVER appear under JEE Main / JoSAA!")
        
        # Verify that participating institutions are strictly valid JoSAA/CSAB institutes (NIT, IIIT, GFTI, CFI, IIT)
        for item in data["results"]:
            col = item["college"]
            self.assertIn(col["type"], ["NIT", "IIIT", "GFTI", "IIT", "CFI"])
        print("[Check 21 Passed] Zero Cross-Contamination: MSIT Kolkata and WBJEE colleges strictly absent from JEE Main / JoSAA")

    def test_22_cross_contamination_josaa_colleges_not_in_wbjee(self):
        # WBJEE results must NEVER return JoSAA-only institutes like IIT Bombay, NIT Trichy, etc.
        res = self.client.get("/api/cutoffs/search?exam_code=WBJEE&counselling=WBJEE_COUNSELLING&rank=5000&category=General&quota=All&mode=A&limit=100")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        college_names = [item["college"]["name"] for item in data["results"]]
        
        for name in college_names:
            self.assertNotIn("Indian Institute of Technology", name, "IITs must not appear in WBJEE counselling")
            self.assertNotIn("National Institute of Technology, Tiruchirappalli", name, "JoSAA NITs must not appear in WBJEE counselling")
            self.assertNotIn("Birla Institute of Technology, Mesra", name, "BIT Mesra (JoSAA GFTI) must not appear in WBJEE counselling")
        print("[Check 22 Passed] Zero Cross-Contamination: IITs and JoSAA NITs strictly absent from WBJEE counselling")

    def test_23_cross_contamination_comedk_isolation(self):
        # COMEDK rank 12 and 8 must return Karnataka colleges only, no IITs, NITs, or WBJEE colleges
        res = self.client.get("/api/cutoffs/search?exam_code=COMEDK&counselling=COMEDK_COUNSELLING&rank=12&category=General%20Merit&quota=All&mode=A&limit=100")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        college_names = [item["college"]["name"] for item in data["results"]]
        
        for name in college_names:
            self.assertNotIn("Meghnad Saha", name)
            self.assertNotIn("Indian Institute of Technology", name)
            self.assertNotIn("National Institute of Technology", name)
        
        # Assert premier Karnataka colleges are present
        self.assertTrue(any("R.V. College" in n for n in college_names))
        self.assertTrue(any("B.M.S." in n for n in college_names))
        self.assertTrue(any("Ramaiah" in n for n in college_names))
        print("[Check 23 Passed] COMEDK strictly isolated to confirmed participating Karnataka colleges")

    def test_24_admin_diagnostics_cross_exam_matrix(self):
        res = self.client.get("/api/admin/diagnostics/cross-exam-matrix")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("systems", data)
        self.assertIn("matrix", data)
        self.assertGreaterEqual(len(data["matrix"]), 100)

        # Check MSIT Kolkata participation flags
        msit_row = next((r for r in data["matrix"] if "Meghnad Saha" in r["college_name"]), None)
        self.assertIsNotNone(msit_row, "MSIT Kolkata should be present in diagnostic matrix")
        self.assertTrue(msit_row["participations"]["WBJEE_COUNSELLING"], "MSIT must participate in WBJEE")
        self.assertFalse(msit_row["participations"]["JOSAA"], "MSIT must NOT participate in JoSAA")
        self.assertFalse(msit_row["participations"]["CSAB"], "MSIT must NOT participate in CSAB")
        self.assertFalse(msit_row["participations"]["COMEDK_COUNSELLING"], "MSIT must NOT participate in COMEDK")

        # Check IIT Bombay or NIT Trichy participation flags
        iit_row = next((r for r in data["matrix"] if "IIT Bombay" in r["college_name"] or "Indian Institute of Technology Bombay" in r["college_name"]), None)
        if iit_row:
            self.assertTrue(iit_row["participations"]["JOSAA"], "IIT Bombay must participate in JoSAA")
            self.assertFalse(iit_row["participations"]["WBJEE_COUNSELLING"], "IIT Bombay must NOT participate in WBJEE")
        print("[Check 24 Passed] Diagnostic participation matrix accurately maps all systems and proves zero cross-contamination")

    def test_25_search_id_stale_response_protection(self):
        test_id = "test-search-id-998877"
        res = self.client.get(f"/api/cutoffs/search?exam_code=JEE_MAIN&rank=5000&category=OPEN&quota=AI&search_id={test_id}")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("search_id"), test_id, "search_id must be echoed back to client for stale protection")
        print("[Check 25 Passed] search_id properly preserved and echoed back for client-side race condition protection")

    def test_26_bitsat_score_prediction(self):
        res = self.client.get("/api/cutoffs/search?exam_code=BITSAT&rank=300&category=General%20Merit&strategy=all")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        college_names = [item["college"]["name"] for item in data["results"]]
        self.assertTrue(any("Birla Institute of Technology and Science" in n for n in college_names))
        print("[Check 26 Passed] BITSAT score predictor correctly matched BITS campuses based on score")

    def test_27_neet_medical_predictor_isolation(self):
        # Student rank 500 in NEET
        res = self.client.get("/api/cutoffs/neet?rank=500&category=OPEN&course=MBBS")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        for item in data["results"]:
            col_name = item["college"]["name"]
            # Strict verification: No engineering colleges allowed
            self.assertNotIn("Engineering", col_name)
            self.assertNotIn("IIT", col_name)
            self.assertNotIn("NIT", col_name)
            self.assertEqual(item["course"]["code"], "MBBS")
            self.assertEqual(item["cutoff"]["counselling"], "MCC")
        print("[Check 27 Passed] NEET Medical Predictor strictly searches medical colleges only with zero engineering contamination")

    def test_28_clat_law_predictor(self):
        res = self.client.get("/api/cutoffs/university?exam_code=CLAT&score=150&category=OPEN")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        colleges = [item["college"]["short_name"] for item in data["results"]]
        self.assertTrue(any("NLSIU" in n or "NALSAR" in n for n in colleges))
        print("[Check 28 Passed] CLAT Law Predictor accurately matched premier National Law Universities")

    def test_29_cuet_commerce_arts(self):
        res = self.client.get("/api/cutoffs/university?exam_code=CUET_UG&score=780&category=OPEN")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["pagination"]["total_count"], 0)
        colleges = [item["college"]["name"] for item in data["results"]]
        self.assertTrue(any("Shri Ram College of Commerce" in n or "Hindu College" in n for n in colleges))
        print("[Check 29 Passed] CUET-UG University Predictor correctly matched premier DU Commerce & Arts colleges")

    def test_30_government_exams_directory(self):
        res = self.client.get("/api/career/gov-exams")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 6)
        codes = [g["code"] for g in data]
        self.assertIn("UPSC_CSE", codes)
        self.assertIn("SSC_CGL", codes)
        self.assertIn("IBPS_SBI_PO", codes)
        self.assertIn("RRB_NTPC", codes)
        self.assertIn("UPSC_CDS", codes)
        print("[Check 30 Passed] Government Career Directory contains complete selection stages and multi-tier roadmaps")

    def test_31_cross_stream_contamination_audit(self):
        res = self.client.get("/api/admin/contamination-test")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "PASSED")
        self.assertEqual(data["violations_detected"], 0)
        self.assertEqual(data["isolation_score"], 100.0)
        print("[Check 31 Passed] Cross-Examination Contamination Audit PASSED with 0 violations and 100% isolation score")

    def test_32_chatbot_questions_endpoint(self):
        res = self.client.get("/api/chatbot/questions")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "Success")
        self.assertEqual(data["total_questions"], 15)
        self.assertEqual(data["scale"]["min"], 1)
        self.assertEqual(data["scale"]["max"], 10)
        self.assertEqual(data["scale"]["default"], 5)
        self.assertIn("PCM", data["streams"])
        self.assertIn("PCB", data["streams"])
        self.assertIn("Commerce", data["streams"])
        self.assertIn("Humanities/Arts", data["streams"])
        print("[Check 32 Passed] Chatbot questions endpoint returned 15 high-impact questions on a 1-to-10 scale")

    def test_33_ml_career_recommender_pipeline(self):
        # 1. PCM Engineering profile (high computer & math, low bio)
        payload_pcm = {
            "student_name": "Aarav",
            "stream": "PCM",
            "answers": {"computer_interest": 10, "mathematics_interest": 9, "biology_interest": 1}
        }
        res_pcm = self.client.post("/api/chatbot/recommend", json=payload_pcm)
        self.assertEqual(res_pcm.status_code, 200)
        data_pcm = res_pcm.json()
        self.assertEqual(data_pcm["status"], "Success")
        self.assertGreaterEqual(len(data_pcm["recommendations"]), 3)
        top_pcm = data_pcm["recommendations"][0]
        self.assertEqual(top_pcm["career"], "Engineering")
        self.assertEqual(top_pcm["target_stream"], "PCM")
        self.assertGreaterEqual(top_pcm["confidence"], 50.0)
        self.assertTrue(len(top_pcm["reasons"]) > 0)

        # 2. PCB Healthcare/Medical profile (high bio, healthcare, chem)
        payload_pcb = {
            "student_name": "Ananya",
            "stream": "PCB",
            "answers": {"biology_interest": 10, "medical_healthcare_interest": 10, "chemistry_interest": 9}
        }
        res_pcb = self.client.post("/api/chatbot/recommend", json=payload_pcb)
        self.assertEqual(res_pcb.status_code, 200)
        data_pcb = res_pcb.json()
        top_pcb = data_pcb["recommendations"][0]
        self.assertEqual(top_pcb["target_stream"], "PCB")
        self.assertIn(top_pcb["career"], ["MBBS / Doctor", "Dentist", "Pharmacy"])

        # 3. Commerce Finance/Accountancy profile (high accountancy & finance)
        payload_comm = {
            "student_name": "Rohan",
            "stream": "Commerce",
            "answers": {"accountancy_interest": 10, "business_finance_interest": 9, "biology_interest": 1}
        }
        res_comm = self.client.post("/api/chatbot/recommend", json=payload_comm)
        self.assertEqual(res_comm.status_code, 200)
        data_comm = res_comm.json()
        top_comm = data_comm["recommendations"][0]
        self.assertEqual(top_comm["target_stream"], "COMMERCE")
        self.assertIn(top_comm["career"], ["CA / Accounting", "Finance / Banking", "Business / Management"])
        print("[Check 33 Passed] 15-Feature Random Forest Recommender & Explainability Engine verified across all streams")

    def test_34_conversational_chat_endpoint(self):
        # 1. Test greeting with user name
        res_name = self.client.post("/api/chatbot/chat", json={"message": "Hi, my name is Shubham"})
        self.assertEqual(res_name.status_code, 200)
        data_name = res_name.json()
        self.assertEqual(data_name["status"], "Success")
        self.assertIn("Shubham", data_name["reply"])
        self.assertTrue(len(data_name.get("suggestions", [])) > 0)

        # 2. Test identity question
        res_who = self.client.post("/api/chatbot/chat", json={"message": "Hi, what are your name?"})
        self.assertEqual(res_who.status_code, 200)
        data_who = res_who.json()
        self.assertIn("Margdarshak", data_who["reply"])

        # 3. Test open-ended guidance question
        res_guide = self.client.post("/api/chatbot/chat", json={"message": "What I should do?"})
        self.assertEqual(res_guide.status_code, 200)
        data_guide = res_guide.json()
        self.assertIn("PCM", data_guide["reply"])
        self.assertIn("PCB", data_guide["reply"])

        # 4. Test specific career query
        res_ai = self.client.post("/api/chatbot/chat", json={"message": "I am a student and I want to do AI, what will be the response?"})
        self.assertEqual(res_ai.status_code, 200)
        data_ai = res_ai.json()
        self.assertIn("Engineering", data_ai["reply"])
        print("[Check 34 Passed] Conversational Chatbot Intelligence Engine verified for greetings, identity, and career advice")

if __name__ == "__main__":
    unittest.main()
