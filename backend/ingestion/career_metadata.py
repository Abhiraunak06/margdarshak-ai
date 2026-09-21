"""
Structured Career Guidance Knowledge Base across all 4 major academic streams:
1. PCM: Engineering, Computer Science, AI/ML, VLSI, Robotics, Aerospace, EV, Civil, Chemical, Architecture, Defence.
2. PCB: Clinical Medicine (MBBS), Dental (BDS), AYUSH (BAMS/BHMS), Veterinary (BVSc), Pharmacy, Physiotherapy, Biotechnology, Nursing.
3. Commerce: Chartered Accountancy (CA New Scheme), Company Secretary (CS), Cost Management (CMA), Investment Banking/CFA, Commercial Banking (RBI/SBI), Business Analytics.
4. Arts / Humanities: Civil Services (UPSC), Corporate & Litigation Law, Clinical Psychology, Journalism & Mass Comm, Public Policy & Economics, Academia & Research.
"""

CAREER_PATHS = [
    # =========================================================================
    # PCM TRACKS
    # =========================================================================
    {
        "title": "Software Engineering & Full Stack Development",
        "slug": "software-engineering",
        "stream": "PCM",
        "domain": "Software & IT",
        "description": "Designing, architecting, and building scalable web, mobile, and distributed systems. Software engineers form the core of global tech products and IT enterprises.",
        "required_skills": "Data Structures & Algorithms, Java/C++/Python, JavaScript/TypeScript, React/Vue, Node.js/Go, SQL & NoSQL, Docker, Git, System Design",
        "recommended_degrees": "B.Tech Computer Science and Engineering, B.Tech Information Technology, Integrated M.Tech CSE",
        "relevant_branches": "Computer Science and Engineering, Information Technology, Software Engineering, Mathematics & Computing",
        "entrance_exams": "JEE Main, JEE Advanced, WBJEE, BITSAT, COMEDK",
        "average_starting_salary_lpa": 12.5,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Master Programming Fundamentals", "actions": "Learn C++ or Java; master OOP concepts; solve 150+ LeetCode problems on Arrays, Strings, Hashing, and Recursion."},
            {"year": "Year 2", "goal": "Advanced DSA & Web Development", "actions": "Master Trees, Graphs, Dynamic Programming. Build full-stack projects using React, Node.js, and PostgreSQL. Participate in hackathons."},
            {"year": "Year 3", "goal": "System Design, DevOps & Internships", "actions": "Study OS, DBMS, Computer Networks, and Low-Level Design (LLD). Containerize apps with Docker. Apply for summer internships at product companies."},
            {"year": "Year 4", "goal": "Pre-Placement Preparation & Offers", "actions": "High-level system design (microservices, caching, rate limiting), mock interviews, and final placement drives."}
        ]
    },
    {
        "title": "Artificial Intelligence & Machine Learning",
        "slug": "ai-ml-engineering",
        "stream": "PCM",
        "domain": "AI & Data",
        "description": "Creating intelligent algorithms, deep learning models, LLMs, and computer vision systems that solve complex perceptual and decision-making problems.",
        "required_skills": "Linear Algebra, Multivariable Calculus, Probability & Statistics, Python, PyTorch, TensorFlow, Hugging Face, MLOps, LangChain, Vector Databases",
        "recommended_degrees": "B.Tech AI & Data Science, B.Tech CSE (AI Specialization), B.Tech Mathematics & Computing",
        "relevant_branches": "Artificial Intelligence and Data Science, Computer Science and Engineering, Mathematics and Computing, Data Engineering",
        "entrance_exams": "JEE Main, JEE Advanced, WBJEE, BITSAT",
        "average_starting_salary_lpa": 14.5,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Math Foundations & Python Mastery", "actions": "Rigorous Linear Algebra, Matrix operations, Probability, and Python (NumPy, Pandas, Matplotlib)."},
            {"year": "Year 2", "goal": "Classical ML & Deep Learning", "actions": "Supervised/unsupervised ML using Scikit-Learn. Transition to Neural Networks and PyTorch. Complete Kaggle competitions."},
            {"year": "Year 3", "goal": "LLMs, Transformers & Generative AI", "actions": "Fine-tuning transformer models, working with Hugging Face, building RAG pipelines, deploying models with FastAPI & Docker."},
            {"year": "Year 4", "goal": "Research Paper / Industrial AI Systems", "actions": "Publish research or build production-grade MLOps pipelines (MLflow, Triton). Target AI research labs and top product tech teams."}
        ]
    },
    {
        "title": "VLSI & Semiconductor Chip Design",
        "slug": "vlsi-semiconductor",
        "stream": "PCM",
        "domain": "Hardware & Electronics",
        "description": "Architecting microchips, ASICs, SoCs, and FPGA systems powering mobile devices, data centers, automotive computing, and AI hardware accelerators.",
        "required_skills": "Digital Electronics, Verilog / SystemVerilog, FPGA Prototyping, Computer Architecture, CMOS Design, STA (Static Timing Analysis), Cadence/Synopsys EDA Tools",
        "recommended_degrees": "B.Tech Electronics & Communication, B.Tech Electrical Engineering, Dual Degree VLSI",
        "relevant_branches": "Electronics and Communication Engineering, Electrical Engineering, VLSI Design, Microelectronics",
        "entrance_exams": "JEE Main, JEE Advanced, WBJEE, GATE (for M.Tech)",
        "average_starting_salary_lpa": 14.0,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Basic Circuits & Logic Design", "actions": "Excel in Network Analysis, Boolean Algebra, Logic Gates, and C programming."},
            {"year": "Year 2", "goal": "HDL & Digital System Design", "actions": "Write synthesizable Verilog; simulate on ModelSim; learn FSM design and RISC architecture basics."},
            {"year": "Year 3", "goal": "FPGA Implementation & ASIC Flow", "actions": "Synthesize on Xilinx Vivado / FPGA boards. Learn SystemVerilog and Universal Verification Methodology (UVM). Target silicon internships."},
            {"year": "Year 4", "goal": "Synthesis, Physical Design & Placements", "actions": "Static Timing Analysis, Clock Tree Synthesis, RTL design interview prep. Target Nvidia, Qualcomm, Intel, TI, AMD."}
        ]
    },
    {
        "title": "Robotics & Autonomous Systems",
        "slug": "robotics-autonomous-systems",
        "stream": "PCM",
        "domain": "Interdisciplinary",
        "description": "Integrating mechanical kinematics, embedded systems, computer vision, and control theory to create autonomous robots, drones, and automated manufacturing systems.",
        "required_skills": "ROS 2 (Robot Operating System), C++, Python, Control Systems, Kinematics, OpenCV, Sensor Fusion (LiDAR, IMU), Embedded Linux",
        "recommended_degrees": "B.Tech Mechatronics, B.Tech Mechanical Engineering, B.Tech ECE, B.Tech Electrical",
        "relevant_branches": "Mechanical Engineering, Mechatronics, Electronics and Communication Engineering, Electrical Engineering",
        "entrance_exams": "JEE Main, JEE Advanced, State CETs",
        "average_starting_salary_lpa": 11.0,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "CAD Modelling & Microcontrollers", "actions": "3D CAD in SolidWorks/Fusion 360, Arduino/ESP32 interfacing, C++ programming."},
            {"year": "Year 2", "goal": "Actuators, Sensors & Motor Drives", "actions": "Kinematics, PID controllers, sensor interfacing, PCB design basics in KiCad."},
            {"year": "Year 3", "goal": "ROS, Simulation & Computer Vision", "actions": "ROS 2, Gazebo simulation, SLAM (Simultaneous Localization and Mapping), OpenCV integration on Raspberry Pi / Jetson."},
            {"year": "Year 4", "goal": "Autonomous Capstone & EV/Robotics Hiring", "actions": "Build an autonomous ground vehicle or drone; interview at EV makers (Tesla, Ather, Ola Electric) and industrial automation firms."}
        ]
    },
    {
        "title": "Aerospace & Defense Technologies",
        "slug": "aerospace-engineering",
        "stream": "PCM",
        "domain": "Core Engineering",
        "description": "Designing next-generation aircraft, satellites, launch vehicles, and propulsion systems for defense and commercial space exploration.",
        "required_skills": "Aerodynamics, Propulsion Systems, Orbital Mechanics, CFD (OpenFOAM/Fluent), Flight Dynamics, MATLAB, Space Mission Design",
        "recommended_degrees": "B.Tech Aerospace Engineering, B.Tech Aeronautical Engineering",
        "relevant_branches": "Aerospace Engineering, Aeronautical Engineering, Mechanical Engineering",
        "entrance_exams": "JEE Advanced, JEE Main, IIST Admission",
        "average_starting_salary_lpa": 10.5,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Foundations in Physics & Calculus", "actions": "Rigorous mechanics, vector calculus, basic aerodynamics principles."},
            {"year": "Year 2", "goal": "Fluid Dynamics & Compressible Flow", "actions": "Shockwaves, airfoil design, aircraft structures and materials."},
            {"year": "Year 3", "goal": "CFD & Rocket Propulsion", "actions": "Nozzle simulations, jet engines, orbital mechanics; participate in cansat/rocketry competitions."},
            {"year": "Year 4", "goal": "Capstone & Space/Defense Careers", "actions": "ISRO recruitment, DRDO, private space-tech startups (Skyroot, Agnikul), Airbus, Boeing."}
        ]
    },
    {
        "title": "Architecture & Sustainable Urban Planning",
        "slug": "architecture-urban-planning",
        "stream": "PCM",
        "domain": "Design & Built Environment",
        "description": "Designing bioclimatic buildings, smart city infrastructure, ecological landscapes, and heritage conservation frameworks balancing aesthetics and structural engineering.",
        "required_skills": "Architectural Drawing, AutoCAD, Revit (BIM), Rhino & Grasshopper, Climate Responsive Design, Building Bye-laws, Lumion/V-Ray 3D Rendering",
        "recommended_degrees": "Bachelor of Architecture (B.Arch - 5 Years)",
        "relevant_branches": "Architecture, Urban Planning, Landscape Design",
        "entrance_exams": "JEE Main Paper 2A (B.Arch), NATA (National Aptitude Test in Architecture)",
        "average_starting_salary_lpa": 6.5,
        "growth_outlook": "Moderate to High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Basic Design & Visual Arts", "actions": "Master freehand architectural sketching, orthographic projections, scale drawing, and 3D physical model making."},
            {"year": "Year 2", "goal": "Building Materials & Digital Drafting", "actions": "Study masonry, timber, concrete detailing. Master AutoCAD and 3D modeling in SketchUp/Revit."},
            {"year": "Year 3", "goal": "Structural Systems & Environmental Science", "actions": "Passive solar design, acoustic design, HVAC integration, parametric modeling using Rhino Grasshopper."},
            {"year": "Year 4", "goal": "Practical Training (6-Month Internship)", "actions": "Mandatory full-time architectural apprenticeship at registered Council of Architecture (CoA) firms."},
            {"year": "Year 5", "goal": "Thesis Project & Professional Practice", "actions": "Complete comprehensive design thesis; CoA registration; apply to top architectural consultancies."}
        ]
    },

    # =========================================================================
    # PCB TRACKS
    # =========================================================================
    {
        "title": "Clinical Medicine & Surgery (MBBS -> MD/MS)",
        "slug": "mbbs-clinical-medicine",
        "stream": "PCB",
        "domain": "Medical Sciences",
        "description": "Diagnosing pathologies, performing surgical procedures, administering patient therapeutic interventions, and leading healthcare teams in clinical environments.",
        "required_skills": "Clinical Anatomy, Physiology, Pathology, Pharmacology, Internal Medicine, General Surgery, Diagnostics, Patient Communication, Critical Care",
        "recommended_degrees": "Bachelor of Medicine and Bachelor of Surgery (MBBS - 5.5 Years)",
        "relevant_branches": "Medicine, Surgery, Pediatrics, Cardiology, Radiology, Orthopedics",
        "entrance_exams": "NEET-UG",
        "average_starting_salary_lpa": 12.0,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1-2 (Pre & Para Clinical)", "goal": "Master Anatomy, Biochemistry & Pathology", "actions": "Comprehensive cadaveric dissection, histological studies, systemic pathology, microbiology, and pharmacology mechanisms."},
            {"year": "Year 3-4 (Clinical Postings)", "goal": "Bedside Clinical Examination & Ward Rounds", "actions": "Daily hospital ward postings in Internal Medicine, General Surgery, Obstetrics & Gynecology, Pediatrics, and Ophthalmology."},
            {"year": "Year 5 (Final Professional)", "goal": "Final Clinical Exams & High-Stakes Patient Management", "actions": "Clear final professional MBBS exams; clinical differential diagnosis under senior consultant supervision."},
            {"year": "Internship Year", "goal": "Compulsory Rotating Medical Internship (CRMI)", "actions": "12-month hands-on emergency, ICU, surgery, and rural primary health centre (PHC) postings; NEET-PG / NExT examination preparation."}
        ]
    },
    {
        "title": "Dental Surgery & Orthodontics (BDS -> MDS)",
        "slug": "dental-surgery-bds",
        "stream": "PCB",
        "domain": "Oral Healthcare",
        "description": "Diagnosing oral pathologies, performing endodontic root canal treatments, maxillofacial trauma surgeries, cosmetic prosthodontics, and orthodontic corrections.",
        "required_skills": "Oral Anatomy, Histopathology, Conservative Dentistry, Prosthodontics, Periodontics, Maxillofacial Surgery, Orthodontics, Radiography",
        "recommended_degrees": "Bachelor of Dental Surgery (BDS - 5 Years)",
        "relevant_branches": "Oral & Maxillofacial Surgery, Orthodontics, Conservative Dentistry & Endodontics, Prosthodontics",
        "entrance_exams": "NEET-UG",
        "average_starting_salary_lpa": 7.5,
        "growth_outlook": "Moderate to High",
        "roadmap_steps": [
            {"year": "Year 1-2", "goal": "Pre-Clinical Tooth Carving & Materials", "actions": "Wax carving of dental morphology, dental materials chemistry, general anatomy and physiology."},
            {"year": "Year 3-4", "goal": "Clinical Patient Treatments & Extractions", "actions": "Chairside clinical treatments: tooth restorations, extractions, scaling, complete and removable partial dentures."},
            {"year": "Year 5 (Internship)", "goal": "Full-Time Rotary Internship", "actions": "Rotations across Oral Surgery, Endodontics, and Orthodontics; prepare for NEET-MDS or establish private dental clinic."}
        ]
    },
    {
        "title": "Veterinary Medicine & Surgery (BVSc & AH)",
        "slug": "veterinary-medicine-bvsc",
        "stream": "PCB",
        "domain": "Animal Health & Livestock",
        "description": "Treating companion animals, horses, livestock, and wildlife against infectious diseases, performing veterinary surgery, and ensuring food security and zoonotic disease control.",
        "required_skills": "Veterinary Anatomy, Animal Nutrition, Veterinary Pharmacology, Clinical Pathology, Animal Genetics, Surgery & Radiology, Zoonoses Prevention",
        "recommended_degrees": "Bachelor of Veterinary Science and Animal Husbandry (B.V.Sc & A.H. - 5.5 Years)",
        "relevant_branches": "Veterinary Clinical Medicine, Surgery, Animal Reproduction, Wildlife Conservation",
        "entrance_exams": "NEET-UG (for 15% VCI All-India Quota), State Veterinary Entrances",
        "average_starting_salary_lpa": 8.0,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Year 1-2", "goal": "Veterinary Gross Anatomy & Animal Genetics", "actions": "Study comparative anatomy of cattle, canines, and equines; livestock management and biochemistry."},
            {"year": "Year 3-4", "goal": "Clinical Diagnostics, Pharmacology & Surgery", "actions": "Clinical veterinary pathology, animal surgery, diagnostic ultrasound/X-ray, infectious zoonotic diseases."},
            {"year": "Internship Year", "goal": "Clinical Veterinary Hospital Posting", "actions": "6-month clinical veterinary hospital training + 6-month farm and zoo ambulatory postings; VCI licensing."}
        ]
    },
    {
        "title": "Pharmaceutical Sciences & Drug Development",
        "slug": "pharmaceutical-sciences-bpharm",
        "stream": "PCB",
        "domain": "Pharmaceuticals & Biotechnology",
        "description": "Formulating pharmaceutical drugs, conducting pharmacological research, clinical trials, regulatory affairs, and industrial quality control in global biopharma corporations.",
        "required_skills": "Medicinal Chemistry, Pharmacology, Pharmaceutics, Pharmacognosy, HPLC/GC-MS Chromatography, Clinical Data Management, GMP Compliance",
        "recommended_degrees": "Bachelor of Pharmacy (B.Pharm - 4 Years), Pharm.D (6 Years)",
        "relevant_branches": "Pharmaceutics, Pharmacology, Pharmaceutical Chemistry, Regulatory Affairs",
        "entrance_exams": "State CETs (WBJEE Pharmacy, MHT CET), NEET-UG (some states), CUET-UG",
        "average_starting_salary_lpa": 6.5,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Organic Chemistry & Human Anatomy", "actions": "Inorganic/organic chemistry, human anatomy, pharmaceutical calculations, and computer applications."},
            {"year": "Year 2", "goal": "Physical Pharmaceutics & Microbiology", "actions": "Drug formulation principles, dosage forms (tablets, injectables), sterile manufacturing, and pharmacognosy."},
            {"year": "Year 3", "goal": "Pharmacology & Instrumental Analysis", "actions": "Mechanism of drug action on organ systems; hands-on HPLC, UV-Vis spectroscopy, and drug assay validation."},
            {"year": "Year 4", "goal": "Industrial Training & Placement", "actions": "Mandatory industrial internship in USFDA-approved plant; GPAT exam preparation for M.Pharm or biopharma campus hiring."}
        ]
    },
    {
        "title": "Biotechnology & Genomic Sciences",
        "slug": "biotechnology-genomic-sciences",
        "stream": "PCB",
        "domain": "Life Sciences & Genomics",
        "description": "Engineering recombinant DNA, CRISPR gene editing, bioinformatics pipelines, stem cell therapies, and bioprocess fermentation for medicine and agriculture.",
        "required_skills": "Molecular Biology, Recombinant DNA Technology, CRISPR-Cas9, Python for Bioinformatics, Next-Generation Sequencing (NGS), Fermentation, Cell Culture",
        "recommended_degrees": "B.Tech Biotechnology, B.Sc (Hons) Biotechnology / Genetics",
        "relevant_branches": "Biotechnology, Bioinformatics, Biomedical Engineering, Genetic Engineering",
        "entrance_exams": "JEE Main / State CETs (for B.Tech), CUET-UG (for B.Sc/Integrated M.Sc)",
        "average_starting_salary_lpa": 8.5,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Cell Biology & Biochemistry", "actions": "Enzymology, metabolic pathways, cell physiology, and introductory biostatistics."},
            {"year": "Year 2", "goal": "Molecular Genetics & Recombinant DNA", "actions": "DNA extraction, PCR amplification, gel electrophoresis, plasmid cloning, and Python basics."},
            {"year": "Year 3", "goal": "Bioinformatics & Downstream Processing", "actions": "Genomic sequence alignment (BLAST), protein structural modeling, bioreactor operations, and summer research fellowship (IASc/INSA)."},
            {"year": "Year 4", "goal": "Capstone Research & Biotech Placement", "actions": "Publish research paper in peer-reviewed journal; prepare for GATE Biotechnology / CSIR-NET / global MS-PhD programs."}
        ]
    },

    # =========================================================================
    # COMMERCE TRACKS
    # =========================================================================
    {
        "title": "Chartered Accountancy (ICAI New Scheme 2024)",
        "slug": "chartered-accountancy",
        "stream": "COMMERCE",
        "domain": "Accounting, Audit & Taxation",
        "description": "The premier professional qualification in India for statutory audit, international taxation, forensic accounting, financial reporting, corporate law, and business advisory.",
        "required_skills": "Ind AS / IFRS Financial Reporting, Advanced Auditing Standards, Direct & International Tax, GST, Company Law, Financial Management, Advanced Excel",
        "recommended_degrees": "ICAI CA Professional Qualification (alongside B.Com / B.Com Hons)",
        "relevant_branches": "Auditing, Corporate Taxation, Forensic Accounting, CFO Advisory",
        "entrance_exams": "CA Foundation (ICAI Entry Examination)",
        "average_starting_salary_lpa": 12.0,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Stage 1 (Class 12 to 6 Months)", "goal": "CA Foundation Examination", "actions": "Register with ICAI; clear 4 papers: Accounting, Business Laws, Quantitative Aptitude, Business Economics (requires 50% aggregate and 40% per paper)."},
            {"year": "Stage 2 (8 Months Study)", "goal": "CA Intermediate (Group 1 & Group 2)", "actions": "Master Advanced Accounting, Corporate Laws, Taxation (Direct & Indirect), Costing, Auditing, and Financial Management. Clear both groups."},
            {"year": "Stage 3 (2 Years Full-Time)", "goal": "Mandatory Articleship & ICITSS", "actions": "Complete 2 years of practical training under a practicing Chartered Accountant firm; complete Information Technology (ICITSS) and soft skills training."},
            {"year": "Stage 4 (Final Milestone)", "goal": "CA Final Examination & ICAI Membership", "actions": "Clear CA Final 6 papers including Financial Reporting, Strategic Financial Management, and Elective; become an Associate Chartered Accountant (ACA)."}
        ]
    },
    {
        "title": "Company Secretary & Corporate Governance (ICSI)",
        "slug": "company-secretary",
        "stream": "COMMERCE",
        "domain": "Corporate Law & Compliance",
        "description": "Chief compliance advisors to corporate boards of directors ensuring full compliance with SEBI LODR, Companies Act 2013, insider trading norms, and board secretarial governance.",
        "required_skills": "Companies Act 2013, SEBI Regulations, Securities Law, Economic & Commercial Laws, Board Drafting, Corporate Restructuring, Due Diligence",
        "recommended_degrees": "ICSI CS Professional Qualification (alongside B.Com / B.A. LL.B.)",
        "relevant_branches": "Corporate Governance, Legal Compliance, Secretarial Audit",
        "entrance_exams": "CSEET (Company Secretary Executive Entrance Test)",
        "average_starting_salary_lpa": 9.5,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Stage 1", "goal": "Clear CSEET Entrance Examination", "actions": "Pass Business Communication, Legal Aptitude, Economic & Business Environment, and Current Affairs test."},
            {"year": "Stage 2", "goal": "CS Executive Program", "actions": "Master 7 comprehensive law papers covering Company Law, Secretarial Practice, Corporate Restructuring, Tax Laws, and Capital Markets."},
            {"year": "Stage 3", "goal": "Practical Training (EDP - 21 Months)", "actions": "Complete Executive Development Programme (EDP) and 21-month practical training in listed corporate houses or practicing CS firms."},
            {"year": "Stage 4", "goal": "CS Professional & Membership", "actions": "Clear CS Professional papers; obtain ICSI membership and practice as Company Secretary / Board Advisor."}
        ]
    },
    {
        "title": "Cost & Management Accounting (ICMAI)",
        "slug": "cost-management-accounting",
        "stream": "COMMERCE",
        "domain": "Costing & Operational Strategy",
        "description": "Optimizing industrial production costs, managing corporate supply chain finance, conducting statutory cost audits, and strategic operational pricing in manufacturing and services.",
        "required_skills": "Cost Accounting Standards (CAS), Standard Costing, Marginal Costing, Supply Chain Analytics, Direct & Indirect Tax, Enterprise Performance Management",
        "recommended_degrees": "ICMAI CMA Professional Qualification",
        "relevant_branches": "Cost Audit, Industrial Finance, Management Accounting",
        "entrance_exams": "CMA Foundation",
        "average_starting_salary_lpa": 9.0,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Stage 1", "goal": "CMA Foundation Examination", "actions": "Clear Fundamentals of Business Laws, Financial Accounting, Business Math & Statistics, and Economics."},
            {"year": "Stage 2", "goal": "CMA Intermediate Examination", "actions": "Study Cost Accounting, Corporate Accounting, Direct/Indirect Taxation, Operations Management & Strategic Management."},
            {"year": "Stage 3", "goal": "Mandatory 15-Month Practical Training", "actions": "Hands-on costing and financial analysis internship in PSUs (ONGC, BHEL, IOCL) or manufacturing corporations."},
            {"year": "Stage 4", "goal": "CMA Final & Cost Auditor Certification", "actions": "Clear Strategic Financial Management, Cost & Management Audit, and Corporate Laws; join as Cost & Management Accountant."}
        ]
    },
    {
        "title": "Investment Banking, Equity Research & CFA",
        "slug": "investment-banking-cfa",
        "stream": "COMMERCE",
        "domain": "High Finance & Capital Markets",
        "description": "Advising corporations on multi-billion dollar mergers & acquisitions (M&A), initial public offerings (IPOs), discounted cash flow valuation modeling, and equity research.",
        "required_skills": "Discounted Cash Flow (DCF) Valuation, LBO Modeling, Financial Statement Analysis, Bloomberg Terminal, M&A Deal Structuring, Pitchbooks, Python for Finance",
        "recommended_degrees": "B.Com (Hons) / BMS / BBA (Finance) -> MBA Finance (IIMs) / CFA Charter",
        "relevant_branches": "Investment Banking, Private Equity, Equity Research, Portfolio Management",
        "entrance_exams": "CUET-UG (for SRCC / SSCBS), IPMAT (for IIMs), CAT (for MBA), CFA Level I",
        "average_starting_salary_lpa": 16.0,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Financial Accounting & Advanced Excel", "actions": "Master 3-statement financial modeling in Excel, macroeconomic cycles, and stock market fundamentals."},
            {"year": "Year 2", "goal": "Valuation Modeling & Corporate Finance", "actions": "Build DCF, Precedent Transactions, and Comparable Company Analysis (Trading Comps) for Indian and global equities."},
            {"year": "Year 3", "goal": "Investment Banking Summer Internship", "actions": "Summer analyst internship at bulge-bracket / boutique investment banks; prepare for CFA Level I examination."},
            {"year": "Year 4", "goal": "Full-Time Placement & CFA Cleared", "actions": "Clear CFA Level 1; interview for Investment Banking Analyst or Private Equity Associate roles."}
        ]
    },
    {
        "title": "Business Analytics & Financial Technology",
        "slug": "business-analytics-fintech",
        "stream": "COMMERCE",
        "domain": "Fintech & Analytics",
        "description": "Using data analytics, statistical modeling, algorithmic payment gateways, and predictive consumer behavior modeling to drive commercial business decisions.",
        "required_skills": "SQL, Python (Pandas/Statsmodels), Power BI / Tableau, Financial Econometrics, Machine Learning for Credit Risk, A/B Testing, Product Analytics",
        "recommended_degrees": "B.Com / BBA Analytics, B.Sc Economics / Data Analytics, BMS",
        "relevant_branches": "Business Analytics, Financial Engineering, Risk Analytics",
        "entrance_exams": "CUET-UG, IPMAT, NPAT",
        "average_starting_salary_lpa": 10.5,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Business Statistics & SQL Mastery", "actions": "Business statistics, probability distributions, relational database querying with PostgreSQL."},
            {"year": "Year 2", "goal": "Python Data Analysis & BI Dashboards", "actions": "Build interactive executive dashboards in Power BI; exploratory data analysis on consumer finance data with Python."},
            {"year": "Year 3", "goal": "Predictive Modeling & Credit Risk Analytics", "actions": "Logistic regression, credit scoring models, fraud detection algorithms; summer analyst internship at fintech unicorn."},
            {"year": "Year 4", "goal": "Product Analytics & Campus Placements", "actions": "Interview for Business Analyst / Data Consultant roles at McKinsey, BCG, Bain, American Express, or top fintech firms."}
        ]
    },

    # =========================================================================
    # ARTS / HUMANITIES TRACKS
    # =========================================================================
    {
        "title": "Civil Services & Public Administration (UPSC CSE)",
        "slug": "civil-services-upsc",
        "stream": "ARTS",
        "domain": "Government & Administration",
        "description": "Leading district governance, implementing public welfare policies, maintaining law & order, and shaping bilateral national policies as IAS, IPS, and IFS officers.",
        "required_skills": "Administrative Leadership, Public Policy Analysis, Constitutional Law, Crisis Management, Critical Analysis, Essay & Descriptive Writing",
        "recommended_degrees": "B.A. (Hons) Political Science / History / Economics / Sociology",
        "relevant_branches": "Public Policy, International Relations, Political Science, Economics",
        "entrance_exams": "UPSC Civil Services Examination (Prelims, Mains, Interview)",
        "average_starting_salary_lpa": 10.0,
        "growth_outlook": "Prestigious / High Impact",
        "roadmap_steps": [
            {"year": "College Year 1", "goal": "NCERT Foundations & Newspaper Habit", "actions": "Read Class 6-12 NCERTs for History, Geography, Polity, Economics. Develop daily 1.5-hour reading habit of The Hindu."},
            {"year": "College Year 2", "goal": "Standard Reference Texts & College Excellence", "actions": "M. Laxmikanth (Polity), Spectrum (Modern India), Nitin Singhania (Art & Culture). Maintain >= 70% in Graduation."},
            {"year": "College Year 3", "goal": "Optional Subject Mastery & Answer Writing", "actions": "Complete optional subject syllabus (e.g. Political Science / History / Sociology); join GS answer writing evaluation program."},
            {"year": "Final Year / Attempt", "goal": "Prelims Mocks & First UPSC Attempt", "actions": "Solve 50+ full-length prelims mocks; revise economic survey and current affairs; appear in UPSC CSE upon reaching 21 years."}
        ]
    },
    {
        "title": "Corporate Law & Litigation (CLAT -> NLU)",
        "slug": "corporate-law-litigation",
        "stream": "ARTS",
        "domain": "Law & Legal Services",
        "description": "Drafting commercial contracts, representing clients before High Courts & Supreme Court, advising on corporate governance, intellectual property, and international arbitration.",
        "required_skills": "Constitutional Law, Contracts & Commercial Law, Legal Drafting & Pleading, Case Law Research (SCC Online, Manupatra), Moot Court Advocacy, Negotiation",
        "recommended_degrees": "5-Year Integrated B.A. LL.B. (Hons) / B.B.A. LL.B. (Hons)",
        "relevant_branches": "Corporate Law, Criminal Litigation, Intellectual Property Rights, Constitutional Law",
        "entrance_exams": "CLAT (Common Law Admission Test), AILET (NLU Delhi)",
        "average_starting_salary_lpa": 15.0,
        "growth_outlook": "Very High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Legal Methods & Law of Torts/Contracts", "actions": "Learn case brief analysis, citation standards, participate in intra-university moot court competitions."},
            {"year": "Year 2", "goal": "Constitutional Law & Criminal Law", "actions": "Study IPC, CrPC, evidence law; intern under trial court / High Court advocates during winter break."},
            {"year": "Year 3", "goal": "Corporate & Commercial Laws", "actions": "Companies Act, insolvency & bankruptcy code (IBC), competition law; intern with judicial clerks or boutique law firms."},
            {"year": "Year 4", "goal": "Tier-1 Law Firm Internships", "actions": "Assessment internships at premier law firms (Shardul Amarchand Mangaldas, AZB, Cyril Amarchand Mangaldas, Trilegal, Khaitan)."},
            {"year": "Year 5", "goal": "Pre-Placement Offers (PPO) & Bar Enrollment", "actions": "Secure Day Zero campus law firm offer; enroll with Bar Council of India to practice in Indian courts."}
        ]
    },
    {
        "title": "Clinical Psychology & Mental Health Counseling",
        "slug": "clinical-psychology",
        "stream": "ARTS",
        "domain": "Mental Healthcare",
        "description": "Administering clinical psychometric assessments, diagnosing cognitive and emotional disorders, providing evidence-based psychotherapy, and conducting neuropsychological research.",
        "required_skills": "Psychological Assessment Tools (WAIS, Rorschach), Cognitive Behavioral Therapy (CBT), Psychopathology Diagnosis (DSM-5), Neuropsychology, Empathy, Research Statistics",
        "recommended_degrees": "B.A./B.Sc Psychology -> M.A./M.Sc Clinical Psychology -> M.Phil in Clinical Psychology (RCI Licensed)",
        "relevant_branches": "Clinical Psychology, Neuropsychology, Counseling Psychology, Child Development",
        "entrance_exams": "CUET-UG (for top DU colleges), CUET-PG / NIMHANS Entrance (for Master's/M.Phil)",
        "average_starting_salary_lpa": 7.0,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Undergrad Year 1-2", "goal": "Foundations of Psychology & Statistics", "actions": "Cognitive psychology, biopsychology, developmental psychology, SPSS statistical data analysis."},
            {"year": "Undergrad Year 3", "goal": "Psychopathology & Clinical Observation", "actions": "Study DSM-5 diagnostic criteria; complete clinical observer internship at psychiatric hospital or NGO."},
            {"year": "Postgrad (M.A./M.Sc)", "goal": "Advanced Psychotherapy & Psychometry", "actions": "Administer standardized intelligence and personality tests; conduct master's research thesis on mental health."},
            {"year": "RCI M.Phil / Psy.D", "goal": "Hospital Residency & RCI Clinical License", "actions": "2-year hospital clinical psychology residency (NIMHANS, CIP Ranchi, or IHBAS); obtain RCI registration as Licensed Clinical Psychologist."}
        ]
    },
    {
        "title": "Journalism, Mass Communication & Digital Media",
        "slug": "journalism-mass-communication",
        "stream": "ARTS",
        "domain": "Media & Communication",
        "description": "Investigative reporting, broadcast television journalism, digital video documentary production, podcasting, and multi-platform editorial storytelling.",
        "required_skills": "Investigative Reporting, News Writing, Video Editing (Premiere Pro), Camera Handling, Fact-Checking, Social Media Strategy, Podcast Production",
        "recommended_degrees": "B.A. (Hons) Journalism, Bachelor of Mass Media (BMM), Post-Graduate Diploma in Journalism (IIMC)",
        "relevant_branches": "Broadcast Journalism, Print & Digital Media, Photojournalism, Documentary Filmmaking",
        "entrance_exams": "CUET-UG, IIMC National Entrance Examination",
        "average_starting_salary_lpa": 6.0,
        "growth_outlook": "Moderate to High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "News Sense & Print Reporting", "actions": "Master headline writing, 5 Ws and 1 H reporting structure, feature writing for campus newspaper."},
            {"year": "Year 2", "goal": "Broadcast Production & Digital Tools", "actions": "Camera framing, audio recording, non-linear video editing on Adobe Premiere Pro, run multimedia blog."},
            {"year": "Year 3", "goal": "Newsroom Internship & Portfolio", "actions": "Summer editorial internship at leading news agency (PTI, ANI, The Indian Express, NDTV); build portfolio of published bylines."},
            {"year": "Year 4", "goal": "Specialized Reporting & Newsroom Placement", "actions": "Specialize in Political, Business, or Climate reporting; join national digital/broadcast news organization."}
        ]
    },
    {
        "title": "Economics, Public Policy & International Think Tanks",
        "slug": "economics-public-policy",
        "stream": "ARTS",
        "domain": "Economics & Public Policy",
        "description": "Analyzing macroeconomic trends, conducting randomized controlled trials (RCTs), evaluating social welfare schemes, and advising government bodies and multilateral organizations (World Bank, UN).",
        "required_skills": "Microeconomics, Macroeconomics, Econometrics (STATA / R), Policy Evaluation, Cost-Benefit Analysis, Data Visualization, Policy Memo Writing",
        "recommended_degrees": "B.A. (Hons) Economics -> Master's in Economics (DSE, ISI, JNU) / Master in Public Policy (MPP)",
        "relevant_branches": "Development Economics, Applied Econometrics, International Trade, Public Policy",
        "entrance_exams": "CUET-UG (for St. Stephen's, SRCC, Hindu, LSR), CUET-PG / IIT JAM Economics",
        "average_starting_salary_lpa": 11.0,
        "growth_outlook": "High",
        "roadmap_steps": [
            {"year": "Year 1", "goal": "Mathematical Methods for Economics", "actions": "Advanced calculus, linear algebra, microeconomic consumer and producer theory."},
            {"year": "Year 2", "goal": "Macroeconomic Modeling & Econometrics", "actions": "IS-LM and dynamic aggregate models; statistical hypothesis testing, regression analysis using R and STATA."},
            {"year": "Year 3", "goal": "Policy Research Fellowship", "actions": "Summer research analyst at policy think tanks (NITI Aayog, CPR, ICRIER, J-PAL South Asia); publish empirical policy memo."},
            {"year": "Year 4 / Postgrad", "goal": "Master's Degree & Economic Consulting", "actions": "Master's from Delhi School of Economics (DSE) / ISI; join as Economic Consultant / Policy Associate."}
        ]
    }
]
