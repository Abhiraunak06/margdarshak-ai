from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Index
)
from sqlalchemy.orm import relationship
from .database import Base

class Examination(Base):
    __tablename__ = "examinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    code = Column(String(40), nullable=False, unique=True, index=True) # e.g., JEE_MAIN, JEE_ADV, WBJEE, COMEDK
    stream = Column(String(40), default="PCM", index=True)
    level = Column(String(40), default="National") # National, State, University/Private
    conducting_body = Column(String(150), nullable=True) # e.g., NTA, JoSAA, WBJEEB
    scoring_type = Column(String(40), default="Rank") # Rank, Percentile, Score
    default_rank_type = Column(String(40), default="OVERALL_RANK") # OVERALL_RANK, CATEGORY_RANK, MERIT_RANK
    has_home_state_quota = Column(Boolean, default=True)
    website_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    years = relationship("ExamYear", back_populates="examination", cascade="all, delete-orphan")
    admission_systems = relationship("AdmissionSystem", back_populates="examination", cascade="all, delete-orphan")
    cutoffs = relationship("Cutoff", back_populates="examination")
    sources = relationship("DataSource", back_populates="examination")

class AdmissionSystem(Base):
    __tablename__ = "admission_systems"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), nullable=False, unique=True, index=True) # e.g., JOSAA, CSAB, WBJEE_COUNSELLING, COMEDK_COUNSELLING, VITEEE_COUNSELLING
    name = Column(String(150), nullable=False) # e.g., Joint Seat Allocation Authority (JoSAA)
    exam_id = Column(Integer, ForeignKey("examinations.id"), nullable=False, index=True)
    conducting_body = Column(String(150), nullable=True) # e.g., JoSAA / CSAB / WBJEEB
    website_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    examination = relationship("Examination", back_populates="admission_systems")
    institutes = relationship("AdmissionSystemInstitute", back_populates="admission_system", cascade="all, delete-orphan")
    cutoffs = relationship("Cutoff", back_populates="admission_system")

class AdmissionSystemInstitute(Base):
    __tablename__ = "admission_system_institutes"

    id = Column(Integer, primary_key=True, index=True)
    admission_system_id = Column(Integer, ForeignKey("admission_systems.id"), nullable=False, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    participation_status = Column(String(40), default="CONFIRMED", index=True) # CONFIRMED, PROVISIONAL, WITHDRAWN
    source_name = Column(String(120), nullable=False)
    source_url = Column(String(255), nullable=True)
    verified_at = Column(DateTime, default=datetime.utcnow)
    effective_from = Column(String(40), nullable=True)
    effective_to = Column(String(40), nullable=True)

    admission_system = relationship("AdmissionSystem", back_populates="institutes")
    college = relationship("College", back_populates="admission_participations")

    __table_args__ = (
        Index("idx_adm_inst_unique", "admission_system_id", "college_id", "year", unique=True),
    )

class ExamYear(Base):
    __tablename__ = "exam_years"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("examinations.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    total_rounds = Column(Integer, default=5)

    examination = relationship("Examination", back_populates="years")

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    short_name = Column(String(80), nullable=True, index=True)
    code = Column(String(80), nullable=True, index=True)
    type = Column(String(60), nullable=False, index=True) # IIT, NIT, IIIT, GFTI, State-Govt, Private
    state = Column(String(80), nullable=False, index=True)
    city = Column(String(80), nullable=True)
    established_year = Column(Integer, nullable=True)
    official_website = Column(String(255), nullable=True)
    nirf_rank = Column(Integer, nullable=True)
    is_verified = Column(Boolean, default=True)

    aliases = relationship("CollegeAlias", back_populates="college", cascade="all, delete-orphan")
    cutoffs = relationship("Cutoff", back_populates="college")
    placements = relationship("CollegePlacement", back_populates="college", cascade="all, delete-orphan")
    admission_participations = relationship("AdmissionSystemInstitute", back_populates="college", cascade="all, delete-orphan")

class CollegeAlias(Base):
    __tablename__ = "college_aliases"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    alias_name = Column(String(255), nullable=False, index=True)

    college = relationship("College", back_populates="aliases")

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String(255), nullable=False, unique=True, index=True)
    code = Column(String(40), nullable=True, index=True) # CSE, ECE, ME, etc.
    degree = Column(String(60), default="B.Tech") # B.Tech, B.E., Integrated M.Tech, BS
    duration_years = Column(Integer, default=4)
    discipline = Column(String(80), nullable=True, index=True) # Computer Science, Electrical, etc.

    aliases = relationship("BranchAlias", back_populates="branch", cascade="all, delete-orphan")
    cutoffs = relationship("Cutoff", back_populates="branch")
    placements = relationship("CollegePlacement", back_populates="branch")

class BranchAlias(Base):
    __tablename__ = "branch_aliases"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    raw_source_name = Column(String(255), nullable=False, index=True)

    branch = relationship("Branch", back_populates="aliases")

class Cutoff(Base):
    __tablename__ = "cutoffs"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("examinations.id"), nullable=False, index=True)
    admission_system_id = Column(Integer, ForeignKey("admission_systems.id"), nullable=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    round = Column(Integer, nullable=False, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    quota = Column(String(40), nullable=False, index=True) # AI, HS, OS, GO, JK, LA, etc.
    category = Column(String(40), nullable=False, index=True) # OPEN, OBC-NCL, EWS, SC, ST, etc.
    seat_type = Column(String(60), nullable=True) # OPEN, EWS, OBC-NCL, etc.
    gender = Column(String(40), default="Gender-Neutral", index=True) # Gender-Neutral, Female-only
    rank_type = Column(String(40), default="OVERALL_RANK", index=True) # OVERALL_RANK, CATEGORY_RANK, MERIT_RANK, STATE_RANK
    opening_rank = Column(Integer, nullable=False)
    closing_rank = Column(Integer, nullable=False, index=True)
    source_name = Column(String(120), nullable=False)
    source_url = Column(String(255), nullable=True)
    published_date = Column(String(40), nullable=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow)

    examination = relationship("Examination", back_populates="cutoffs")
    admission_system = relationship("AdmissionSystem", back_populates="cutoffs")
    college = relationship("College", back_populates="cutoffs")
    branch = relationship("Branch", back_populates="cutoffs")

    __table_args__ = (
        Index("idx_cutoff_lookup", "exam_id", "admission_system_id", "year", "category", "quota", "round", "closing_rank"),
        Index("idx_college_branch_year", "college_id", "branch_id", "year"),
    )

class CollegePlacement(Base):
    __tablename__ = "college_placements"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True, index=True)
    is_branch_level = Column(Boolean, default=False)
    median_package_lpa = Column(Float, nullable=True)
    average_package_lpa = Column(Float, nullable=True)
    highest_package_lpa = Column(Float, nullable=True)
    placement_percentage = Column(Float, nullable=True)
    students_placed = Column(Integer, nullable=True)
    students_graduated = Column(Integer, nullable=True)
    source_name = Column(String(120), nullable=False) # e.g., NIRF Engineering Report
    source_url = Column(String(255), nullable=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow)

    college = relationship("College", back_populates="placements")
    branch = relationship("Branch", back_populates="placements")

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("examinations.id"), nullable=True, index=True)
    name = Column(String(120), nullable=False)
    source_url = Column(String(255), nullable=False)
    source_type = Column(String(60), default="Official Portal") # Official Portal, Centralized Dataset, API
    sync_frequency = Column(String(40), default="Daily")
    last_sync_at = Column(DateTime, nullable=True)
    status = Column(String(40), default="Idle") # Idle, Syncing, Success, Error, Temporarily Unavailable

    examination = relationship("Examination", back_populates="sources")
    sync_logs = relationship("DataSyncLog", back_populates="data_source", cascade="all, delete-orphan")

class DataSyncLog(Base):
    __tablename__ = "data_sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=True, index=True)
    exam_code = Column(String(40), nullable=False, index=True)
    status = Column(String(40), nullable=False) # Success, Partial, Failed
    records_fetched = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    data_source = relationship("DataSource", back_populates="sync_logs")

class DataQualityReport(Base):
    __tablename__ = "data_quality_reports"

    id = Column(Integer, primary_key=True, index=True)
    exam_code = Column(String(40), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    total_colleges = Column(Integer, default=0)
    total_branches = Column(Integer, default=0)
    total_cutoffs = Column(Integer, default=0)
    categories_present = Column(Text, nullable=True) # JSON or comma-separated
    quotas_present = Column(Text, nullable=True)
    rounds_present = Column(Text, nullable=True)
    missing_categories = Column(Text, nullable=True)
    missing_branches = Column(Text, nullable=True)
    duplicate_records_count = Column(Integer, default=0)
    invalid_ranks_count = Column(Integer, default=0)
    completeness_score = Column(Float, default=100.0) # 0 to 100%
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, unique=True)
    slug = Column(String(80), nullable=False, unique=True, index=True)
    domain = Column(String(80), nullable=False, index=True) # Software, Hardware, Core, AI, Emerging
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False) # Comma-separated or JSON string
    recommended_degrees = Column(Text, nullable=False)
    relevant_branches = Column(Text, nullable=False)
    entrance_exams = Column(Text, nullable=False)
    roadmap_steps = Column(Text, nullable=False) # JSON formatted steps
    stream = Column(String(40), default="PCM", index=True) # PCM, PCB, COMMERCE, ARTS
    average_starting_salary_lpa = Column(Float, nullable=True)
    growth_outlook = Column(String(60), default="High")

class MedicalCollege(Base):
    __tablename__ = "medical_colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    short_name = Column(String(80), nullable=True, index=True)
    code = Column(String(80), nullable=True, index=True)
    type = Column(String(60), nullable=False, index=True) # AIIMS, Central University, State-Govt, Deemed, Private
    state = Column(String(80), nullable=False, index=True)
    city = Column(String(80), nullable=True)
    established_year = Column(Integer, nullable=True)
    official_website = Column(String(255), nullable=True)
    nirf_medical_rank = Column(Integer, nullable=True)
    annual_tuition_fee_inr = Column(Integer, nullable=True)
    is_verified = Column(Boolean, default=True)

    cutoffs = relationship("NeetCutoff", back_populates="college", cascade="all, delete-orphan")
    placements = relationship("MedicalPlacement", back_populates="college", cascade="all, delete-orphan")

class MedicalCourse(Base):
    __tablename__ = "medical_courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True, index=True) # MBBS, BDS, BAMS, BHMS, BUMS, BVSc & AH, B.Sc Nursing, B.Pharm, BPT
    code = Column(String(40), nullable=False, unique=True, index=True)
    degree = Column(String(60), default="MBBS")
    duration_years = Column(Float, default=5.5) # e.g. 5.5 years for MBBS (4.5 + 1 year internship)
    requires_neet = Column(Boolean, default=True)
    description = Column(Text, nullable=True)

    cutoffs = relationship("NeetCutoff", back_populates="course", cascade="all, delete-orphan")

class NeetCutoff(Base):
    __tablename__ = "neet_cutoffs"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    round = Column(Integer, nullable=False, index=True)
    counselling_authority = Column(String(80), default="MCC", index=True) # MCC (All India Quota) or State Medical Counselling
    quota = Column(String(40), nullable=False, index=True) # All India Quota (AIQ), State Quota, Delhi University Quota, IP Quota, Deemed/Paid Seats
    college_id = Column(Integer, ForeignKey("medical_colleges.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("medical_courses.id"), nullable=False, index=True)
    category = Column(String(40), nullable=False, index=True) # OPEN, OBC, EWS, SC, ST, PwD
    opening_rank = Column(Integer, nullable=False)
    closing_rank = Column(Integer, nullable=False, index=True)
    neet_score_approx = Column(Integer, nullable=True) # NEET score (out of 720) corresponding to closing rank
    source_name = Column(String(120), default="MCC NEET-UG Official Seat Allotment")
    source_url = Column(String(255), default="https://mcc.nic.in")
    last_verified_at = Column(DateTime, default=datetime.utcnow)

    college = relationship("MedicalCollege", back_populates="cutoffs")
    course = relationship("MedicalCourse", back_populates="cutoffs")

    __table_args__ = (
        Index("idx_neet_lookup", "year", "round", "quota", "category", "closing_rank"),
        Index("idx_neet_college_course", "college_id", "course_id", "year"),
    )

class MedicalPlacement(Base):
    __tablename__ = "medical_placements"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("medical_colleges.id"), nullable=False, index=True)
    monthly_internship_stipend_inr = Column(Integer, nullable=True)
    junior_resident_starting_salary_pm = Column(Integer, nullable=True)
    compulsory_rural_service_years = Column(Integer, default=0)
    bond_penalty_amount_lakhs = Column(Float, default=0.0)
    source_name = Column(String(120), default="State Directorate of Medical Education")
    source_url = Column(String(255), nullable=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow)

    college = relationship("MedicalCollege", back_populates="placements")

class UniversityCollege(Base):
    __tablename__ = "university_colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    short_name = Column(String(80), nullable=True, index=True)
    code = Column(String(80), nullable=True, index=True)
    type = Column(String(60), nullable=False, index=True) # Central University, State University, National Law University, IIM, Private
    stream = Column(String(40), nullable=False, index=True) # COMMERCE, ARTS, LAW, MANAGEMENT
    state = Column(String(80), nullable=False, index=True)
    city = Column(String(80), nullable=True)
    established_year = Column(Integer, nullable=True)
    official_website = Column(String(255), nullable=True)
    nirf_rank = Column(Integer, nullable=True)
    annual_tuition_fee_inr = Column(Integer, nullable=True)
    median_package_lpa = Column(Float, nullable=True)
    highest_package_lpa = Column(Float, nullable=True)
    placement_source = Column(String(120), nullable=True)
    is_verified = Column(Boolean, default=True)

    cutoffs = relationship("UniversityCutoff", back_populates="college", cascade="all, delete-orphan")

class UniversityCourse(Base):
    __tablename__ = "university_courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True, index=True)
    code = Column(String(40), nullable=False, unique=True, index=True)
    degree = Column(String(60), nullable=False) # B.Com (Hons), B.A. (Hons), BMS, BBA, B.A. LL.B. (Hons), IPM (BBA+MBA)
    stream = Column(String(40), nullable=False, index=True) # COMMERCE, ARTS, LAW, MANAGEMENT
    duration_years = Column(Integer, default=3)

    cutoffs = relationship("UniversityCutoff", back_populates="course", cascade="all, delete-orphan")

class UniversityCutoff(Base):
    __tablename__ = "university_cutoffs"

    id = Column(Integer, primary_key=True, index=True)
    exam_code = Column(String(40), nullable=False, index=True) # CUET_UG, IPMAT, CLAT
    year = Column(Integer, nullable=False, index=True)
    round = Column(Integer, default=1, index=True)
    college_id = Column(Integer, ForeignKey("university_colleges.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("university_courses.id"), nullable=False, index=True)
    category = Column(String(40), nullable=False, index=True) # OPEN, OBC, EWS, SC, ST
    rank_type = Column(String(40), default="SCORE") # SCORE, PERCENTILE, ALL_INDIA_RANK
    min_cutoff_value = Column(Float, nullable=False) # e.g. 780 marks or 99.5 percentile or Rank 120
    max_cutoff_value = Column(Float, nullable=True)
    source_name = Column(String(120), nullable=False)
    source_url = Column(String(255), nullable=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow)

    college = relationship("UniversityCollege", back_populates="cutoffs")
    course = relationship("UniversityCourse", back_populates="cutoffs")

    __table_args__ = (
        Index("idx_univ_cutoff_lookup", "exam_code", "year", "category", "min_cutoff_value"),
    )

class GovernmentExam(Base):
    __tablename__ = "government_exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True, index=True) # UPSC_CSE, SSC_CGL, IBPS_PO, RRB_NTPC, CDS, AFCAT, STATE_PSC, UGC_NET
    conducting_body = Column(String(120), nullable=False)
    sector = Column(String(80), nullable=False) # Civil Services, Staff Selection, Public Sector Banking, Indian Railways, Armed Forces, Academia
    eligibility_education = Column(String(150), nullable=False) # Any Bachelor's Degree, 10+2, Master's Degree
    min_age = Column(Integer, default=21)
    max_age = Column(Integer, default=32)
    selection_stages = Column(Text, nullable=False) # JSON: Prelims, Mains, Interview
    syllabus_overview = Column(Text, nullable=False)
    career_roles = Column(Text, nullable=False) # IAS, IPS, Tax Inspector, Probationary Officer
    salary_scale = Column(String(80), nullable=True) # Level 10 Pay Matrix (Rs. 56,100 - Rs. 1,77,500)
    official_website = Column(String(255), nullable=True)
    application_window = Column(String(120), nullable=True)
    preparation_roadmap = Column(Text, nullable=False) # JSON formatted phase-wise prep guidance

