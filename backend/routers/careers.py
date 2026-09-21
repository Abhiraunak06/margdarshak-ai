import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.schema import CareerPath, GovernmentExam

router = APIRouter(prefix="/api/career", tags=["Career Guidance"])

class RoadmapRequest(BaseModel):
    stream: str = "PCM" # PCM, PCB, COMMERCE, ARTS
    exam: str
    rank: int
    branch: Optional[str] = "Computer Science and Engineering"
    interest: str = "Software Development"
    career_goal: Optional[str] = "Product Company Software Engineer / Tech Lead"

@router.get("/paths")
def get_career_paths(stream: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(CareerPath)
    if stream:
        st_upper = stream.strip().upper()
        if st_upper in ["PCM", "ENGINEERING"]:
            query = query.filter(CareerPath.stream == "PCM")
        elif st_upper in ["PCB", "MEDICAL"]:
            query = query.filter(CareerPath.stream == "PCB")
        elif st_upper in ["COMMERCE", "FINANCE"]:
            query = query.filter(CareerPath.stream == "COMMERCE")
        elif st_upper in ["ARTS", "HUMANITIES"]:
            query = query.filter(CareerPath.stream == "ARTS")
        else:
            query = query.filter(CareerPath.stream == stream)

    paths = query.all()
    results = []
    for p in paths:
        try:
            steps = json.loads(p.roadmap_steps)
        except Exception:
            steps = []
        results.append({
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "stream": p.stream or "PCM",
            "domain": p.domain,
            "description": p.description,
            "required_skills": [s.strip() for s in p.required_skills.split(",")],
            "recommended_degrees": [d.strip() for d in p.recommended_degrees.split(",")],
            "relevant_branches": [b.strip() for b in p.relevant_branches.split(",")],
            "entrance_exams": [e.strip() for e in p.entrance_exams.split(",")],
            "average_starting_salary_lpa": p.average_starting_salary_lpa,
            "growth_outlook": p.growth_outlook,
            "roadmap_steps": steps
        })
    return results

@router.get("/gov-exams")
def list_government_exams(db: Session = Depends(get_db)):
    exams = db.query(GovernmentExam).all()
    results = []
    for g in exams:
        try:
            stages = json.loads(g.selection_stages)
        except Exception:
            stages = []
        try:
            prep_roadmap = json.loads(g.preparation_roadmap)
        except Exception:
            prep_roadmap = []

        results.append({
            "id": g.id,
            "title": g.title,
            "code": g.code,
            "conducting_body": g.conducting_body,
            "sector": g.sector,
            "eligibility_education": g.eligibility_education,
            "min_age": g.min_age,
            "max_age": g.max_age,
            "selection_stages": stages,
            "syllabus_overview": g.syllabus_overview,
            "career_roles": [r.strip() for r in g.career_roles.split(",")],
            "salary_scale": g.salary_scale,
            "official_website": g.official_website,
            "application_window": g.application_window,
            "preparation_roadmap": prep_roadmap
        })
    return results

@router.get("/paths/{slug}")
def get_career_path_by_slug(slug: str, db: Session = Depends(get_db)):
    p = db.query(CareerPath).filter(CareerPath.slug == slug).first()
    if not p:
        raise HTTPException(status_code=404, detail="Career path not found")

    try:
        steps = json.loads(p.roadmap_steps)
    except Exception:
        steps = []

    return {
        "id": p.id,
        "title": p.title,
        "slug": p.slug,
        "domain": p.domain,
        "description": p.description,
        "required_skills": [s.strip() for s in p.required_skills.split(",")],
        "recommended_degrees": [d.strip() for d in p.recommended_degrees.split(",")],
        "relevant_branches": [b.strip() for b in p.relevant_branches.split(",")],
        "entrance_exams": [e.strip() for e in p.entrance_exams.split(",")],
        "average_starting_salary_lpa": p.average_starting_salary_lpa,
        "growth_outlook": p.growth_outlook,
        "roadmap_steps": steps
    }

@router.post("/roadmap/generate")
def generate_personalized_roadmap(req: RoadmapRequest, db: Session = Depends(get_db)):
    stream_upper = (req.stream or "PCM").strip().upper()
    interest_lower = (req.interest or "").lower()

    if stream_upper in ["PCB", "MEDICAL"]:
        rationale = (
            f"Based on your entrance exam ({req.exam}) with rank {req.rank:,} and aspiration in '{req.interest}', "
            f"pursuing {req.branch or 'Medical / Healthcare sciences'} equips you with clinical diagnostic capabilities, patient care expertise, and healthcare leadership. "
            f"This pathway provides comprehensive pre-clinical, para-clinical, clinical ward postings, and rotating medical internship training."
        )
        steps = [
            {
                "phase": "Year 1 (Pre-Clinical): Anatomy, Physiology & Biochemistry Foundations",
                "academic_focus": "Gross Anatomy & Cadaveric Dissection, Histology, General Physiology, Clinical Biochemistry",
                "core_skills": ["Cadaveric Dissection", "Microscopic Histopathology", "Biochemical Blood Chemistry", "Medical Terminology"],
                "milestone_projects": ["Anatomical variations research poster presentation", "Basal metabolic rate and endocrine feedback clinical case study"],
                "certifications_recommendation": "Basic Life Support (BLS) & Cardiopulmonary Resuscitation (CPR) Certification"
            },
            {
                "phase": "Year 2 (Para-Clinical): Pathology, Microbiology & Pharmacology",
                "academic_focus": "Systemic Pathology, Medical Microbiology, Antimicrobial Pharmacology, Forensic Medicine & Toxicology",
                "core_skills": ["Histopathological Staining", "Culture & Antibiotic Sensitivity Testing", "Pharmacokinetics Calculation", "Medico-Legal Documentation"],
                "milestone_projects": ["Hospital nosocomial infection surveillance report", "Adverse Drug Reaction (ADR) pharmacovigilance audit"],
                "certifications_recommendation": "ICMR Short Term Studentship (STS) Clinical Research Project"
            },
            {
                "phase": "Years 3 & 4 (Clinical Postings): Bedside Diagnosis, Surgery & Pediatrics",
                "academic_focus": "Internal Medicine, General Surgery, Pediatrics, Obstetrics & Gynecology, Community Health",
                "core_skills": ["Patient History Taking", "Bedside Physical Examination", "Suturing & Wound Care", "ECG & Chest X-Ray Interpretation"],
                "milestone_projects": ["Rural primary health centre community health survey", "Grand clinical ward rounds presentation under Senior Consultant"],
                "certifications_recommendation": "Advanced Cardiac Life Support (ACLS) & Pediatric Advanced Life Support (PALS)"
            },
            {
                "phase": "Internship Year: Compulsory Rotating Medical Internship (CRMI) & NExT/NEET-PG",
                "academic_focus": "Casualty / Emergency Medicine, Intensive Care Unit (ICU), Labor Ward, Rural PHC",
                "core_skills": ["Emergency Triage", "Intravenous Cannulation & Arterial Blood Gas", "Patient Stabilization", "NExT / NEET-PG Competitive Prep"],
                "milestone_projects": ["Primary management of 100+ emergency acute trauma cases", "NExT / NEET-PG exam cracking strategy"],
                "certifications_recommendation": "Permanent Medical Registration with National Medical Commission (NMC)"
            }
        ]
        recs = [
            "Maintain meticulous clinical bedside logs during hospital postings.",
            "Complete an ICMR Short Term Studentship (STS) research project to bolster post-graduate residency applications.",
            "Start solving clinical scenario question banks (Marrow/Prepladder) early in Phase 3 for NExT / NEET-PG readiness.",
            "Cultivate empathetic patient communication and bioethics compliance."
        ]

    elif stream_upper in ["COMMERCE", "FINANCE"]:
        rationale = (
            f"Based on your examination ({req.exam}) and focus on '{req.interest}', "
            f"your path in {req.branch or 'Commerce & Management'} leads to premier corporate leadership, auditing advisory, and financial market strategy. "
            f"This roadmap synchronizes academic degree rigor with professional qualifications (CA/CS/CMA/CFA) and practical industrial articleship."
        )
        if "ca" in interest_lower or "chartered" in interest_lower or "audit" in interest_lower:
            steps = [
                {
                    "phase": "Stage 1 (Months 1-6): CA Foundation & Accounting Principles",
                    "academic_focus": "Principles of Accounting, Business Laws, Quantitative Aptitude, Business Economics",
                    "core_skills": ["Double-entry Bookkeeping", "Partnership Accounts", "Contract Act 1872", "Macroeconomic Analysis"],
                    "milestone_projects": ["Preparation of complete financial statements for small manufacturing firm", "Business law case brief portfolio"],
                    "certifications_recommendation": "ICAI Foundation Examination (Clear with 50%+ aggregate)"
                },
                {
                    "phase": "Stage 2 (Months 7-16): CA Intermediate Group 1 & Group 2",
                    "academic_focus": "Advanced Accounting (Ind AS), Corporate Laws, Taxation (Direct & GST), Auditing & Ethics, Strategic Financial Management",
                    "core_skills": ["Ind AS Compliance", "Income Tax Computation", "GST Filing & Reconciliation", "Statutory Audit Checklists"],
                    "milestone_projects": ["Tax planning and return filing case simulation", "Internal audit operational review of retail company"],
                    "certifications_recommendation": "ICITSS (Information Technology & Orientation Course)"
                },
                {
                    "phase": "Stage 3 (Years 2 & 3): 2-Year Mandatory Articleship Training",
                    "academic_focus": "Hands-on statutory audit, corporate tax litigation, transfer pricing, bank concurrent audit",
                    "core_skills": ["SAP / Tally ERP Audit", "Vouching & Verification", "Due Diligence Reporting", "Client Board Representation"],
                    "milestone_projects": ["Statutory audit of listed entity or scheduled commercial bank branch", "Tax assessment appeal drafting before CIT(A)"],
                    "certifications_recommendation": "Advanced ICITSS (Information Technology & Management Soft Skills)"
                },
                {
                    "phase": "Stage 4 (Final Year): CA Final Examination & ACA Membership",
                    "academic_focus": "Financial Reporting, Advanced Financial Management, Advanced Auditing, Direct & International Taxation",
                    "core_skills": ["M&A Valuation", "Consolidated Financial Statements", "International Transfer Pricing", "Corporate Advisory"],
                    "milestone_projects": ["Comprehensive DCF business valuation and pitchbook", "Clearing CA Final Both Groups"],
                    "certifications_recommendation": "Associate Chartered Accountant (ACA) Membership with ICAI"
                }
            ]
        else:
            steps = [
                {
                    "phase": "Year 1: Financial Accounting & Advanced Business Excel",
                    "academic_focus": "Financial Accounting, Microeconomics, Business Statistics, Business Mathematics",
                    "core_skills": ["Advanced Excel (VLOOKUP, INDEX-MATCH, Pivot, What-If Analysis)", "Financial Ratio Analysis", "Business Writing"],
                    "milestone_projects": ["Comparative 5-year financial statement analysis of Nifty 50 companies", "Automated Excel financial dashboard"],
                    "certifications_recommendation": "Wall Street Prep / CFI Financial Modeling & Valuation Analyst (FMVA)"
                },
                {
                    "phase": "Year 2: Corporate Finance, Valuation & Capital Markets",
                    "academic_focus": "Corporate Finance, Macroeconomics, Investment Analysis, Cost Accounting",
                    "core_skills": ["Discounted Cash Flow (DCF) Modeling", "Comparable Company Valuation", "Equity Research Report Writing"],
                    "milestone_projects": ["Initiating coverage equity research report on Indian FMCG or IT sector", "Bloomberg / Capitaline terminal financial extraction"],
                    "certifications_recommendation": "NISM Series VIII (Equity Derivatives) & CFA Level I Registration"
                },
                {
                    "phase": "Year 3: Summer Internship & CFA Level I",
                    "academic_focus": "Portfolio Management, International Finance, Financial Econometrics, Business Law",
                    "core_skills": ["LBO Modeling", "Mergers & Acquisitions Deal Structuring", "Credit Risk Evaluation", "Pitchbooks"],
                    "milestone_projects": ["Summer Analyst Internship at Investment Bank or Big 4 Transaction Advisory", "Cross-border M&A synergy case model"],
                    "certifications_recommendation": "Clear CFA Level I Examination"
                },
                {
                    "phase": "Final Placement: Pre-Placement Offers & Consulting Hiring",
                    "academic_focus": "Strategic Management, Enterprise Risk Governance, Capstone Thesis",
                    "core_skills": ["Case Interview Frameworks (Profitability, Market Entry, M&A)", "High-level Executive Pitching", "Financial Due Diligence"],
                    "milestone_projects": ["End-to-end IPO roadshow deck and valuation memo", "Campus Placement Shortlists"],
                    "certifications_recommendation": "Secure Analyst role at Tier-1 Investment Bank, Big 4, or FMCG Management"
                }
            ]
        recs = [
            "Build an active financial portfolio tracking public equities on screener.in and Excel.",
            "Prepare for competitive finance certifications like CFA Level 1 or NISM certifications alongside graduation.",
            "Complete at least two structured corporate finance or auditing internships.",
            "Master presentation skills and case analysis frameworks for management consulting rounds."
        ]

    elif stream_upper in ["ARTS", "HUMANITIES"]:
        rationale = (
            f"Based on your entrance exam ({req.exam}) with rank {req.rank:,} and career focus on '{req.interest}', "
            f"your path in {req.branch or 'Humanities & Social Sciences'} builds critical inquiry, legal analysis, public policy design, and administrative stewardship. "
            f"This roadmap bridges intellectual breadth with competitive civil services / law / policy recruitment benchmarks."
        )
        if "law" in interest_lower or "legal" in interest_lower or "clat" in interest_lower:
            steps = [
                {
                    "phase": "Year 1: Legal Methods & Law of Torts / Contracts",
                    "academic_focus": "Legal Methods, Law of Torts, General Principles of Contract, Constitutional History",
                    "core_skills": ["Case Briefing & Analysis", "Legal Citation (Bluebook)", "SCC Online & Manupatra Research", "Intra-Moot Court Advocacy"],
                    "milestone_projects": ["First intra-university moot court memorial drafting", "Legal article on Consumer Protection Act in student law review"],
                    "certifications_recommendation": "Winter Judicial Clerkship or Trial Court Advocate Internship"
                },
                {
                    "phase": "Year 2: Criminal Law, Family Law & High Court Internships",
                    "academic_focus": "Indian Penal Code (IPC/BNS), Criminal Procedure (CrPC/BNSS), Law of Evidence, Family Law",
                    "core_skills": ["Bail Application Drafting", "Cross-examination Observation", "Statutory Interpretation", "Legal Aid Clinic Work"],
                    "milestone_projects": ["Legal aid camp documentation on fundamental rights awareness", "Inter-university national moot court competition"],
                    "certifications_recommendation": "Summer Internship under Senior Advocate at High Court"
                },
                {
                    "phase": "Year 3 & 4: Corporate Law, Commercial Disputes & Tier-1 Law Firm Stints",
                    "academic_focus": "Companies Act 2013, Insolvency & Bankruptcy Code (IBC), Competition Law, Arbitration & ADR, Intellectual Property",
                    "core_skills": ["Due Diligence Review", "Commercial Contract Drafting (Shareholders Agreement, NDA)", "Arbitration Claim Statements"],
                    "milestone_projects": ["Publication in Scopus-indexed law journal on corporate insolvency", "Assessment internship at top law firm (SAM/CAM/Trilegal/Khaitan)"],
                    "certifications_recommendation": "WIPO Intellectual Property Certificate or Harvard Negotiation Program"
                },
                {
                    "phase": "Year 5: Pre-Placement Offers, Bar Council Enrollment & Judiciary Prep",
                    "academic_focus": "Professional Ethics, Taxation Law, International Trade Law, Capstone Dissertation",
                    "core_skills": ["Final Placement Day Zero Interviews", "Bar Council of India All India Bar Examination (AIBE) Prep", "Judicial Services Prelims"],
                    "milestone_projects": ["Comprehensive legal dissertation on emerging AI and privacy jurisprudence", "Securing Corporate Law Associate PPO"],
                    "certifications_recommendation": "Bar Council of India Enrollment & Advocate Licensing"
                }
            ]
        else:
            steps = [
                {
                    "phase": "College Year 1: NCERT Foundations & Analytical Reading",
                    "academic_focus": "History, Political Science, Geography, Sociology, Foundations of Economics",
                    "core_skills": ["Critical Source Evaluation", "Newspaper Analytical Reading (The Hindu / Indian Express)", "Descriptive Essay Writing", "Public Speaking"],
                    "milestone_projects": ["Comparative research paper on Indian federalism and grassroots panchayati raj", "Daily 1.5-hour current affairs digest maintenance"],
                    "certifications_recommendation": "NPTEL / Coursera Public Policy & Governance Course"
                },
                {
                    "phase": "College Year 2: Standard Reference Works & Academic Research",
                    "academic_focus": "Indian Polity & Constitution (M. Laxmikanth), Modern Indian History (Spectrum), Environment & Biodiversity (Shankar IAS)",
                    "core_skills": ["Structured Answer Writing (Intro-Body-Conclusion format)", "Diagrammatic Representation of Social Concepts", "Qualitative Survey Design"],
                    "milestone_projects": ["Field study on implementation of public welfare schemes (MGNREGA / PDS)", "College departmental journal editorial leadership"],
                    "certifications_recommendation": "Summer Policy Research Internship at Think Tank (CPR / NITI Aayog / Observer Research Foundation)"
                },
                {
                    "phase": "College Year 3: Optional Subject Mastery & Answer Writing Drills",
                    "academic_focus": "Full completion of UPSC CSE Optional syllabus (e.g., Political Science & IR, Sociology, History, or Geography)",
                    "core_skills": ["Daily GS Answer Writing (2 answers/day evaluated against UPSC model answers)", "Map Marking & Diagram Integration", "Ethics Case Study Analysis"],
                    "milestone_projects": ["Complete coverage of 10-year previous UPSC CSE Mains question papers", "Graduation Degree completion with First Class Honors"],
                    "certifications_recommendation": "UGC-NET Examination (upon eligibility) or Central University Entrance"
                },
                {
                    "phase": "Final Sprint / Attempt Phase: Full Mock Simulation & Civil Services Examination",
                    "academic_focus": "Yearly Current Affairs compilation (Vision/Insights), Economic Survey, Union Budget, CSAT Speed Drills",
                    "core_skills": ["100-question Prelims Mock Tests in 120 mins with negative marking minimization", "3-hour Mains Essay writing sprint", "Personality & DAF interview preparation"],
                    "milestone_projects": ["Solve 50+ full-length UPSC Prelims mock tests scoring consistently >= 105 marks in GS 1", "Appearing for UPSC Civil Services Prelims"],
                    "certifications_recommendation": "Civil Services Prelims Qualification -> Mains Intensive Preparation"
                }
            ]
        recs = [
            "Develop a disciplined daily reading habit covering national editorial opinions and international developments.",
            "Start answer writing practice early using previous year question papers to build time management and clarity.",
            "Seek summer internships at policy think tanks, research institutes, or NGOs to gain empirical field experience.",
            "Maintain high graduation grades to keep doors open for top Central Universities (JNU, DSE, TISS) and international master's fellowships."
        ]

    else:
        # Default PCM Engineering Roadmap
        rationale = (
            f"Based on your entrance exam ({req.exam}) with rank {req.rank:,} and interest in '{req.interest}', "
            f"pursuing {req.branch or 'engineering'} positions you well for high-impact roles in the Indian and global technology sectors. "
            f"The roadmap balances foundational academic excellence with competitive programming, open source projects, and industrial internships."
        )
        if "ai" in interest_lower or "machine learning" in interest_lower or "data" in interest_lower:
            steps = [
                {
                    "phase": "Year 1 (Semesters 1 & 2): Strong Mathematical Foundation & Python Mastery",
                    "academic_focus": "Engineering Mathematics (Linear Algebra, Calculus, Statistics) & Introduction to Programming",
                    "core_skills": ["Python", "NumPy", "Pandas", "Matplotlib", "Git & GitHub"],
                    "milestone_projects": ["Data analysis on real-world Indian demographic/climate datasets", "Automated web data extraction and visualization"],
                    "certifications_recommendation": "DeepLearning.AI Mathematics for Machine Learning Specialization"
                },
                {
                    "phase": "Year 2 (Semesters 3 & 4): Core Algorithms & Classical Machine Learning",
                    "academic_focus": "Data Structures & Algorithms, Discrete Math, Database Management Systems",
                    "core_skills": ["Scikit-Learn", "PyTorch Basics", "SQL", "Feature Engineering"],
                    "milestone_projects": ["Predictive housing/salary price model with end-to-end evaluation", "Participate in Kaggle Community competitions"],
                    "certifications_recommendation": "Andrew Ng's Machine Learning Specialization"
                },
                {
                    "phase": "Year 3 (Semesters 5 & 6): Deep Learning, LLMs & Industrial Internships",
                    "academic_focus": "Operating Systems, Computer Networks, Deep Learning Architectures",
                    "core_skills": ["Transformers & Hugging Face", "LangChain / LlamaIndex", "FastAPI", "Docker", "MLOps"],
                    "milestone_projects": ["Custom Document RAG Q&A Assistant using open-source LLMs", "Production model serving pipeline with CI/CD"],
                    "certifications_recommendation": "Summer Research or Industrial AI Internship"
                },
                {
                    "phase": "Year 4 (Semesters 7 & 8): Capstone Systems, High-Level Design & Placements",
                    "academic_focus": "Distributed Systems, AI Ethics, Capstone Thesis",
                    "core_skills": ["Model Quantization", "Triton Server", "System Design for ML", "Interview DSA prep"],
                    "milestone_projects": ["Multi-modal AI assistant or published IEEE conference paper", "Production-scale LLM agent system"],
                    "certifications_recommendation": "Campus Placement Drives & Off-Campus Hiring"
                }
            ]
        elif "vlsi" in interest_lower or "hardware" in interest_lower or "core" in interest_lower or "robotics" in interest_lower:
            steps = [
                {
                    "phase": "Year 1 (Semesters 1 & 2): Fundamentals of Electrical & Logic Circuits",
                    "academic_focus": "Network Analysis, Engineering Physics, C Programming",
                    "core_skills": ["Boolean Logic", "K-Maps", "Breadboard Prototyping", "C/C++"],
                    "milestone_projects": ["Digital clock with discrete logic ICs", "Microcontroller sensor interface (Arduino/ESP32)"],
                    "certifications_recommendation": "NPTEL Basic Electrical & Electronics"
                },
                {
                    "phase": "Year 2 (Semesters 3 & 4): Hardware Description Languages & Digital Design",
                    "academic_focus": "Digital Electronics, Signals & Systems, Computer Architecture",
                    "core_skills": ["Verilog HDL", "ModelSim Simulation", "FPGA Vivado Basics", "Linux"],
                    "milestone_projects": ["Design of an 8-bit ALU in Verilog with testbench verification", "UART protocol transmitter/receiver"],
                    "certifications_recommendation": "NPTEL VLSI Design / IEEE Student Branch project"
                },
                {
                    "phase": "Year 3 (Semesters 5 & 6): Advanced RTL, ASIC Flow & Core Internships",
                    "academic_focus": "CMOS Analog Design, Control Systems, Microprocessors",
                    "core_skills": ["SystemVerilog", "UVM verification basics", "Static Timing Analysis (STA)", "EDA Tools"],
                    "milestone_projects": ["Pipelined RISC-V 32-bit single cycle core in Verilog", "Synthesis on Xilinx Artix-7 FPGA"],
                    "certifications_recommendation": "Internship at semiconductor design firms (TI, Qualcomm, NXP, Intel)"
                },
                {
                    "phase": "Year 4 (Semesters 7 & 8): Physical Design, Verification & Placements",
                    "academic_focus": "VLSI Testing, Embedded RTOS, Capstone Project",
                    "core_skills": ["Floorplanning & Routing", "Clock Tree Synthesis", "Domain Specific Architecture"],
                    "milestone_projects": ["Full taped-out ASIC design using open-source OpenLane/SkyWater 130nm PDK", "Major Capstone Design"],
                    "certifications_recommendation": "Core company placement drives & GATE exam preparation for M.Tech/PSUs"
                }
            ]
        else:
            steps = [
                {
                    "phase": "Year 1 (Semesters 1 & 2): Programming Fundamentals & Problem Solving",
                    "academic_focus": "Engineering Mathematics, Basics of Electrical/Electronics, C/C++ Programming",
                    "core_skills": ["C++ / Java", "Object-Oriented Programming (OOP)", "Git & GitHub", "Basic Data Structures"],
                    "milestone_projects": ["Terminal-based management system in C++", "Personal developer portfolio website on GitHub Pages"],
                    "certifications_recommendation": "CS50 Introduction to Computer Science"
                },
                {
                    "phase": "Year 2 (Semesters 3 & 4): Advanced DSA & Full-Stack Development",
                    "academic_focus": "Data Structures & Algorithms, Database Management Systems, Discrete Mathematics",
                    "core_skills": ["Trees, Graphs, DP", "React / Next.js", "Node.js / Express", "PostgreSQL / MongoDB"],
                    "milestone_projects": ["Full-stack e-commerce or collaborative notes app with authentication and payment gateway", "Competitive programming on Codeforces/LeetCode (250+ questions)"],
                    "certifications_recommendation": "Meta Front-End or Backend Professional Certificate"
                },
                {
                    "phase": "Year 3 (Semesters 5 & 6): Core CS Fundamentals, System Design & Summer Internships",
                    "academic_focus": "Operating Systems, Computer Networks, Low-Level Design (LLD)",
                    "core_skills": ["Docker", "Redis", "Kafka", "RESTful APIs & GraphQL", "Microservices Architecture"],
                    "milestone_projects": ["Real-time collaborative whiteboard or chat system using WebSockets & Redis pub/sub", "Open source contributions to popular GitHub repositories"],
                    "certifications_recommendation": "Summer Internship at Tier-1 product tech companies / unicorns"
                },
                {
                    "phase": "Year 4 (Semesters 7 & 8): High-Level System Design & Campus Hiring",
                    "academic_focus": "Cloud Computing, Information Security, Final Year Capstone Project",
                    "core_skills": ["High-Level System Design (HLD)", "Concurrency & Multi-threading", "Scalability & Caching", "Mock Technical Interviews"],
                    "milestone_projects": ["Production distributed rate-limiter and URL shortener handling 10k req/sec", "Complete Capstone Engineering Project"],
                    "certifications_recommendation": "Pre-placement preparation, On-campus hiring, off-campus referrals"
                }
            ]
        recs = [
            "Maintain a cumulative CGPA >= 8.0 to clear shortlisting cutoffs for top product companies.",
            "Solve 1-2 algorithmic problems daily on platforms like LeetCode or GeeksforGeeks.",
            "Build at least 2 comprehensive, deployed projects showcasing system scalability and clean code architecture.",
            "Participate actively in technical hackathons (Smart India Hackathon, MLH) and open-source contribution drives."
        ]

    return {
        "student_profile": {
            "stream": req.stream,
            "exam": req.exam,
            "rank": req.rank,
            "branch": req.branch,
            "interest": req.interest,
            "career_goal": req.career_goal
        },
        "rationale": rationale,
        "four_year_roadmap": steps,
        "key_recommendations": recs
    }
