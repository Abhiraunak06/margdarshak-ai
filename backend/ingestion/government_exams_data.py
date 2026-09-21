import json

GOVERNMENT_EXAMS_DATA = [
    {
        "title": "UPSC Civil Services Examination (CSE)",
        "code": "UPSC_CSE",
        "conducting_body": "Union Public Service Commission (UPSC)",
        "sector": "Civil Services & Executive Administration",
        "eligibility_education": "Any Bachelor's Degree in any discipline from a recognized University",
        "min_age": 21,
        "max_age": 32,
        "salary_scale": "Level 10 in Pay Matrix (Entry Basic Rs. 56,100 + DA + HRA up to Rs. 2,50,000 for Cabinet Secretary)",
        "official_website": "https://upsc.gov.in",
        "application_window": "February - March annually (Prelims in May/June)",
        "career_roles": "Indian Administrative Service (IAS), Indian Police Service (IPS), Indian Foreign Service (IFS), Indian Revenue Service (IRS), Indian Audit and Accounts Service (IA&AS)",
        "selection_stages": json.dumps([
            {"stage": "Stage 1: Preliminary Examination (Objective)", "details": "Paper I: General Studies (100 questions, 200 marks, merit) + Paper II: CSAT (80 questions, 200 marks, qualifying at 33%)."},
            {"stage": "Stage 2: Main Examination (Written Descriptive)", "details": "9 Papers: Essay (250 marks), GS I, II, III, IV (250 marks each), 2 Optional Papers (250 marks each) + 2 Qualifying Language Papers."},
            {"stage": "Stage 3: Personality Test / Interview", "details": "275 marks interview evaluating intellectual integrity, critical judgment, social cohesion, and leadership."}
        ]),
        "syllabus_overview": "Ancient, Medieval & Modern Indian History, Art & Culture, Indian & World Geography, Indian Polity & Constitution, Governance, Social Justice, Economy & Sustainable Development, Environment & Ecology, Science & Technology, Internal Security, Disaster Management, and Ethics, Integrity & Aptitude.",
        "preparation_roadmap": json.dumps([
            {"phase": "Foundation (Months 1-4)", "focus": "Complete thorough reading of NCERT textbooks (Classes 6 to 12) for History, Geography, Polity, and Economics. Start daily reading of The Hindu or The Indian Express."},
            {"phase": "Standard Reference & GS (Months 5-8)", "focus": "M. Laxmikanth for Indian Polity, Ramesh Singh/Sanjiv Verma for Economy, Spectrum for Modern India, Shankar IAS for Environment. Select and start Optional Subject."},
            {"phase": "Answer Writing & Optional Completion (Months 9-11)", "focus": "Daily GS answer writing practice (2 questions/day). Finish 100% of Optional syllabus with self-made summary notes and previous 10-year question papers."},
            {"phase": "Prelims Intensive Sprint (Last 3 Months)", "focus": "Solve 50+ full-length mock tests for GS Paper 1 and CSAT. Thoroughly revise Year-long Current Affairs compilations and economic survey."}
        ])
    },
    {
        "title": "SSC Combined Graduate Level (SSC CGL)",
        "code": "SSC_CGL",
        "conducting_body": "Staff Selection Commission (SSC)",
        "sector": "Central Ministries & Attached Subordinate Offices",
        "eligibility_education": "Bachelor's Degree in any discipline from a recognized University",
        "min_age": 18,
        "max_age": 30,
        "salary_scale": "Level 4 to Level 8 (Pay Band Rs. 25,500 to Rs. 1,51,100 depending on post)",
        "official_website": "https://ssc.gov.in",
        "application_window": "June - July annually",
        "career_roles": "Assistant Section Officer (Central Secretariat / MEA / IB), Income Tax Inspector, Central Excise / GST Inspector, Preventive Officer, Enforcement Officer (ED), Sub-Inspector (CBI)",
        "selection_stages": json.dumps([
            {"stage": "Tier 1: Computer Based Examination (Qualifying)", "details": "100 questions (200 marks): General Intelligence & Reasoning (25), General Awareness (25), Quantitative Aptitude (25), English Comprehension (25). Duration 60 mins."},
            {"stage": "Tier 2: Paper 1 (Merit Assessment)", "details": "Section I: Math (30) + Reasoning (30) [180 marks]; Section II: English (45) + GA (25) [210 marks]; Section III: Computer Knowledge (20 questions, qualifying) + Data Entry Speed Test (DEST)."}
        ]),
        "syllabus_overview": "Advanced Mathematics (Trigonometry, Geometry, Algebra, Mensuration, Arithmetic), Verbal & Non-Verbal Reasoning, Static General Knowledge & Current Affairs, English Grammar, Vocabulary, Reading Comprehension, and Computer Basics.",
        "preparation_roadmap": json.dumps([
            {"phase": "Phase 1: Arithmetic & Grammar Mastery", "focus": "Complete core arithmetic, percentage, ratio, speed-time, algebra, and geometry. Solve Kiran SSC Chapterwise Math and Neetu Singh English Vol 1."},
            {"phase": "Phase 2: Reasoning & Static GK", "focus": "Lucent GK for History, Polity, Geography, and General Science. Daily section-wise timed quizzes for Reasoning speed."},
            {"phase": "Phase 3: Tier 2 Mock Drills", "focus": "Solve 40+ full mock tests on Testbook or Oliveboard. Practice daily 15-minute touch typing to exceed 27 WPM for DEST qualification."}
        ])
    },
    {
        "title": "IBPS & SBI Probationary Officer (PO)",
        "code": "IBPS_SBI_PO",
        "conducting_body": "Institute of Banking Personnel Selection (IBPS) & State Bank of India",
        "sector": "Public Sector Commercial Banking & Financial Services",
        "eligibility_education": "Graduation in any discipline with minimum 60% marks (General/OBC)",
        "min_age": 20,
        "max_age": 30,
        "salary_scale": "Basic Pay Rs. 41,960 + 4 advance increments (Gross ~Rs. 65,000 - 72,000/month + leased accommodation)",
        "official_website": "https://ibps.in / https://sbi.co.in",
        "application_window": "August - September annually",
        "career_roles": "Probationary Officer (Scale I) -> Assistant Manager -> Branch Manager -> Chief Manager -> General Manager",
        "selection_stages": json.dumps([
            {"stage": "Prelims (Online Objective)", "details": "100 questions (100 marks, 60 mins sectional timing): English (30), Quantitative Aptitude (35), Reasoning Ability (35)."},
            {"stage": "Mains (Objective + Descriptive)", "details": "155 questions (200 marks, 3 hrs): Reasoning & Computer (45), Data Analysis & Interpretation (35), General/Economy/Banking Awareness (40), English (35) + Descriptive English (Letter & Essay writing, 25 marks)."},
            {"stage": "Group Discussion & Personal Interview", "details": "GD (20 marks) and Interview (30 marks) assessing financial acumen, situation handling, and banking fundamentals."}
        ]),
        "syllabus_overview": "Data Interpretation (Pie charts, Radar, Caselets, Missing DI), High-level Puzzles and Seating Arrangement, Critical Reasoning, Banking Operations, RBI Regulations, Monetary Policy, Financial Awareness, and Business English.",
        "preparation_roadmap": json.dumps([
            {"phase": "Phase 1: Calculation Speed & Concepts", "focus": "Vedic math techniques, square roots, cubes, fractions. Master syllogisms, inequalities, input-output, and blood relations."},
            {"phase": "Phase 2: Complex DI & High-Level Puzzles", "focus": "Daily practice of 4 complex seating arrangement puzzles and 3 data analysis caselets. Regular reading of The Economic Times."},
            {"phase": "Phase 3: Banking Awareness & Mocks", "focus": "Study last 6 months banking affairs, monetary policy, Basel norms, priority sector lending. Daily full-length sectional mocks."}
        ])
    },
    {
        "title": "Combined Defence Services Examination (CDS)",
        "code": "UPSC_CDS",
        "conducting_body": "Union Public Service Commission (UPSC) & Service Selection Board (SSB)",
        "sector": "Indian Armed Forces (Army, Navy, Air Force)",
        "eligibility_education": "Bachelor's Degree for IMA/OTA; Degree in Engineering for Indian Naval Academy; Degree with Physics & Math (or B.E.) for Air Force Academy",
        "min_age": 19,
        "max_age": 25,
        "salary_scale": "Lieutenant / Sub Lieutenant / Flying Officer (Level 10: Rs. 56,100 + Military Service Pay Rs. 15,500/month)",
        "official_website": "https://upsc.gov.in",
        "application_window": "Twice a year (CDS I in Oct/Nov, CDS II in May/June)",
        "career_roles": "Commissioned Officer in Indian Army (IMA Dehradun / OTA Chennai), Indian Navy (INA Ezhimala), Indian Air Force (AFA Dundigal)",
        "selection_stages": json.dumps([
            {"stage": "Written Examination", "details": "For IMA/INA/AFA: English (100 marks), General Knowledge (100 marks), Elementary Mathematics (100 marks). For OTA: English (100 marks) and General Knowledge (100 marks)."},
            {"stage": "5-Day SSB Interview", "details": "Stage 1: OIR Test & PPDT (Screening). Stage 2: Psychological tests (TAT, WAT, SRT, SD), Group Testing Officer (GTO) indoor/outdoor tasks, and Personal Interview."},
            {"stage": "Special Medical Board (SMB)", "details": "Comprehensive military fitness, vision standards, and physical endurance evaluation."}
        ]),
        "syllabus_overview": "English comprehension, spotting errors, sentence rearrangement; Elementary Mathematics up to Class 10 (Arithmetic, Algebra, Trigonometry, Geometry, Mensuration, Statistics); General Knowledge covering Indian History, Geography, Defense, Science, and World Affairs.",
        "preparation_roadmap": json.dumps([
            {"phase": "Phase 1: Written Exam Preparation", "focus": "Complete NCERT Class 9-10 Math; solve RS Aggarwal Quantitative Aptitude. Daily reading of current affairs with specific emphasis on military modernization and international relations."},
            {"phase": "Phase 2: Physical Fitness & Conditioning", "focus": "Daily 5 km running, pull-ups, push-ups, and core fitness. Develop stamina to comfortably clear military endurance norms."},
            {"phase": "Phase 3: SSB Psychological & GTO Preparation", "focus": "Practice TAT story writing on positive resolution; WAT sentence framing reflecting Officer Like Qualities (OLQs); practice public speaking (Lecturette) and group discussion."}
        ])
    },
    {
        "title": "Railway Recruitment Board Non-Technical (RRB NTPC)",
        "code": "RRB_NTPC",
        "conducting_body": "Railway Recruitment Boards (Ministry of Railways)",
        "sector": "Indian Railways Central Operations",
        "eligibility_education": "Any Bachelor's Degree from a recognized University",
        "min_age": 18,
        "max_age": 33,
        "salary_scale": "Level 4 to Level 6 (Gross Rs. 35,000 to Rs. 65,000/month + Railway pass and medical perks)",
        "official_website": "https://rrbcdg.gov.in",
        "application_window": "As announced periodically by Railway Recruitment Control Board",
        "career_roles": "Station Master, Goods Guard / Train Manager, Commercial Apprentice, Senior Clerk cum Typist, Traffic Assistant",
        "selection_stages": json.dumps([
            {"stage": "1st Stage Computer Based Test (CBT 1)", "details": "100 questions (100 marks, 90 mins): General Awareness (40), Mathematics (30), General Intelligence & Reasoning (30). Screening test."},
            {"stage": "2nd Stage Computer Based Test (CBT 2)", "details": "120 questions (120 marks, 90 mins): General Awareness (50), Mathematics (35), General Intelligence & Reasoning (35). Merit determining."},
            {"stage": "Computer Based Aptitude Test (CBAT) / Typing Test", "details": "CBAT specifically for Station Master / Traffic Assistant; Typing Skill Test for Clerical posts."}
        ]),
        "syllabus_overview": "Number System, Decimals, Fractions, LCM/HCF, Ratio and Proportion, Percentages, Mensuration, Time and Work, Simple & Compound Interest, Coding-Decoding, Venn Diagrams, Current Events of National & International Importance, Indian Literature, Monuments and Places of India, General Science (Life Science, Physics, Chemistry up to 10th CBSE).",
        "preparation_roadmap": json.dumps([
            {"phase": "Phase 1: General Science & General Awareness", "focus": "Master Class 9-10 NCERT Science and Lucent General Knowledge. Daily review of railway static facts and Indian Geography."},
            {"phase": "Phase 2: Math & Reasoning Speed Drills", "focus": "Solve previous 10-year RRB NTPC papers. Focus on accuracy to eliminate negative marking (1/3rd penalty)."},
            {"phase": "Phase 3: CBAT Intelligence Battery Test", "focus": "Practice psycho-aptitude test modules (Intelligence Test, Selective Attention Test, Spatial Scanning, Personality Test)."}
        ])
    },
    {
        "title": "UGC National Eligibility Test (UGC-NET / JRF)",
        "code": "UGC_NET",
        "conducting_body": "National Testing Agency (NTA) on behalf of UGC",
        "sector": "Higher Education, University Lectureship & Research",
        "eligibility_education": "Master's Degree or equivalent with at least 55% marks (50% for reserved categories)",
        "min_age": 21,
        "max_age": 30, # For JRF (no upper age limit for Assistant Professor)
        "salary_scale": "Assistant Professor (Academic Level 10: Rs. 57,700 - Rs. 1,82,400) / JRF Fellowship (Rs. 37,000/month + HRA)",
        "official_website": "https://ugcnet.nta.ac.in",
        "application_window": "Twice a year (June & December cycles)",
        "career_roles": "Assistant Professor in Central/State Universities, Junior Research Fellow (JRF), Policy Analyst in think tanks",
        "selection_stages": json.dumps([
            {"stage": "Paper I: General Paper on Teaching & Research Aptitude", "details": "50 objective questions (100 marks, 1 hr): Teaching Aptitude, Research Methodology, Reading Comprehension, Communication, Mathematical Reasoning, Logical Reasoning, Data Interpretation, Information and Communication Technology (ICT), People, Development & Environment, Higher Education System."},
            {"stage": "Paper II: Subject Domain Specialization", "details": "100 objective questions (200 marks, 2 hrs): In-depth assessment in the candidate's chosen Master's subject (Commerce, Economics, Political Science, History, Sociology, English, Management, Law, Psychology, etc.)."}
        ]),
        "syllabus_overview": "Comprehensive higher education pedagogy, research ethics, qualitative/quantitative methods, environmental protocols, ICT in governance, combined with exhaustive subject mastery matching Post-Graduate University curricula.",
        "preparation_roadmap": json.dumps([
            {"phase": "Phase 1: Paper 1 Methodological Mastery", "focus": "Study K.V.S. Madaan for Paper 1. Focus on Research Aptitude, Teaching Aptitude, and Higher Education System governance."},
            {"phase": "Phase 2: Paper 2 Core Subject Syllabus", "focus": "Map 100% of UGC-NET subject syllabus. Create concise concept flashcards and formula sheets for fast review."},
            {"phase": "Phase 3: Previous Year Question Analysis", "focus": "Solve last 10 session papers (2019-2024). Analyze pattern of assertion-reason and matching type questions."}
        ])
    }
]
