import re
import fitz  # PyMuPDF

# ============================
# CONFIGURATION
# ============================
CONFIG = {
    "role": "Data Analyst (Premium)",
    "weights": {
        "tools": 25,
        "projects": 25,
        "experience": 15,
        "domain": 10,
        "impact": 10,
        "proof": 15,
    },
    "keywords": {
        "tools": ["sql", "python", "excel", "power bi", "tableau", "pandas", "numpy", "matplotlib", "r", "statistics", "ml"],
        "projects": ["dashboard", "etl", "automation", "analysis", "visualization", "business case", "capstone"],
        "domain": ["fintech", "banking", "payment", "risk", "regulatory", "credit", "financial modeling"],
        "impact": ["kpi", "roi", "metrics", "efficiency", "improved", "decision-making"],
        "proof": ["github", "tableau", "portfolio", "kaggle", "medium"],
    }
}

# ============================
# PDF Extraction
# ============================
def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF (works for resumes)."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text.lower()

# ============================
# Keyword Matching
# ============================
def match_keywords(keywords, text):
    return [kw for kw in keywords if kw.lower() in text]

# ============================
# Resume Analysis
# ============================
def analyze_resume(resume_text, jd_text=""):
    score = 0
    results = {}
    feedback = {}
    roadmap = []

    # Tools
    matched_tools = match_keywords(CONFIG["keywords"]["tools"], resume_text)
    results["tools"] = matched_tools
    if matched_tools:
        score += (len(matched_tools) / len(CONFIG["keywords"]["tools"])) * CONFIG["weights"]["tools"]
    else:
        feedback["tools"] = "❌ Add core tools (SQL, Python, Power BI, Tableau, Excel)."
        roadmap.append("Learn & highlight SQL + Python with real-world use cases.")

    # Projects
    matched_projects = match_keywords(CONFIG["keywords"]["projects"], resume_text)
    results["projects"] = matched_projects
    if matched_projects:
        score += (len(matched_projects) / len(CONFIG["keywords"]["projects"])) * CONFIG["weights"]["projects"]
    else:
        feedback["projects"] = "❌ Add academic/capstone projects (dashboards, automation, data pipelines)."
        roadmap.append("Build a capstone project like sales dashboard or data migration case.")

    # Experience
    exp_match = re.search(r'(\d+)\+?\s*year', resume_text)
    experience = int(exp_match.group(1)) if exp_match else 0
    results["experience_years"] = experience
    if experience >= 2:
        score += CONFIG["weights"]["experience"]
    elif experience >= 1:
        score += CONFIG["weights"]["experience"] * 0.5
        feedback["experience"] = "⚠️ Add more relevant analyst experience."
        roadmap.append("Highlight internships, freelancing or client projects to show experience.")
    else:
        feedback["experience"] = "ℹ️ Fresher profile: Compensate with strong projects & proof-of-work."
        roadmap.append("As a fresher, publish academic projects on GitHub/Tableau.")

    # Domain
    matched_domain = match_keywords(CONFIG["keywords"]["domain"], resume_text)
    results["domain"] = matched_domain
    if matched_domain:
        score += (len(matched_domain) / len(CONFIG["keywords"]["domain"])) * CONFIG["weights"]["domain"]
    else:
        feedback["domain"] = "❌ Emphasize business/FinTech knowledge."
        roadmap.append("Add case studies: risk analysis, payments, or credit scoring.")

    # Impact
    matched_impact = match_keywords(CONFIG["keywords"]["impact"], resume_text)
    results["impact"] = matched_impact
    if matched_impact:
        score += (len(matched_impact) / len(CONFIG["keywords"]["impact"])) * CONFIG["weights"]["impact"]
    else:
        feedback["impact"] = "❌ Add impact terms (KPIs, ROI, decision-making)."
        roadmap.append("Reframe achievements: 'Improved efficiency by X%' or 'Reduced cost by Y%.'")

    # Proof of Work
    matched_proof = match_keywords(CONFIG["keywords"]["proof"], resume_text)
    results["proof"] = matched_proof
    if matched_proof:
        score += CONFIG["weights"]["proof"]
    else:
        feedback["proof"] = "❌ Add proof-of-work links (GitHub, Tableau, Kaggle, portfolio)."
        roadmap.append("Publish projects on GitHub/Tableau and add links to resume.")

    return round(score, 2), results, feedback, roadmap
