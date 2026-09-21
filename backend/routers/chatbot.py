import re
import httpx
import os
import io
import json
import urllib.request
import urllib.parse
import joblib
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

router = APIRouter(prefix="/api/chatbot", tags=["Class 12 Career Recommender ML"])

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "career_dataset_v5_balanced_realistic.csv")
MODEL_CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "career_recommendation_v5_bundle.pkl")

# 15 High-Impact Features as specified in the user's ML script
KEY_FEATURES = [
    ("biology_interest", "Interest in Biology & Living Systems"),
    ("medical_healthcare_interest", "Interest in Medicine, Clinical Care & Health"),
    ("chemistry_interest", "Interest in Chemistry, Formulations & Drugs"),
    ("computer_interest", "Interest in Computers, Programming & Software"),
    ("mathematics_interest", "Interest in Mathematics & Numbers"),
    ("accountancy_interest", "Interest in Accounting, Auditing & Ledgers"),
    ("business_finance_interest", "Interest in Financial Markets & Banking"),
    ("business_interest", "Interest in Business Strategy & Startups"),
    ("law_debate_interest", "Interest in Law, Rules & Legal Debates"),
    ("history_political_science_interest", "Interest in History, Politics & Civics"),
    ("government_public_service_interest", "Interest in Civil Service & Public Administration"),
    ("psychology_interest", "Interest in Human Psychology & Mental Health"),
    ("teaching_interest", "Interest in Teaching, Lecturing & Mentoring"),
    ("public_speaking", "Confidence in Public Speaking & Presenting"),
    ("creativity", "Creativity, Hands-on Dexterity & Design"),
]

FEATURE_COLS = [f[0] for f in KEY_FEATURES]

CAREER_METADATA: Dict[str, Dict[str, Any]] = {
    "Engineering": {
        "recommended_stream": "PCM",
        "target_stream": "PCM",
        "target_tab": "predictor",
        "career_family": "Engineering & Technology (B.Tech / B.E.)",
        "representative_roles": "Software Engineer, AI/ML Specialist, Systems Architect, Robotics Engineer",
        "typical_path_after_12": "Class 12 (PCM) -> JEE Main / Advanced / BITSAT -> 4-Year B.Tech -> Tech Industry / Innovation",
        "redirect_label": "Explore Engineering & JEE Predictor",
        "colleges": [
            {"name": "IIT Bombay", "degree": "B.Tech Computer Science / EE", "exam": "JEE Advanced"},
            {"name": "IIT Delhi", "degree": "B.Tech Computer Science / Math & Computing", "exam": "JEE Advanced"},
            {"name": "BITS Pilani", "degree": "B.E. Computer Science / Electronics", "exam": "BITSAT"},
            {"name": "NIT Trichy", "degree": "B.Tech Computer Science / ECE", "exam": "JEE Main"},
        ]
    },
    "MBBS / Doctor": {
        "recommended_stream": "PCB",
        "target_stream": "PCB",
        "target_tab": "predictor",
        "career_family": "Medicine & Clinical Surgery (MBBS)",
        "representative_roles": "Physician, Surgeon, Cardiologist, Pediatrician, Radiologist",
        "typical_path_after_12": "Class 12 (PCB) -> NEET UG -> 5.5-Year MBBS + 1-Year Internship -> MD/MS Specialization",
        "redirect_label": "Explore Medical & NEET Predictor",
        "colleges": [
            {"name": "AIIMS New Delhi", "degree": "MBBS", "exam": "NEET UG"},
            {"name": "Christian Medical College (CMC) Vellore", "degree": "MBBS", "exam": "NEET UG"},
            {"name": "JIPMER Puducherry", "degree": "MBBS", "exam": "NEET UG"},
            {"name": "King George's Medical University (KGMU)", "degree": "MBBS", "exam": "NEET UG"},
        ]
    },
    "Dentist": {
        "recommended_stream": "PCB",
        "target_stream": "PCB",
        "target_tab": "predictor",
        "career_family": "Dental Surgery & Oral Healthcare (BDS)",
        "representative_roles": "Dental Surgeon, Orthodontist, Periodontist, Implantologist",
        "typical_path_after_12": "Class 12 (PCB) -> NEET UG -> 5-Year BDS -> Dental Practice / MDS Specialization",
        "redirect_label": "Explore Dental & Medical Portal",
        "colleges": [
            {"name": "Maulana Azad Institute of Dental Sciences, Delhi", "degree": "BDS", "exam": "NEET UG"},
            {"name": "Manipal College of Dental Sciences", "degree": "BDS", "exam": "NEET UG"},
            {"name": "Faculty of Dental Sciences, KGMU Lucknow", "degree": "BDS", "exam": "NEET UG"},
        ]
    },
    "Pharmacy": {
        "recommended_stream": "PCB",
        "target_stream": "PCB",
        "target_tab": "predictor",
        "career_family": "Pharmaceutical Sciences & Drug Discovery (B.Pharm)",
        "representative_roles": "Clinical Pharmacist, Drug Formulation Scientist, Regulatory Affairs Specialist",
        "typical_path_after_12": "Class 12 (PCB/PCM) -> State CET / NEET / GPAT -> 4-Year B.Pharm / 6-Year Pharm.D -> Pharma R&D",
        "redirect_label": "Explore Pharmacy & Medical Portal",
        "colleges": [
            {"name": "Jamia Hamdard, New Delhi (NIRF #1)", "degree": "B.Pharm / Pharm.D", "exam": "NEET / Merit"},
            {"name": "National Institute of Pharmaceutical Education (NIPER) Mohali", "degree": "M.Pharm / MS (Pharm)", "exam": "NIPER JEE"},
            {"name": "Institute of Chemical Technology (ICT) Mumbai", "degree": "B.Pharm", "exam": "MHT CET / NEET"},
        ]
    },
    "CA / Accounting": {
        "recommended_stream": "Commerce",
        "target_stream": "COMMERCE",
        "target_tab": "predictor",
        "career_family": "Chartered Accountancy & Financial Audit (CA / CMA)",
        "representative_roles": "Chartered Accountant (CA), Forensic Auditor, Tax Consultant, Chief Financial Officer (CFO)",
        "typical_path_after_12": "Class 12 -> ICAI CA Foundation -> CA Intermediate + Articleship -> CA Final",
        "redirect_label": "Explore Commerce & CA Portal",
        "colleges": [
            {"name": "Institute of Chartered Accountants of India (ICAI)", "degree": "CA Designation", "exam": "CA Foundation / Inter"},
            {"name": "Shri Ram College of Commerce (SRCC) Delhi", "degree": "B.Com (Hons)", "exam": "CUET UG"},
            {"name": "St. Xavier's College Kolkata", "degree": "B.Com (Hons) Accountancy", "exam": "Merit / Entrance"},
        ]
    },
    "Finance / Banking": {
        "recommended_stream": "Commerce",
        "target_stream": "COMMERCE",
        "target_tab": "predictor",
        "career_family": "Investment Banking & Corporate Finance (BBA / CFA)",
        "representative_roles": "Investment Banker, Equity Research Analyst, Portfolio Manager, Risk Modeler",
        "typical_path_after_12": "Class 12 -> CUET / IPMAT -> BBA Finance / B.Com / Eco (Hons) -> CFA / MBA Finance",
        "redirect_label": "Explore Finance & Banking Portal",
        "colleges": [
            {"name": "Shaheed Sukhdev College of Business Studies (SSCBS)", "degree": "BMS / BFIA", "exam": "CUET UG"},
            {"name": "IIM Indore (5-Year Integrated IPM)", "degree": "BBA + MBA", "exam": "IPMAT"},
            {"name": "NMIMS Mumbai", "degree": "B.Com / BBA Finance", "exam": "NMIMS NPAT"},
        ]
    },
    "Business / Management": {
        "recommended_stream": "Commerce",
        "target_stream": "COMMERCE",
        "target_tab": "predictor",
        "career_family": "Business Strategy, Management & Entrepreneurship (BBA / MBA)",
        "representative_roles": "Management Consultant, Startup Founder, Product Strategist, Operations Director",
        "typical_path_after_12": "Class 12 -> IPMAT / CUET -> 5-Year IPM or BBA -> MBA / Corporate Leadership",
        "redirect_label": "Explore Business Management Portal",
        "colleges": [
            {"name": "IIM Indore / IIM Rohtak", "degree": "5-Year Integrated Program in Management (IPM)", "exam": "IPMAT"},
            {"name": "SSCBS University of Delhi", "degree": "Bachelor of Management Studies (BMS)", "exam": "CUET UG"},
            {"name": "Christ University Bengaluru", "degree": "BBA Honors", "exam": "CUET / Christ Entrance"},
        ]
    },
    "Law": {
        "recommended_stream": "Humanities/Arts",
        "target_stream": "ARTS",
        "target_tab": "predictor",
        "career_family": "Corporate & Constitutional Law (BA LLB / BBA LLB)",
        "representative_roles": "Corporate Lawyer, Litigator, Cyber Law Counsel, Judicial Magistrate",
        "typical_path_after_12": "Class 12 -> CLAT UG / AILET -> 5-Year Integrated BA LLB / BBA LLB -> Bar Council Enrollment",
        "redirect_label": "Explore Law & Arts Portal",
        "colleges": [
            {"name": "National Law School of India University (NLSIU) Bengaluru", "degree": "5-Year BA LLB (Hons)", "exam": "CLAT UG"},
            {"name": "NALSAR University of Law, Hyderabad", "degree": "5-Year BA LLB (Hons)", "exam": "CLAT UG"},
            {"name": "National Law University (NLU) Delhi", "degree": "5-Year BA LLB (Hons)", "exam": "AILET"},
        ]
    },
    "Civil Services": {
        "recommended_stream": "Humanities/Arts",
        "target_stream": "ARTS",
        "target_tab": "predictor",
        "career_family": "Civil Services, Public Policy & Governance (IAS / IPS)",
        "representative_roles": "Indian Administrative Officer (IAS), Indian Police Officer (IPS), Diplomat (IFS), Policy Analyst",
        "typical_path_after_12": "Class 12 -> Bachelor's Degree (Any Stream) -> UPSC Civil Services Examination (Prelims + Mains + Interview)",
        "redirect_label": "Explore Civil Services & Arts Portal",
        "colleges": [
            {"name": "St. Stephen's College, Delhi", "degree": "BA (Hons) History / Economics", "exam": "CUET UG"},
            {"name": "Hindu College, University of Delhi", "degree": "BA (Hons) Political Science", "exam": "CUET UG"},
            {"name": "Miranda House, Delhi", "degree": "BA (Hons) Political Science / History", "exam": "CUET UG"},
        ]
    },
    "Journalism / Media": {
        "recommended_stream": "Humanities/Arts",
        "target_stream": "ARTS",
        "target_tab": "predictor",
        "career_family": "Journalism, Mass Communication & Digital Broadcasting (BJMC)",
        "representative_roles": "Investigative Journalist, News Anchor, Digital Content Director, Broadcast Producer",
        "typical_path_after_12": "Class 12 -> CUET UG / College Entrance -> 3-Year BJMC / BMM -> Top Media & Broadcast Houses",
        "redirect_label": "Explore Journalism & Media Portal",
        "colleges": [
            {"name": "Indian Institute of Mass Communication (IIMC) New Delhi", "degree": "PG Diploma in Journalism", "exam": "CUET PG / IIMC Entrance"},
            {"name": "Asian College of Journalism (ACJ) Chennai", "degree": "Postgraduate Diploma in Journalism", "exam": "ACJ Entrance Exam"},
            {"name": "Xavier Institute of Communications (XIC) Mumbai", "degree": "Diploma in Journalism & Mass Comm", "exam": "OET Entrance"},
        ]
    },
    "Psychology": {
        "recommended_stream": "Humanities/Arts",
        "target_stream": "ARTS",
        "target_tab": "predictor",
        "career_family": "Psychology, Behavioral Science & Counseling (BA / B.Sc)",
        "representative_roles": "Clinical Psychologist, Counseling Psychologist, Neuropsychologist, Cognitive Scientist",
        "typical_path_after_12": "Class 12 -> CUET UG -> BA/B.Sc Psychology -> M.Sc / M.Phil Clinical Psychology (RCI Licensed)",
        "redirect_label": "Explore Psychology & Arts Portal",
        "colleges": [
            {"name": "Lady Shri Ram College (LSR) Delhi", "degree": "BA (Hons) Psychology", "exam": "CUET UG"},
            {"name": "Christ University Bengaluru", "degree": "B.Sc Psychology (Hons)", "exam": "Christ Entrance Test"},
            {"name": "Tata Institute of Social Sciences (TISS) Mumbai", "degree": "MA Applied Psychology", "exam": "CUET PG"},
        ]
    },
    "Teaching / Professor": {
        "recommended_stream": "Humanities/Arts",
        "target_stream": "ARTS",
        "target_tab": "predictor",
        "career_family": "Academia, Higher Education & Scientific Research",
        "representative_roles": "University Professor, Research Scientist, Academic Dean, Curriculum Architect",
        "typical_path_after_12": "Class 12 -> Bachelor's Degree -> Master's Degree -> UGC-NET / CSIR-NET -> Ph.D -> Professorship",
        "redirect_label": "Explore Teaching & Academia Portal",
        "colleges": [
            {"name": "Delhi University (CIE)", "degree": "B.Ed / M.Ed / Ph.D", "exam": "CUET PG"},
            {"name": "Banaras Hindu University (BHU) Varanasi", "degree": "Integrated B.Ed / Masters", "exam": "CUET PG"},
            {"name": "Jawaharlal Nehru University (JNU) New Delhi", "degree": "MA / M.Phil / Ph.D", "exam": "CUET PG / UGC-NET"},
        ]
    }
}

class CareerModelManager:
    """
    Manages loading, training, and caching of the 15-Feature Random Forest Recommender.
    """
    def __init__(self):
        self.model: Optional[RandomForestClassifier] = None
        self.label_encoder: Optional[LabelEncoder] = None
        self.class_benchmarks: Optional[pd.DataFrame] = None
        self.global_means: Optional[pd.Series] = None
        self.feature_cols: List[str] = FEATURE_COLS
        self._initialize()

    def _initialize(self):
        if os.path.exists(MODEL_CACHE_PATH):
            try:
                bundle = joblib.load(MODEL_CACHE_PATH)
                self.model = bundle["model"]
                self.label_encoder = bundle["label_encoder"]
                self.class_benchmarks = bundle["class_benchmarks"]
                self.global_means = bundle["global_means"]
                self.feature_cols = bundle["feature_cols"]
                print("[CareerModelManager] Loaded cached model bundle successfully.")
                return
            except Exception as e:
                print(f"[CareerModelManager] Cache load failed ({e}), retraining from dataset...")

        self._train_and_cache()

    def _train_and_cache(self):
        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

        df = pd.read_csv(DATASET_PATH)
        X = df[self.feature_cols]
        y = df["career_choice"]

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=RANDOM_SEED, stratify=y_encoded
        )

        model = RandomForestClassifier(n_estimators=150, max_depth=14, random_state=RANDOM_SEED, n_jobs=1)
        model.fit(X_train, y_train)

        train_df = X_train.copy()
        train_df["career"] = label_encoder.inverse_transform(y_train)
        class_benchmarks = train_df.groupby("career")[self.feature_cols].mean()
        global_means = X_train.mean()

        self.model = model
        self.label_encoder = label_encoder
        self.class_benchmarks = class_benchmarks
        self.global_means = global_means

        bundle = {
            "model": model,
            "label_encoder": label_encoder,
            "class_benchmarks": class_benchmarks,
            "global_means": global_means,
            "feature_cols": self.feature_cols,
        }
        try:
            joblib.dump(bundle, MODEL_CACHE_PATH)
            print(f"[CareerModelManager] Model successfully trained (accuracy: {model.score(X_test, y_test)*100:.1f}%) and cached.")
        except Exception as e:
            print(f"[CareerModelManager] Could not cache model bundle: {e}")

    def explain_career(self, user_scores: Dict[str, float], career: str, top_n: int = 3) -> List[str]:
        if self.class_benchmarks is None or career not in self.class_benchmarks.index:
            return []

        career_avg = self.class_benchmarks.loc[career]
        distinctiveness = career_avg - self.global_means

        reasons = []
        for col in self.feature_cols:
            u_val = user_scores.get(col, 5.0)
            c_val = career_avg[col]
            d_val = distinctiveness[col]

            clean_col = col.replace("_", " ")

            # Key required trait where user also scored high
            if d_val > 1.2 and u_val >= 7:
                diff = abs(u_val - c_val)
                reasons.append({
                    "rank": diff - d_val,
                    "text": f"High {clean_col} ({int(u_val)}/10 matches target profile ~{c_val:.1f}/10)"
                })
            # Field typically requires little focus here and user scored low
            elif d_val < -1.2 and u_val <= 4:
                diff = abs(u_val - c_val)
                reasons.append({
                    "rank": diff + d_val,
                    "text": f"Low {clean_col} ({int(u_val)}/10 matches target profile ~{c_val:.1f}/10)"
                })

        reasons.sort(key=lambda x: x["rank"])
        return [r["text"] for r in reasons[:top_n]]

manager = CareerModelManager()

class CareerRecommenderInput(BaseModel):
    student_name: Optional[str] = "Student"
    stream: Optional[str] = "PCM"
    answers: Dict[str, Any] = Field(..., description="Map of question_id or feature_name -> rating (1 to 10)")

@router.get("/questions")
def get_assessment_questions() -> Dict[str, Any]:
    """
    Returns the 15 high-impact questions configured on a 1-to-10 rating scale (default 5).
    """
    questions_list = []
    for idx, (feat, prompt) in enumerate(KEY_FEATURES, start=1):
        questions_list.append({
            "id": f"q{idx}",
            "question_num": idx,
            "feature": feat,
            "prompt": prompt,
            "min_val": 1,
            "max_val": 10,
            "default_val": 5
        })

    return {
        "status": "Success",
        "total_questions": len(questions_list),
        "scale": {"min": 1, "max": 10, "default": 5},
        "streams": ["PCM", "PCB", "Commerce", "Humanities/Arts"],
        "questions": questions_list
    }

@router.post("/recommend")
def recommend_careers(payload: CareerRecommenderInput) -> Dict[str, Any]:
    """
    Runs the 15-Feature Random Forest ML Career Prediction Engine and Explainability Module.
    Returns the Top 3 career matches with confidence %, explainability reasons, and website redirection metadata.
    """
    user_scores = {}
    answers = payload.answers or {}

    # Map inputs whether provided by feature name or question ID (e.g. q1..q15)
    for idx, (col, _) in enumerate(KEY_FEATURES, start=1):
        qid = f"q{idx}"
        val = 5.0
        if col in answers:
            try:
                val = float(answers[col])
            except (ValueError, TypeError):
                val = 5.0
        elif qid in answers:
            try:
                val = float(answers[qid])
            except (ValueError, TypeError):
                val = 5.0

        val = max(1.0, min(10.0, val))
        user_scores[col] = val

    # Model inference
    input_data = pd.DataFrame([user_scores])[FEATURE_COLS]
    probabilities = manager.model.predict_proba(input_data)[0]
    top_indices = np.argsort(probabilities)[::-1][:3]

    recommendations = []
    for rank, idx in enumerate(top_indices, start=1):
        career = manager.label_encoder.classes_[idx]
        confidence = round(float(probabilities[idx] * 100.0), 1)
        reasons = manager.explain_career(user_scores, career)
        if not reasons:
            reasons = ["Balanced compatibility across multiple core domains."]

        meta = CAREER_METADATA.get(career, {
            "recommended_stream": "PCM",
            "target_stream": "PCM",
            "target_tab": "predictor",
            "career_family": career,
            "representative_roles": "Specialist / Professional",
            "typical_path_after_12": "Undergraduate Degree -> Specialization",
            "redirect_label": f"Explore {career} on our website",
            "colleges": []
        })

        recommendations.append({
            "rank": rank,
            "career": career,
            "career_family": meta["career_family"],
            "confidence": confidence,
            "compatibility_score": confidence,
            "reasons": reasons,
            "recommended_stream": meta["recommended_stream"],
            "target_stream": meta["target_stream"],
            "target_tab": meta["target_tab"],
            "redirect_label": meta["redirect_label"],
            "representative_roles": meta["representative_roles"],
            "typical_path_after_12": meta["typical_path_after_12"],
            "associated_colleges": meta["colleges"]
        })

    return {
        "status": "Success",
        "algorithm": "Random Forest Classifier (150 trees, 15 High-Impact Features, Explainability Engine)",
        "student_name": payload.student_name or "Student",
        "top_career": recommendations[0]["career"] if recommendations else None,
        "recommendations": recommendations
    }

class ChatMessageInput(BaseModel):
    message: str = Field(..., description="User query or greeting to Margdarshak AI")
    history: Optional[List[Dict[str, str]]] = Field(default=[], description="Recent conversation turns")
    student_name: Optional[str] = "Student"
    api_key: Optional[str] = Field(default=None, description="Optional Google Gemini API key provided by user")

async def query_gemini_api(user_message: str, history: List[Dict[str, str]], api_key: str) -> Optional[Dict[str, Any]]:
    """
    Calls Google Gemini 1.5 Flash API with Google Search Grounding.
    Returns generated text and grounding sources / URLs if available.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    system_instruction = (
        "You are Margdarshak AI, an empathetic, highly knowledgeable, and interactive career mentor and educational advisor for Indian students. "
        "You provide comprehensive, clear, accurate, and encouraging guidance on Class 10/12 stream choices (PCM, PCB, Commerce, Arts/Humanities), "
        "entrance exams (JEE, NEET, CUET, CLAT, CA, IPMAT, NDA, NATA, etc.), college cutoffs, eligibility criteria, and modern career paths. "
        "Format responses cleanly with bold headings, bullet points, and actionable steps. "
        "Always mention that Margdarshak also provides a 15-question psychometric machine learning career assessment that calculates exact career compatibility."
    )
    contents = []
    for h in (history or [])[-6:]:
        role = "user" if h.get("sender") == "user" else "model"
        text = h.get("text", "")
        if text:
            contents.append({"role": role, "parts": [{"text": text}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    # 1. Attempt with Google Search Grounding
    payload_search = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
        "tools": [{"googleSearch": {}}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1000}
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            res = await client.post(url, json=payload_search)
            if res.status_code == 200:
                data = res.json()
                candidate = data["candidates"][0]
                text = candidate["content"]["parts"][0]["text"]
                sources = []
                grounding = candidate.get("groundingMetadata", {})
                for chunk in grounding.get("groundingChunks", []):
                    web = chunk.get("web", {})
                    if web.get("uri") and web.get("title"):
                        sources.append({"title": web["title"], "url": web["uri"]})
                return {
                    "reply": text,
                    "sources": sources,
                    "model": "Gemini 1.5 Flash (Live Google Search Grounded)"
                }
        except Exception as e:
            print(f"[Gemini Search Grounding error]: {e}")

        # 2. Fallback without search tool
        try:
            payload_basic = {
                "system_instruction": {"parts": [{"text": system_instruction}]},
                "contents": contents,
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1000}
            }
            res = await client.post(url, json=payload_basic)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "reply": text,
                    "sources": [],
                    "model": "Gemini 1.5 Flash"
                }
            else:
                print(f"[Gemini API HTTP {res.status_code}]: {res.text}")
        except Exception as e:
            print(f"[Gemini Basic Generation error]: {e}")

    return None

def search_live_web_knowledge(query: str, limit: int = 3) -> List[Dict[str, str]]:
    """
    Fetches real-time internet knowledge excerpts, summaries, and URLs via Wikipedia REST API.
    """
    clean_q = re.sub(r'[^a-zA-Z0-9\s]', ' ', query).strip()
    stopwords = {
        'i', 'am', 'a', 'want', 'to', 'do', 'what', 'how', 'is', 'the', 'for', 'in', 
        'after', '12th', 'tell', 'me', 'about', 'can', 'should', 'my', 'name', 'hi', 
        'hello', 'hey', 'so', 'will', 'be', 'this', 'that', 'with', 'and', 'or', 'which'
    }
    tokens = [w for w in clean_q.split() if w.lower() not in stopwords]
    search_term = " ".join(tokens[:5]) if tokens else clean_q

    url = f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={urllib.parse.quote(search_term)}&limit={limit}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "MargdarshakAI/2.0 (student.counselor@margdarshak.edu)"
    })
    DISALLOWED_TERMS = {'suicide', 'murder', 'crash', 'disaster', 'accident', 'slop', 'porn', 'terror', 'death', 'casualty'}
    results = []
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for page in data.get("pages", []):
                title = page.get("title", "")
                desc = page.get("description", "")
                excerpt = re.sub(r'<[^>]+>', '', page.get("excerpt", "")).strip()
                combined = f"{title} {desc} {excerpt}".lower()
                if any(bad in combined for bad in DISALLOWED_TERMS):
                    continue
                key = page.get("key", title.replace(" ", "_"))
                link = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(key)}"
                if title:
                    results.append({
                        "title": title,
                        "description": desc or "Online Knowledge Base",
                        "snippet": excerpt,
                        "url": link
                    })
    except Exception as e:
        print(f"[search_live_web_knowledge error]: {e}")
    return results

def generate_margdarshak_response(user_text: str, history: List[Dict[str, str]], student_name: Optional[str] = "Student") -> Dict[str, Any]:
    """
    Dynamic, internet-grounded conversational career guidance engine.
    Fetches live internet knowledge and dynamically answers greetings, identity queries,
    and open-ended career questions with structured facts and web citations.
    """
    text_clean = user_text.strip()
    text_lower = text_clean.lower()

    # 1. Assessment trigger
    if any(k in text_lower for k in ["start assessment", "take assessment", "15 question", "start quiz", "start test", "questionnaire"]):
        return {
            "reply": (
                "🎯 **Starting the 15-Question Machine Learning Career Assessment!**\n\n"
                "I will present 15 core aptitude dimensions rated from **1 (lowest) to 10 (highest)** (neutral default is 5).\n\n"
                "Our **Random Forest ML Model** will then evaluate your distinctiveness benchmarks against 7,200 empirical student profiles to compute your Top 3 career matches with explainability insights."
            ),
            "suggestions": ["✨ Start 15-Question Assessment", "How does the ML model work?"],
            "action": "start_assessment",
            "sources": []
        }

    # 2. Extract name if student introduces themselves (e.g. 'Hi, my name is Shubham' or 'I am Priya')
    name_match = re.search(r"(?:my name is|i am|this is|call me)\s+([A-Za-z]+)", text_clean, re.IGNORECASE)
    detected_name = name_match.group(1).capitalize() if name_match else (student_name or "Student")
    if detected_name.lower() in ["a", "an", "the", "student", "here", "just", "trying", "looking", "interested"]:
        detected_name = student_name or "Student"

    # 3. Questions about Bot Name / Identity ("What are your name?", "What is your name?", "Who are you?")
    if any(q in text_lower for q in ["what is your name", "what are your name", "whats your name", "who are you", "your name"]):
        return {
            "reply": (
                f"Hello {detected_name if detected_name != 'Student' else ''}! I am **Margdarshak AI** (मार्गदर्शक — *meaning Pathfinder & Guide*).\n\n"
                "I am your dedicated, interactive AI educational counselor and college discovery mentor for Indian students.\n\n"
                "### What I can do for you:\n"
                "• **Answer Any Career Question:** From commercial piloting, robotics, and biotechnology to CA, law, and civil services.\n"
                "• **Live Internet Grounding:** I pull real-time encyclopedic and academic information directly from the web.\n"
                "• **Stream & Exam Roadmaps:** Comprehensive blueprints for Class 11-12 streams (PCM, PCB, Commerce, Arts) and exams like JEE, NEET, CUET, CLAT, IPMAT, and NDA.\n"
                "• **15-Question ML Career Assessment:** Machine learning evaluation across 7,200 empirical benchmarks to predict your top 3 matching careers.\n\n"
                "How can I assist your educational journey today?"
            ),
            "suggestions": ["✨ Start 15-Question Assessment", "What should I do?", "Tell me about Engineering (PCM)", "Tell me about Medical (PCB)"],
            "action": "none",
            "sources": []
        }

    # 4. Greetings & Introductions ("Hi, my name is Shubham", "Hello", "Hey")
    if any(re.search(rf"\b{g}\b", text_lower) for g in ["hi", "hello", "hey", "namaste", "good morning", "good afternoon", "good evening"]):
        if name_match:
            return {
                "reply": (
                    f"Hello **{detected_name}**! It's fantastic to meet you! 😊\n\n"
                    "Welcome to **Margdarshak AI**. I'm here to help you navigate your academic and career choices with confidence.\n\n"
                    "You can ask me anything — for example: *\"I want to become an AI engineer\"*, *\"What are the top medical colleges?\"*, *\"How to prepare for CA?\"*, or take our **15-Question Machine Learning Career Assessment** to find your ideal career path."
                ),
                "suggestions": ["✨ Start 15-Question Assessment", "What should I do?", "I like computers & coding", "I want to become a Doctor"],
                "action": "none",
                "sources": []
            }
        return {
            "reply": (
                f"Hello! Welcome to **Margdarshak AI**.\n\n"
                "I am your interactive career mentor. You can ask me any question about career roadmaps, college admissions, or competitive exams. "
                "You can also take our **15-Question Machine Learning Career Assessment** to discover your strongest career alignments."
            ),
            "suggestions": ["✨ Start 15-Question Assessment", "What should I do?", "Tell me about Engineering (PCM)", "Tell me about Medical (PCB)"],
            "action": "none",
            "sources": []
        }

    # 5. "What should I do?" / "What I should do?" / "I am confused"
    if any(phrase in text_lower for phrase in ["what should i do", "what i should do", "i am confused", "what to do", "help me choose", "which stream"]):
        return {
            "reply": (
                f"It is completely natural to feel uncertain, **{detected_name}**! Choosing your direction after Class 10 or 12 is a big milestone. "
                "Here is a proven 3-step framework to guide you:\n\n"
                "### 1. Identify Your Core Aptitude\n"
                "• **PCM (Engineering & Tech):** For students who enjoy math, logic, software, physics, and problem-solving.\n"
                "• **PCB (Medicine & Healthcare):** For those passionate about biology, healthcare, clinical research, and saving lives.\n"
                "• **Commerce (Business & Finance):** For those driven by finance, entrepreneurship, stock markets, and accounting (CA/CFA/MBA).\n"
                "• **Arts & Humanities (Law & Public Policy):** For thinkers interested in civil services (UPSC), law (CLAT), psychology, journalism, and creative arts.\n\n"
                "### 2. Take the 15-Question Career Assessment\n"
                "Our built-in **Random Forest ML Recommender** analyzes 15 high-impact dimensions to find your exact top 3 career trajectories.\n\n"
                "### 3. Check Official College Cutoffs\n"
                "Use our JoSAA and NEET college predictors to see which premier institutions match your marks."
            ),
            "suggestions": ["✨ Start 15-Question Assessment", "I like computers & coding", "I like biology & medicine", "I like finance & management"],
            "action": "none",
            "sources": []
        }

    # 6. Fetch live web knowledge for all specific inquiries
    web_results = search_live_web_knowledge(text_clean, limit=3)
    sources = [{"title": r["title"], "url": r["url"]} for r in web_results]

    web_snippet_block = ""
    if web_results:
        top_items = []
        for r in web_results[:2]:
            top_items.append(f"• **{r['title']}**: {r['snippet']}")
        web_snippet_block = "\n\n> 🌐 **Live Web Intelligence:**\n" + "\n".join(f"> {item}" for item in top_items)

    # Contextual career breakdown based on detected domain
    domain_guidance = ""
    if any(k in text_lower for k in ["pilot", "aviation", "flying", "commercial pilot"]):
        domain_guidance = (
            "### Commercial Aviation Career Blueprint:\n"
            "• **Eligibility:** Class 12 with Physics and Mathematics (minimum 50% marks) and Class 1 DGCA Medical Certificate.\n"
            "• **Key Steps:** Student Pilot License (SPL) $\\rightarrow$ Private Pilot License (PPL) $\\rightarrow$ Commercial Pilot License (CPL) with 200 flying hours.\n"
            "• **Premier Academies:** IGRUA (Indira Gandhi Rashtriya Uran Akademi, Amethi), NFTI Gondia, and CAE Oxford.\n"
            "• **Entrance Exam:** IGRUA Entrance Exam (written test + pilot aptitude test + interview)."
        )
    elif any(k in text_lower for k in ["robot", "robotics", "automation", "mechatronics"]):
        domain_guidance = (
            "### Robotics & Mechatronics Engineering Blueprint:\n"
            "• **Academic Stream:** Class 11-12 with Physics, Chemistry, and Mathematics (PCM).\n"
            "• **Degree Pathways:** B.Tech in Robotics & Automation, Mechatronics, or Mechanical / Computer Science with robotics electives.\n"
            "• **Entrance Exams:** JEE Main, JEE Advanced, BITSAT, and state engineering CETs.\n"
            "• **Premier Institutions:** IIT Kanpur, IIT Madras, BITS Pilani, and IIIT Hyderabad."
        )
    elif any(k in text_lower for k in ["data science", "machine learning", "ai", "artificial intelligence"]):
        domain_guidance = (
            "### Artificial Intelligence & Data Science Engineering Blueprint:\n"
            "• **Academic Stream:** Class 11-12 with PCM (strong focus on Mathematics, Linear Algebra, and Statistics).\n"
            "• **Degree Pathways:** B.Tech in Computer Science & Engineering (AI/ML specialization), B.Sc in Data Science (e.g. IIT Madras Online Degree), or Integrated M.Tech Engineering.\n"
            "• **Key Skills:** Python, PyTorch/TensorFlow, SQL, Machine Learning algorithms, and Probability Theory.\n"
            "• **Premier Institutions:** IIT Hyderabad (B.Tech AI), IIT Bombay, IIT Delhi, BITS Pilani, and IIIT Delhi."
        )
    elif any(k in text_lower for k in ["psychology", "mental health", "counseling", "psychiatry"]):
        domain_guidance = (
            "### Psychology & Mental Healthcare Blueprint:\n"
            "• **Academic Stream:** Any stream (Arts, Science, or Commerce); Biology in Class 12 is beneficial for neuropsychology.\n"
            "• **Degree Pathways:** BA / B.Sc in Psychology $\\rightarrow$ MA / M.Sc in Clinical/Counseling Psychology $\\rightarrow$ M.Phil / Psy.D for RCI (Rehabilitation Council of India) licensing.\n"
            "• **Entrance Exams:** CUET-UG (for Central Universities like DU, BHU), Christ University Entrance, and TISS-NET / CUET-PG.\n"
            "• **Premier Institutions:** Lady Shri Ram College (LSR) Delhi, NIMHANS Bengaluru, Christ University, and TISS Mumbai."
        )
    elif any(k in text_lower for k in ["biotech", "biotechnology", "bioinformatics", "genetics"]):
        domain_guidance = (
            "### Biotechnology & Life Sciences Blueprint:\n"
            "• **Academic Stream:** Class 11-12 with PCB or PCMB.\n"
            "• **Degree Pathways:** B.Tech Biotechnology (via JEE Main/State CET) or B.Sc Biotechnology (via CUET-UG) followed by M.Sc/M.Tech and Ph.D.\n"
            "• **Core Applications:** Genetic engineering, biopharmaceuticals, vaccine formulation, and agricultural biotechnology.\n"
            "• **Premier Institutions:** IIT Delhi, IIT Kharagpur, ICT Mumbai, IISc Bengaluru, and JNU New Delhi."
        )
    elif any(k in text_lower for k in ["law", "clat", "judge", "advocate", "lawyer"]):
        domain_guidance = (
            "### Corporate & Constitutional Law Blueprint:\n"
            "• **Academic Stream:** Any stream (Arts, Commerce, or Science) with 45% aggregate in Class 12.\n"
            "• **Entrance Exams:** CLAT-UG (for 24 National Law Universities) and AILET (for NLU Delhi).\n"
            "• **Degree Pathways:** 5-Year Integrated B.A. LL.B. (Hons) or B.B.A. LL.B. (Hons).\n"
            "• **Premier Institutions:** NLSIU Bengaluru, NALSAR Hyderabad, WBNUJS Kolkata, and NLU Delhi."
        )
    elif any(k in text_lower for k in ["ca", "chartered accountant", "accounting", "audit"]):
        domain_guidance = (
            "### Chartered Accountancy (ICAI) Blueprint:\n"
            "• **Eligibility:** Register with ICAI after Class 10/12; open to students from any stream (Commerce is ideal).\n"
            "• **Stages:** CA Foundation (4 papers) $\\rightarrow$ CA Intermediate (6 papers) $\\rightarrow$ 2 Years Practical Articleship $\\rightarrow$ CA Final.\n"
            "• **Key Roles:** Statutory Auditor, Financial Controller, Forensic Auditor, and Chief Financial Officer (CFO)."
        )
    else:
        domain_guidance = (
            "### Academic & Career Guidance:\n"
            "• **Eligibility & Preparation:** Verify specific minimum percentage criteria (typically 50-60%) in Class 12 and relevant subject prerequisites.\n"
            "• **Entrance Examinations:** Target recognized national-level entrance tests (JEE, NEET, CUET-UG, CLAT, etc.) for government and premier tier-1 colleges.\n"
            "• **Institution Selection:** Prioritize institutions with strong NIRF rankings, NAAC A++ accreditation, and proven industry placement track records."
        )

    reply_content = (
        f"Thank you for asking, **{detected_name}**! Here is an in-depth breakdown for **\"{text_clean}\"**:\n\n"
        f"{domain_guidance}"
        f"{web_snippet_block}\n\n"
        "💡 **Next Steps:**\n"
        "To get a mathematically rigorous evaluation of how your personal skills and interests match this and other careers, "
        "take our **15-Question Machine Learning Career Assessment**."
    )

    return {
        "reply": reply_content,
        "sources": sources,
        "suggestions": ["✨ Start 15-Question Assessment", "Tell me about Engineering (PCM)", "Tell me about Medical (PCB)", "Tell me about Commerce & CA"],
        "action": "none"
    }

@router.post("/chat")
async def chat_with_margdarshak(payload: ChatMessageInput) -> Dict[str, Any]:
    """
    Conversational endpoint for Margdarshak AI.
    - If user provides an api_key in payload OR has GEMINI_API_KEY in environment,
      queries Google Gemini 1.5 Flash with live Google Search Grounding.
    - Otherwise seamlessly uses the built-in Margdarshak Live Web AI Engine,
      fetching real-time knowledge and providing comprehensive career blueprints.
    """
    user_msg = payload.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    api_key = (payload.api_key or os.environ.get("GEMINI_API_KEY", "")).strip()
    gemini_data = None
    if api_key:
        gemini_data = await query_gemini_api(user_msg, payload.history or [], api_key)

    if gemini_data:
        action = "start_assessment" if any(w in user_msg.lower() for w in ["start assessment", "take assessment", "quiz", "15 question"]) else "none"
        return {
            "status": "Success",
            "reply": gemini_data["reply"],
            "sources": gemini_data.get("sources", []),
            "suggestions": ["✨ Start 15-Question Assessment", "Tell me about engineering colleges", "Tell me about medical cutoffs"],
            "action": action,
            "source": gemini_data.get("model", "Google Gemini AI (Live Search)")
        }

    # Seamless built-in Live Web AI Engine
    response_data = generate_margdarshak_response(user_msg, payload.history or [], payload.student_name)
    response_data["status"] = "Success"
    response_data["source"] = "Margdarshak Live Web Intelligence"
    return response_data

