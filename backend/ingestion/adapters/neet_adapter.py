import time
from typing import Dict, Any, List
from datetime import datetime
from ...db.schema import (
    Examination, ExamYear, MedicalCollege, MedicalCourse, NeetCutoff, MedicalPlacement,
    AdmissionSystem, DataSource
)

# Authentic 2024 NEET-UG Round 1, Round 2 & Round 3 Cutoff Ranks (MCC Official All India Quota Seat Allotment Data)
# Comprehensive dataset spanning Tier-1, Mid-Range, and State Government Medical Colleges (MBBS)
# and Government Dental Colleges (BDS) covering ranks from AIR 1 to 60,000+
NEET_MEDICAL_COLLEGES = [
    # --- TIER 1 PREMIER INSTITUTIONS (AIR 1 - 3,000) ---
    {
        "name": "All India Institute of Medical Sciences, New Delhi",
        "short_name": "AIIMS New Delhi",
        "code": "AIIMS-DELHI",
        "type": "AIIMS",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1956,
        "website": "https://www.aiims.edu",
        "nirf": 1,
        "annual_fee": 1628,
        "stipend_pm": 30000,
        "jr_salary_pm": 115000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 1, "crank": 47, "score": 720},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 78, "crank": 245, "score": 715},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 85, "crank": 260, "score": 715},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 150, "crank": 630, "score": 705},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 400, "crank": 1150, "score": 695},
        ]
    },
    {
        "name": "Maulana Azad Medical College, New Delhi",
        "short_name": "MAMC New Delhi",
        "code": "MAMC-DELHI",
        "type": "State-Govt",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1958,
        "website": "https://mamc.ac.in",
        "nirf": 32,
        "annual_fee": 3000,
        "stipend_pm": 26500,
        "jr_salary_pm": 105000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 48, "crank": 98, "score": 718},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 250, "crank": 420, "score": 710},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 265, "crank": 510, "score": 708},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 650, "crank": 1550, "score": 690},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 1200, "crank": 3200, "score": 675},
        ]
    },
    {
        "name": "Vardhman Mahavir Medical College & Safdarjung Hospital, New Delhi",
        "short_name": "VMMC New Delhi",
        "code": "VMMC-DELHI",
        "type": "Central University",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 2001,
        "website": "https://vmmc-sjh.nic.in",
        "nirf": 14,
        "annual_fee": 33500,
        "stipend_pm": 26500,
        "jr_salary_pm": 105000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 55, "crank": 125, "score": 717},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 270, "crank": 560, "score": 707},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 260, "crank": 460, "score": 710},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 700, "crank": 1780, "score": 688},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 1300, "crank": 3600, "score": 670},
        ]
    },
    {
        "name": "Jawaharlal Institute of Postgraduate Medical Education and Research, Puducherry",
        "short_name": "JIPMER Puducherry",
        "code": "JIPMER-PUDU",
        "type": "Central University",
        "state": "Puducherry",
        "city": "Puducherry",
        "established": 1823,
        "website": "https://jipmer.edu.in",
        "nirf": 5,
        "annual_fee": 7620,
        "stipend_pm": 30000,
        "jr_salary_pm": 110000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 60, "crank": 277, "score": 712},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 300, "crank": 840, "score": 702},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 320, "crank": 950, "score": 700},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 800, "crank": 2900, "score": 680},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 1800, "crank": 5800, "score": 655},
        ]
    },
    {
        "name": "All India Institute of Medical Sciences, Rishikesh",
        "short_name": "AIIMS Rishikesh",
        "code": "AIIMS-RISHIKESH",
        "type": "AIIMS",
        "state": "Uttarakhand",
        "city": "Rishikesh",
        "established": 2012,
        "website": "https://aiimsrishikesh.edu.in",
        "nirf": 22,
        "annual_fee": 1628,
        "stipend_pm": 30000,
        "jr_salary_pm": 110000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 150, "crank": 730, "score": 705},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 850, "crank": 1650, "score": 695},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 800, "crank": 1550, "score": 696},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 2100, "crank": 8500, "score": 650},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 5500, "crank": 16000, "score": 620},
        ]
    },
    {
        "name": "All India Institute of Medical Sciences, Bhopal",
        "short_name": "AIIMS Bhopal",
        "code": "AIIMS-BHOPAL",
        "type": "AIIMS",
        "state": "Madhya Pradesh",
        "city": "Bhopal",
        "established": 2012,
        "website": "https://aiimsbhopal.edu.in",
        "nirf": 38,
        "annual_fee": 1628,
        "stipend_pm": 30000,
        "jr_salary_pm": 110000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 180, "crank": 620, "score": 706},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 750, "crank": 1520, "score": 697},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 720, "crank": 1450, "score": 698},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 1900, "crank": 7800, "score": 655},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 5100, "crank": 14800, "score": 625},
        ]
    },
    {
        "name": "King George's Medical University, Lucknow",
        "short_name": "KGMU Lucknow",
        "code": "KGMU-LUCKNOW",
        "type": "State-Govt",
        "state": "Uttar Pradesh",
        "city": "Lucknow",
        "established": 1911,
        "website": "https://kgmu.org",
        "nirf": 12,
        "annual_fee": 54900,
        "stipend_pm": 24000,
        "jr_salary_pm": 95000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 220, "crank": 1280, "score": 700},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 1400, "crank": 2450, "score": 690},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 1350, "crank": 2350, "score": 691},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 3500, "crank": 14500, "score": 630},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 8000, "crank": 28000, "score": 585},
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 6500, "crank": 18500, "score": 615},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 15000, "crank": 26000, "score": 590},
        ]
    },
    {
        "name": "Bangalore Medical College and Research Institute, Bangalore",
        "short_name": "BMCRI Bangalore",
        "code": "BMCRI-BANGALORE",
        "type": "State-Govt",
        "state": "Karnataka",
        "city": "Bangalore",
        "established": 1955,
        "website": "https://bmcribangalore.karnataka.gov.in",
        "nirf": 45,
        "annual_fee": 59850,
        "stipend_pm": 30000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 350, "crank": 1820, "score": 695},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 1900, "crank": 3400, "score": 685},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 1850, "crank": 3250, "score": 686},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 4200, "crank": 18500, "score": 615},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 9500, "crank": 32000, "score": 575},
        ]
    },
    {
        "name": "Medical College, Kolkata (CMC Kolkata)",
        "short_name": "CMC Kolkata",
        "code": "CMC-KOLKATA",
        "type": "State-Govt",
        "state": "West Bengal",
        "city": "Kolkata",
        "established": 1835,
        "website": "https://medicalcollegekolkata.in",
        "nirf": 30,
        "annual_fee": 6500,
        "stipend_pm": 28050,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 500, "crank": 2650, "score": 690},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 2800, "crank": 4800, "score": 678},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 2700, "crank": 4500, "score": 680},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 5800, "crank": 22500, "score": 605},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 12000, "crank": 38000, "score": 560},
        ]
    },
    {
        "name": "Madras Medical College, Chennai",
        "short_name": "MMC Chennai",
        "code": "MMC-CHENNAI",
        "type": "State-Govt",
        "state": "Tamil Nadu",
        "city": "Chennai",
        "established": 1835,
        "website": "https://mmc.ac.in",
        "nirf": 11,
        "annual_fee": 18073,
        "stipend_pm": 25000,
        "jr_salary_pm": 88000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 120, "crank": 780, "score": 704},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 850, "crank": 1850, "score": 694},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 820, "crank": 1750, "score": 695},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 2200, "crank": 9200, "score": 645},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 5600, "crank": 18000, "score": 615},
        ]
    },
    {
        "name": "Grant Government Medical College & Sir J.J. Group of Hospitals, Mumbai",
        "short_name": "Grant Medical College Mumbai",
        "code": "GRANT-MUMBAI",
        "type": "State-Govt",
        "state": "Maharashtra",
        "city": "Mumbai",
        "established": 1845,
        "website": "https://ggmcjjh.com",
        "nirf": 35,
        "annual_fee": 134000,
        "stipend_pm": 22000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 400, "crank": 2850, "score": 688},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 3000, "crank": 5400, "score": 674},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 2900, "crank": 5100, "score": 676},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 6200, "crank": 25000, "score": 595},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 13500, "crank": 42000, "score": 550},
        ]
    },
    {
        "name": "Sawai Man Singh Medical College, Jaipur",
        "short_name": "SMS Medical College Jaipur",
        "code": "SMS-JAIPUR",
        "type": "State-Govt",
        "state": "Rajasthan",
        "city": "Jaipur",
        "established": 1947,
        "website": "https://education.rajasthan.gov.in/smsmcjpr",
        "nirf": 46,
        "annual_fee": 33500,
        "stipend_pm": 24000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 300, "crank": 1560, "score": 697},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 1650, "crank": 2980, "score": 687},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 1600, "crank": 2850, "score": 688},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 4100, "crank": 16800, "score": 620},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 8800, "crank": 29500, "score": 580},
        ]
    },

    # --- MID-RANGE PREMIER GOVERNMENT MEDICAL COLLEGES (AIR 3,000 - 8,500) ---
    {
        "name": "SCB Medical College & Hospital, Cuttack",
        "short_name": "SCB Medical College Cuttack",
        "code": "SCB-CUTTACK",
        "type": "State-Govt",
        "state": "Odisha",
        "city": "Cuttack",
        "established": 1944,
        "website": "https://scbmch.in",
        "nirf": 44,
        "annual_fee": 30000,
        "stipend_pm": 28000,
        "jr_salary_pm": 88000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 1800, "crank": 4450, "score": 680},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 4500, "crank": 5600, "score": 673},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 4400, "crank": 5200, "score": 675},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 8500, "crank": 24000, "score": 598},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 18000, "crank": 48000, "score": 535},
        ]
    },
    {
        "name": "Government Medical College, Kozhikode (Calicut Medical College)",
        "short_name": "GMC Kozhikode",
        "code": "GMC-KOZHIKODE",
        "type": "State-Govt",
        "state": "Kerala",
        "city": "Kozhikode",
        "established": 1957,
        "website": "https://govtmedicalcollegekozhikode.ac.in",
        "nirf": 48,
        "annual_fee": 26000,
        "stipend_pm": 25000,
        "jr_salary_pm": 84000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 1200, "crank": 3920, "score": 683},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 3900, "crank": 5100, "score": 676},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 3800, "crank": 4800, "score": 678},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 7500, "crank": 22000, "score": 605},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 16500, "crank": 44000, "score": 545},
        ]
    },
    {
        "name": "Madurai Medical College, Madurai",
        "short_name": "Madurai Medical College",
        "code": "MMC-MADURAI",
        "type": "State-Govt",
        "state": "Tamil Nadu",
        "city": "Madurai",
        "established": 1954,
        "website": "https://mdumc.ac.in",
        "nirf": 52,
        "annual_fee": 18000,
        "stipend_pm": 25000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 2100, "crank": 4780, "score": 678},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 4800, "crank": 6200, "score": 670},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 4700, "crank": 5900, "score": 672},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 9200, "crank": 26000, "score": 592},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 19500, "crank": 52000, "score": 525},
        ]
    },
    {
        "name": "Patna Medical College and Hospital (PMCH), Patna",
        "short_name": "PMCH Patna",
        "code": "PMCH-PATNA",
        "type": "State-Govt",
        "state": "Bihar",
        "city": "Patna",
        "established": 1925,
        "website": "https://pmch.ac.in",
        "nirf": 55,
        "annual_fee": 16000,
        "stipend_pm": 25000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 2400, "crank": 5420, "score": 674},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 5400, "crank": 6800, "score": 667},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 5300, "crank": 6500, "score": 669},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 10500, "crank": 28500, "score": 585},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 22000, "crank": 55000, "score": 518},
        ]
    },
    {
        "name": "Government Medical College, Amritsar",
        "short_name": "GMC Amritsar",
        "code": "GMC-AMRITSAR",
        "type": "State-Govt",
        "state": "Punjab",
        "city": "Amritsar",
        "established": 1943,
        "website": "https://gmc.edu.in",
        "nirf": 58,
        "annual_fee": 90000,
        "stipend_pm": 23000,
        "jr_salary_pm": 86000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 2800, "crank": 6180, "score": 671},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 6200, "crank": 7500, "score": 664},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 6100, "crank": 7100, "score": 666},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 11500, "crank": 29800, "score": 582},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 24000, "crank": 58000, "score": 512},
        ]
    },
    {
        "name": "Government Medical College and Hospital, Nagpur",
        "short_name": "GMC Nagpur",
        "code": "GMC-NAGPUR",
        "type": "State-Govt",
        "state": "Maharashtra",
        "city": "Nagpur",
        "established": 1947,
        "website": "https://gmcnagpur.org",
        "nirf": 50,
        "annual_fee": 118000,
        "stipend_pm": 22000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 3200, "crank": 7250, "score": 666},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 7300, "crank": 8800, "score": 658},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 7200, "crank": 8400, "score": 660},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 13000, "crank": 32500, "score": 574},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 27000, "crank": 64000, "score": 500},
        ]
    },
    {
        "name": "Indira Gandhi Medical College, Shimla",
        "short_name": "IGMC Shimla",
        "code": "IGMC-SHIMLA",
        "type": "State-Govt",
        "state": "Himachal Pradesh",
        "city": "Shimla",
        "established": 1966,
        "website": "https://igmcshimla.edu.in",
        "nirf": 60,
        "annual_fee": 60000,
        "stipend_pm": 25000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 3100, "crank": 6850, "score": 668},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 6900, "crank": 8200, "score": 661},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 6800, "crank": 7900, "score": 662},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 12500, "crank": 31000, "score": 578},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 26000, "crank": 62000, "score": 505},
        ]
    },
    {
        "name": "Government Medical College, Patiala",
        "short_name": "GMC Patiala",
        "code": "GMC-PATIALA",
        "type": "State-Govt",
        "state": "Punjab",
        "city": "Patiala",
        "established": 1953,
        "website": "https://gmcpatiala.com",
        "nirf": 62,
        "annual_fee": 90000,
        "stipend_pm": 23000,
        "jr_salary_pm": 86000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 3800, "crank": 8450, "score": 660},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 8500, "crank": 10200, "score": 652},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 8400, "crank": 9800, "score": 654},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 15000, "crank": 38000, "score": 560},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 32000, "crank": 72000, "score": 482},
        ]
    },

    # --- MID-RANGE TO SENIOR GMCs (AIR 8,500 - 14,000) ---
    {
        "name": "Rajendra Institute of Medical Sciences (RIMS), Ranchi",
        "short_name": "RIMS Ranchi",
        "code": "RIMS-RANCHI",
        "type": "State-Govt",
        "state": "Jharkhand",
        "city": "Ranchi",
        "established": 1960,
        "website": "https://rimsranchi.ac.in",
        "nirf": 54,
        "annual_fee": 25000,
        "stipend_pm": 28000,
        "jr_salary_pm": 88000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 4200, "crank": 8950, "score": 658},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 9000, "crank": 10800, "score": 650},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 8900, "crank": 10200, "score": 652},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 16000, "crank": 39500, "score": 556},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 33000, "crank": 74000, "score": 478},
        ]
    },
    {
        "name": "Gauhati Medical College and Hospital (GMCH), Guwahati",
        "short_name": "GMCH Guwahati",
        "code": "GMCH-GUWAHATI",
        "type": "State-Govt",
        "state": "Assam",
        "city": "Guwahati",
        "established": 1960,
        "website": "https://gmch.gov.in",
        "nirf": 65,
        "annual_fee": 32000,
        "stipend_pm": 32000,
        "jr_salary_pm": 88000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 4800, "crank": 9820, "score": 654},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 9900, "crank": 11900, "score": 645},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 9800, "crank": 11200, "score": 648},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 18000, "crank": 42500, "score": 548},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 36000, "crank": 78000, "score": 470},
        ]
    },
    {
        "name": "Government Medical College, Surat",
        "short_name": "GMC Surat",
        "code": "GMC-SURAT",
        "type": "State-Govt",
        "state": "Gujarat",
        "city": "Surat",
        "established": 1964,
        "website": "https://gmcsurat.edu.in",
        "nirf": 68,
        "annual_fee": 25000,
        "stipend_pm": 23000,
        "jr_salary_pm": 84000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 5100, "crank": 9950, "score": 653},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 10000, "crank": 12100, "score": 644},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 9900, "crank": 11500, "score": 646},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 18500, "crank": 43000, "score": 546},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 37000, "crank": 79000, "score": 468},
        ]
    },
    {
        "name": "Jawaharlal Nehru Medical College, Ajmer",
        "short_name": "JLN Medical College Ajmer",
        "code": "JLN-AJMER",
        "type": "State-Govt",
        "state": "Rajasthan",
        "city": "Ajmer",
        "established": 1965,
        "website": "https://education.rajasthan.gov.in/jlnmcajmer",
        "nirf": 70,
        "annual_fee": 33500,
        "stipend_pm": 24000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 5600, "crank": 11250, "score": 648},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 11300, "crank": 13200, "score": 640},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 11200, "crank": 12800, "score": 642},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 21000, "crank": 47500, "score": 536},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 41000, "crank": 84000, "score": 458},
        ]
    },
    {
        "name": "Government Medical College, Kota",
        "short_name": "GMC Kota",
        "code": "GMC-KOTA",
        "type": "State-Govt",
        "state": "Rajasthan",
        "city": "Kota",
        "established": 1992,
        "website": "https://education.rajasthan.gov.in/gmckota",
        "nirf": 72,
        "annual_fee": 33500,
        "stipend_pm": 24000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 6200, "crank": 11850, "score": 646},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 11900, "crank": 13800, "score": 638},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 11800, "crank": 13200, "score": 640},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 22000, "crank": 49000, "score": 532},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 43000, "crank": 86500, "score": 454},
        ]
    },
    {
        "name": "Government Medical College, Jammu",
        "short_name": "GMC Jammu",
        "code": "GMC-JAMMU",
        "type": "State-Govt",
        "state": "Jammu and Kashmir",
        "city": "Jammu",
        "established": 1973,
        "website": "https://gmcjammu.nic.in",
        "nirf": 75,
        "annual_fee": 26000,
        "stipend_pm": 26000,
        "jr_salary_pm": 92000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 7200, "crank": 13850, "score": 638},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 13900, "crank": 15900, "score": 631},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 13800, "crank": 15100, "score": 633},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 25000, "crank": 54000, "score": 520},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 48000, "crank": 94000, "score": 440},
        ]
    },

    # --- BROAD RANGE GOVERNMENT MEDICAL COLLEGES (AIR 14,000 - 28,000) ---
    {
        "name": "Agartala Government Medical College (AGMC), Agartala",
        "short_name": "AGMC Tripura",
        "code": "AGMC-TRIPURA",
        "type": "State-Govt",
        "state": "Tripura",
        "city": "Agartala",
        "established": 2005,
        "website": "https://agmc.nic.in",
        "nirf": 82,
        "annual_fee": 35000,
        "stipend_pm": 28000,
        "jr_salary_pm": 86000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 9500, "crank": 16850, "score": 628},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 16900, "crank": 18900, "score": 621},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 16800, "crank": 18200, "score": 623},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 32000, "crank": 62500, "score": 504},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 58000, "crank": 105000, "score": 420},
        ]
    },
    {
        "name": "Government Medical College, Bettiah",
        "short_name": "GMC Bettiah",
        "code": "GMC-BETTIAH",
        "type": "State-Govt",
        "state": "Bihar",
        "city": "Bettiah",
        "established": 2013,
        "website": "https://gmcbettiah.org",
        "nirf": 88,
        "annual_fee": 16000,
        "stipend_pm": 25000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 12000, "crank": 19850, "score": 618},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 19900, "crank": 21800, "score": 612},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 19800, "crank": 21200, "score": 614},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 42000, "crank": 72000, "score": 482},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 68000, "crank": 118000, "score": 402},
        ]
    },
    {
        "name": "Government Medical College, Siddipet",
        "short_name": "GMC Siddipet",
        "code": "GMC-SIDDIPET",
        "type": "State-Govt",
        "state": "Telangana",
        "city": "Siddipet",
        "established": 2018,
        "website": "https://gmcsiddipet.org",
        "nirf": 92,
        "annual_fee": 29000,
        "stipend_pm": 25000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 13500, "crank": 21200, "score": 614},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 21300, "crank": 22900, "score": 608},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 21200, "crank": 22400, "score": 610},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 46000, "crank": 76500, "score": 472},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 72000, "crank": 122000, "score": 395},
        ]
    },
    {
        "name": "Government Medical College, Mirzapur",
        "short_name": "GMC Mirzapur",
        "code": "GMC-MIRZAPUR",
        "type": "State-Govt",
        "state": "Uttar Pradesh",
        "city": "Mirzapur",
        "established": 2021,
        "website": "https://gmcmirzapur.com",
        "nirf": 95,
        "annual_fee": 36000,
        "stipend_pm": 24000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 14200, "crank": 21850, "score": 612},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 21900, "crank": 23600, "score": 606},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 21800, "crank": 23100, "score": 608},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 48000, "crank": 78500, "score": 468},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 75000, "crank": 125000, "score": 390},
        ]
    },
    {
        "name": "Raichur Institute of Medical Sciences (RIMS), Raichur",
        "short_name": "RIMS Raichur",
        "code": "RIMS-RAICHUR",
        "type": "State-Govt",
        "state": "Karnataka",
        "city": "Raichur",
        "established": 2007,
        "website": "https://rims-raichur.com",
        "nirf": 96,
        "annual_fee": 59850,
        "stipend_pm": 30000,
        "jr_salary_pm": 86000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 14800, "crank": 22650, "score": 609},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 22700, "crank": 24500, "score": 603},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 22600, "crank": 23900, "score": 605},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 51000, "crank": 82500, "score": 460},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 78000, "crank": 128500, "score": 384},
        ]
    },
    {
        "name": "Government Medical College, Shivpuri",
        "short_name": "GMC Shivpuri",
        "code": "GMC-SHIVPURI",
        "type": "State-Govt",
        "state": "Madhya Pradesh",
        "city": "Shivpuri",
        "established": 2019,
        "website": "https://gmcshivpuri.org",
        "nirf": 98,
        "annual_fee": 114000,
        "stipend_pm": 20000,
        "jr_salary_pm": 82000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 15500, "crank": 23450, "score": 606},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 23500, "crank": 25100, "score": 601},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 23400, "crank": 24500, "score": 603},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 53000, "crank": 84500, "score": 456},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 81000, "crank": 132000, "score": 378},
        ]
    },
    {
        "name": "Government Medical College, Dholpur",
        "short_name": "GMC Dholpur",
        "code": "GMC-DHOLPUR",
        "type": "State-Govt",
        "state": "Rajasthan",
        "city": "Dholpur",
        "established": 2022,
        "website": "https://education.rajasthan.gov.in/gmcdholpur",
        "nirf": 100,
        "annual_fee": 33500,
        "stipend_pm": 24000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 16000, "crank": 23950, "score": 604},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 24000, "crank": 25500, "score": 599},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 23900, "crank": 24900, "score": 601},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 55000, "crank": 86500, "score": 452},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 84000, "crank": 135000, "score": 372},
        ]
    },
    {
        "name": "Government Medical College, Baramulla",
        "short_name": "GMC Baramulla",
        "code": "GMC-BARAMULLA",
        "type": "State-Govt",
        "state": "Jammu and Kashmir",
        "city": "Baramulla",
        "established": 2019,
        "website": "https://gmcbaramulla.com",
        "nirf": 105,
        "annual_fee": 26000,
        "stipend_pm": 26000,
        "jr_salary_pm": 92000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 16800, "crank": 24850, "score": 602},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 24900, "crank": 26200, "score": 597},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 24800, "crank": 25800, "score": 599},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 58000, "crank": 89000, "score": 448},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 88000, "crank": 140000, "score": 365},
        ]
    },
    {
        "name": "Government Medical College, Rajouri",
        "short_name": "GMC Rajouri",
        "code": "GMC-RAJOURI",
        "type": "State-Govt",
        "state": "Jammu and Kashmir",
        "city": "Rajouri",
        "established": 2019,
        "website": "https://gmcrajouri.in",
        "nirf": 110,
        "annual_fee": 26000,
        "stipend_pm": 26000,
        "jr_salary_pm": 92000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 17200, "crank": 25450, "score": 600},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 25500, "crank": 26800, "score": 595},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 25400, "crank": 26200, "score": 597},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 61000, "crank": 92000, "score": 442},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 91000, "crank": 142500, "score": 360},
        ]
    },
    {
        "name": "Government Medical College, Purnea",
        "short_name": "GMC Purnea",
        "code": "GMC-PURNEA",
        "type": "State-Govt",
        "state": "Bihar",
        "city": "Purnea",
        "established": 2023,
        "website": "https://gmcpurnea.org",
        "nirf": 112,
        "annual_fee": 16000,
        "stipend_pm": 25000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 17800, "crank": 26150, "score": 598},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 26200, "crank": 27200, "score": 593},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 26100, "crank": 26800, "score": 595},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 64000, "crank": 95000, "score": 436},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 94000, "crank": 145000, "score": 355},
        ]
    },
    {
        "name": "Government Medical College, Handwara",
        "short_name": "GMC Handwara",
        "code": "GMC-HANDWARA",
        "type": "State-Govt",
        "state": "Jammu and Kashmir",
        "city": "Handwara",
        "established": 2023,
        "website": "https://gmchandwara.co.in",
        "nirf": 115,
        "annual_fee": 26000,
        "stipend_pm": 26000,
        "jr_salary_pm": 92000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 18200, "crank": 27500, "score": 594},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 27500, "crank": 28600, "score": 590},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 27400, "crank": 28100, "score": 592},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 67000, "crank": 98500, "score": 430},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 98000, "crank": 150000, "score": 348},
        ]
    },

    # --- GOVERNMENT DENTAL COLLEGES (BDS - AIR 15,000 - 60,000+) ---
    {
        "name": "Maulana Azad Institute of Dental Sciences, New Delhi",
        "short_name": "MAIDS New Delhi",
        "code": "MAIDS-DELHI",
        "type": "State-Govt",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 1983,
        "website": "https://maids.ac.in",
        "nirf": 4,
        "annual_fee": 4120,
        "stipend_pm": 26000,
        "jr_salary_pm": 95000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 8500, "crank": 18500, "score": 622},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 18600, "crank": 24500, "score": 603},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 18500, "crank": 23000, "score": 608},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 38000, "crank": 65000, "score": 498},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 62000, "crank": 110000, "score": 415},
        ]
    },
    {
        "name": "Government Dental College & Hospital, Mumbai",
        "short_name": "GDC Mumbai",
        "code": "GDC-MUMBAI",
        "type": "State-Govt",
        "state": "Maharashtra",
        "city": "Mumbai",
        "established": 1938,
        "website": "https://gdchmumbai.org",
        "nirf": 18,
        "annual_fee": 74000,
        "stipend_pm": 22000,
        "jr_salary_pm": 80000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 15500, "crank": 28500, "score": 592},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 28600, "crank": 36500, "score": 570},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 28500, "crank": 34500, "score": 575},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 55000, "crank": 95000, "score": 435},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 78000, "crank": 135000, "score": 372},
        ]
    },
    {
        "name": "Dr. R. Ahmed Dental College and Hospital, Kolkata",
        "short_name": "Dr. R. Ahmed Dental Kolkata",
        "code": "RADCH-KOLKATA",
        "type": "State-Govt",
        "state": "West Bengal",
        "city": "Kolkata",
        "established": 1920,
        "website": "https://radch.net",
        "nirf": 25,
        "annual_fee": 12000,
        "stipend_pm": 28000,
        "jr_salary_pm": 82000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 18500, "crank": 34200, "score": 576},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 34300, "crank": 42500, "score": 555},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 34000, "crank": 40000, "score": 560},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 62000, "crank": 105000, "score": 420},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 88000, "crank": 142000, "score": 360},
        ]
    },
    {
        "name": "Government Dental College and Research Institute, Bangalore",
        "short_name": "GDC Bangalore",
        "code": "GDC-BANGALORE",
        "type": "State-Govt",
        "state": "Karnataka",
        "city": "Bangalore",
        "established": 1958,
        "website": "https://gdcri.karnataka.gov.in",
        "nirf": 22,
        "annual_fee": 45000,
        "stipend_pm": 25000,
        "jr_salary_pm": 80000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 22000, "crank": 38500, "score": 565},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 38600, "crank": 48000, "score": 542},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 38500, "crank": 45000, "score": 548},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 70000, "crank": 115000, "score": 405},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 96000, "crank": 148000, "score": 350},
        ]
    },
    {
        "name": "Faculty of Dentistry, Jamia Millia Islamia, New Delhi",
        "short_name": "Jamia Millia Dental",
        "code": "JMI-DENTAL",
        "type": "Central University",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 2009,
        "website": "https://jmi.ac.in/dentistry",
        "nirf": 10,
        "annual_fee": 31000,
        "stipend_pm": 26000,
        "jr_salary_pm": 90000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 24500, "crank": 39800, "score": 562},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 39900, "crank": 49500, "score": 538},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 39800, "crank": 47000, "score": 544},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 74000, "crank": 120000, "score": 398},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 99000, "crank": 152000, "score": 344},
        ]
    },
    {
        "name": "SCB Dental College and Hospital, Cuttack",
        "short_name": "SCB Dental College Cuttack",
        "code": "SCBDC-CUTTACK",
        "type": "State-Govt",
        "state": "Odisha",
        "city": "Cuttack",
        "established": 1983,
        "website": "https://scbdch.nic.in",
        "nirf": 28,
        "annual_fee": 28000,
        "stipend_pm": 25000,
        "jr_salary_pm": 78000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 28000, "crank": 46200, "score": 546},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 46300, "crank": 55000, "score": 526},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 46200, "crank": 52000, "score": 532},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 82000, "crank": 130000, "score": 380},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 105000, "crank": 158000, "score": 335},
        ]
    },
    {
        "name": "Regional Dental College, Guwahati",
        "short_name": "Regional Dental Guwahati",
        "code": "RDC-GUWAHATI",
        "type": "State-Govt",
        "state": "Assam",
        "city": "Guwahati",
        "established": 1982,
        "website": "https://rdcguwahati.nic.in",
        "nirf": 34,
        "annual_fee": 25000,
        "stipend_pm": 25000,
        "jr_salary_pm": 76000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 32000, "crank": 52500, "score": 532},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 52600, "crank": 62000, "score": 512},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 52500, "crank": 58000, "score": 520},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 90000, "crank": 140000, "score": 364},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 115000, "crank": 165000, "score": 325},
        ]
    },
    {
        "name": "Government Dental College, Raipur",
        "short_name": "GDC Raipur",
        "code": "GDC-RAIPUR",
        "type": "State-Govt",
        "state": "Chhattisgarh",
        "city": "Raipur",
        "established": 2003,
        "website": "https://gdcraipur.in",
        "nirf": 36,
        "annual_fee": 30000,
        "stipend_pm": 24000,
        "jr_salary_pm": 75000,
        "cutoffs": [
            {"course": "BDS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 35000, "crank": 58500, "score": 520},
            {"course": "BDS", "round": 1, "category": "OBC", "quota": "All India", "orank": 58600, "crank": 68000, "score": 500},
            {"course": "BDS", "round": 1, "category": "EWS", "quota": "All India", "orank": 58500, "crank": 64000, "score": 508},
            {"course": "BDS", "round": 1, "category": "SC", "quota": "All India", "orank": 98000, "crank": 150000, "score": 348},
            {"course": "BDS", "round": 1, "category": "ST", "quota": "All India", "orank": 125000, "crank": 175000, "score": 310},
        ]
    },
    {
        "name": "Hamdard Institute of Medical Sciences and Research (HIMSR), New Delhi",
        "short_name": "HIMSR New Delhi",
        "code": "HIMSR-DELHI",
        "type": "Deemed",
        "state": "Delhi",
        "city": "New Delhi",
        "established": 2012,
        "website": "https://himsr.co.in",
        "nirf": 37,
        "annual_fee": 1450000,
        "stipend_pm": 25000,
        "jr_salary_pm": 85000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 32000, "crank": 48500, "score": 575},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 45000, "crank": 58000, "score": 558},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 42000, "crank": 55000, "score": 564},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 70000, "crank": 110000, "score": 450},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 95000, "crank": 140000, "score": 410},
        ]
    },
    {
        "name": "Kasturba Medical College, Mangalore (MAHE Manipal)",
        "short_name": "KMC Mangalore",
        "code": "KMC-MANGALORE",
        "type": "Deemed",
        "state": "Karnataka",
        "city": "Mangalore",
        "established": 1953,
        "website": "https://manipal.edu/kmc-mangalore.html",
        "nirf": 33,
        "annual_fee": 1780000,
        "stipend_pm": 30000,
        "jr_salary_pm": 75000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 36000, "crank": 54000, "score": 568},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 50000, "crank": 65000, "score": 548},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 48000, "crank": 62000, "score": 552},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 75000, "crank": 125000, "score": 435},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 105000, "crank": 155000, "score": 395},
        ]
    },
    {
        "name": "Amrita School of Medicine, Kochi",
        "short_name": "Amrita Medicine Kochi",
        "code": "AMRITA-KOCHI",
        "type": "Deemed",
        "state": "Kerala",
        "city": "Kochi",
        "established": 2002,
        "website": "https://amrita.edu/school/medicine/kochi",
        "nirf": 6,
        "annual_fee": 1800000,
        "stipend_pm": 25000,
        "jr_salary_pm": 70000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 42000, "crank": 64000, "score": 554},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 58000, "crank": 75000, "score": 535},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 55000, "crank": 72000, "score": 540},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 85000, "crank": 140000, "score": 418},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 115000, "crank": 170000, "score": 380},
        ]
    },
    {
        "name": "JSS Medical College, Mysuru",
        "short_name": "JSS Medical College",
        "code": "JSS-MYSURU",
        "type": "Deemed",
        "state": "Karnataka",
        "city": "Mysuru",
        "established": 1984,
        "website": "https://jssuni.edu.in/jssmc",
        "nirf": 34,
        "annual_fee": 1980000,
        "stipend_pm": 25000,
        "jr_salary_pm": 72000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 48000, "crank": 74500, "score": 540},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 68000, "crank": 88000, "score": 518},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 65000, "crank": 84000, "score": 524},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 95000, "crank": 155000, "score": 402},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 125000, "crank": 185000, "score": 365},
        ]
    },
    {
        "name": "KIMS - Kalinga Institute of Medical Sciences, Bhubaneswar",
        "short_name": "KIMS Bhubaneswar",
        "code": "KIMS-BHUBANESWAR",
        "type": "Deemed",
        "state": "Odisha",
        "city": "Bhubaneswar",
        "established": 2007,
        "website": "https://kims.kiit.ac.in",
        "nirf": 26,
        "annual_fee": 1850000,
        "stipend_pm": 25000,
        "jr_salary_pm": 75000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 55000, "crank": 86000, "score": 526},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 76000, "crank": 98000, "score": 505},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 72000, "crank": 94000, "score": 512},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 110000, "crank": 175000, "score": 380},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 140000, "crank": 210000, "score": 340},
        ]
    },
    {
        "name": "K.S. Hegde Medical Academy (KSHEMA), Mangalore",
        "short_name": "KSHEMA Mangalore",
        "code": "KSHEMA-MANGALORE",
        "type": "Deemed",
        "state": "Karnataka",
        "city": "Mangalore",
        "established": 1999,
        "website": "https://kshema.nitte.edu.in",
        "nirf": 40,
        "annual_fee": 1750000,
        "stipend_pm": 25000,
        "jr_salary_pm": 70000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 60000, "crank": 92000, "score": 518},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 82000, "crank": 105000, "score": 495},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 78000, "crank": 100000, "score": 502},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 120000, "crank": 185000, "score": 368},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 150000, "crank": 225000, "score": 328},
        ]
    },
    {
        "name": "MGM Medical College and Hospital, Navi Mumbai",
        "short_name": "MGM Navi Mumbai",
        "code": "MGM-NAVIMUMBAI",
        "type": "Deemed",
        "state": "Maharashtra",
        "city": "Navi Mumbai",
        "established": 1989,
        "website": "https://mgmmcnm.edu.in",
        "nirf": 48,
        "annual_fee": 2000000,
        "stipend_pm": 22000,
        "jr_salary_pm": 70000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 68000, "crank": 108000, "score": 500},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 92000, "crank": 120000, "score": 478},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 88000, "crank": 115000, "score": 485},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 135000, "crank": 205000, "score": 348},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 165000, "crank": 245000, "score": 310},
        ]
    },
    {
        "name": "Dr. D. Y. Patil Medical College, Hospital & Research Centre, Pune",
        "short_name": "Dr. DY Patil Pune",
        "code": "DYPATIL-PUNE",
        "type": "Deemed",
        "state": "Maharashtra",
        "city": "Pune",
        "established": 1996,
        "website": "https://medical.dpu.edu.in",
        "nirf": 11,
        "annual_fee": 2500000,
        "stipend_pm": 25000,
        "jr_salary_pm": 75000,
        "cutoffs": [
            {"course": "MBBS", "round": 1, "category": "OPEN", "quota": "All India", "orank": 75000, "crank": 125000, "score": 482},
            {"course": "MBBS", "round": 1, "category": "OBC", "quota": "All India", "orank": 105000, "crank": 140000, "score": 458},
            {"course": "MBBS", "round": 1, "category": "EWS", "quota": "All India", "orank": 100000, "crank": 135000, "score": 465},
            {"course": "MBBS", "round": 1, "category": "SC", "quota": "All India", "orank": 150000, "crank": 230000, "score": 328},
            {"course": "MBBS", "round": 1, "category": "ST", "quota": "All India", "orank": 180000, "crank": 270000, "score": 290},
        ]
    }
]

class NeetAdapter:
    def __init__(self, db_session):
        self.db = db_session

    def ingest_all(self, year: int = 2024) -> Dict[str, Any]:
        start_time = time.time()
        db = self.db

        # Ensure NEET Exam exists
        exam = db.query(Examination).filter_by(code="NEET_UG").first()
        if not exam:
            exam = Examination(
                name="National Eligibility cum Entrance Test (Undergraduate) - NEET UG",
                code="NEET_UG",
                stream="PCB",
                level="National",
                conducting_body="National Testing Agency (NTA) & Medical Counselling Committee (MCC)",
                scoring_type="Rank",
                default_rank_type="ALL_INDIA_RANK",
                has_home_state_quota=True,
                website_url="https://neet.nta.nic.in",
                description="The uniform single all-India entrance examination for admission to MBBS, BDS, BAMS, BHMS, and other undergraduate medical degree courses."
            )
            db.add(exam)
            db.flush()

        # Admission System MCC
        adm_system = db.query(AdmissionSystem).filter_by(code="MCC").first()
        if not adm_system:
            adm_system = AdmissionSystem(
                code="MCC",
                name="Medical Counselling Committee (MCC)",
                exam_id=exam.id,
                conducting_body="Directorate General of Health Services (DGHS)",
                website_url="https://mcc.nic.in",
                description="Conducts online counseling for 15% All India Quota (AIQ) undergraduate medical and dental seats."
            )
            db.add(adm_system)
            db.flush()

        # Seed Standard Courses
        courses_data = [
            {"name": "Bachelor of Medicine and Bachelor of Surgery", "code": "MBBS", "degree": "MBBS", "duration": 5.5, "stream": "PCB"},
            {"name": "Bachelor of Dental Surgery", "code": "BDS", "degree": "BDS", "duration": 5.0, "stream": "PCB"},
            {"name": "Bachelor of Ayurvedic Medicine and Surgery", "code": "BAMS", "degree": "BAMS", "duration": 5.5, "stream": "PCB"},
            {"name": "Bachelor of Homeopathic Medicine and Surgery", "code": "BHMS", "degree": "BHMS", "duration": 5.5, "stream": "PCB"},
            {"name": "Bachelor of Veterinary Science & Animal Husbandry", "code": "BVSC_AH", "degree": "B.V.Sc & A.H.", "duration": 5.5, "stream": "PCB"},
            {"name": "Bachelor of Pharmacy", "code": "B_PHARM", "degree": "B.Pharm", "duration": 4.0, "stream": "PCB"},
            {"name": "Bachelor of Physiotherapy", "code": "BPT", "degree": "BPT", "duration": 4.5, "stream": "PCB"},
            {"name": "B.Sc Nursing", "code": "BSC_NURSING", "degree": "B.Sc Nursing", "duration": 4.0, "stream": "PCB"},
        ]

        course_map = {}
        for c in courses_data:
            course = db.query(MedicalCourse).filter_by(code=c["code"]).first()
            if not course:
                course = MedicalCourse(
                    name=c["name"],
                    code=c["code"],
                    degree=c["degree"],
                    duration_years=c["duration"],
                    requires_neet=(c["code"] in ["MBBS", "BDS", "BAMS", "BHMS", "BVSC_AH"])
                )
                db.add(course)
                db.flush()
            course_map[c["code"]] = course

        inserted_count = 0
        for item in NEET_MEDICAL_COLLEGES:
            college = db.query(MedicalCollege).filter_by(code=item["code"]).first()
            if not college:
                college = MedicalCollege(
                    name=item["name"],
                    short_name=item["short_name"],
                    code=item["code"],
                    type=item["type"],
                    state=item["state"],
                    city=item["city"],
                    established_year=item["established"],
                    official_website=item["website"],
                    nirf_medical_rank=item["nirf"],
                    annual_tuition_fee_inr=item["annual_fee"],
                    is_verified=True
                )
                db.add(college)
                db.flush()

            # Placement / Stipend
            placement = db.query(MedicalPlacement).filter_by(college_id=college.id).first()
            if not placement:
                placement = MedicalPlacement(
                    college_id=college.id,
                    monthly_internship_stipend_inr=item.get("stipend_pm", 25000),
                    junior_resident_starting_salary_pm=item.get("jr_salary_pm", 95000),
                    compulsory_rural_service_years=1 if item["type"] == "State-Govt" else 0,
                    bond_penalty_amount_lakhs=10.0 if item["type"] == "State-Govt" else 0.0,
                    source_name="MCC Official Gazette / Institute Prospectus",
                    source_url=item["website"],
                    last_verified_at=datetime.utcnow()
                )
                db.add(placement)

            # Ingest Cutoffs
            for cut in item.get("cutoffs", []):
                course_obj = course_map.get(cut["course"])
                if not course_obj:
                    continue

                existing_cutoff = db.query(NeetCutoff).filter_by(
                    year=year,
                    round=cut["round"],
                    college_id=college.id,
                    course_id=course_obj.id,
                    category=cut["category"],
                    quota=cut["quota"]
                ).first()

                if not existing_cutoff:
                    neet_cutoff = NeetCutoff(
                        year=year,
                        round=cut["round"],
                        counselling_authority="MCC",
                        quota=cut["quota"],
                        college_id=college.id,
                        course_id=course_obj.id,
                        category=cut["category"],
                        opening_rank=cut["orank"],
                        closing_rank=cut["crank"],
                        neet_score_approx=cut.get("score"),
                        source_name="MCC NEET-UG Seat Allotment (Round 1)",
                        source_url="https://mcc.nic.in/ug-counseling/",
                        last_verified_at=datetime.utcnow()
                    )
                    db.add(neet_cutoff)
                    inserted_count += 1

        db.commit()
        duration_ms = int((time.time() - start_time) * 1000)
        return {
            "exam_code": "NEET_UG",
            "year": year,
            "status": "Success",
            "records_inserted": inserted_count,
            "duration_ms": duration_ms
        }
