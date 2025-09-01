import re
import fitz  # PyMuPDF

# ============================
# CONFIGURATION
# ============================
CONFIG = {
    "role": "Data Analyst (Default)",
    "weights": {
        "tools": 25,
        "projects": 25,
        "experience": 20,
        "domain": 15,
        "proof_of_work": 15  # GitHub projects / portfolio
    },
    "keywords": {
        "tools": ["sql", "python", "excel", "power bi", "tableau", "r", "pandas", "numpy", "matplotlib"],
        "projects": ["etl", "dashboard", "visualization", "automation", "analytics", "machine learning"],
        "domain": ["fintech", "banking", "payment", "regulatory", "credit", "kpi", "metrics", "roi"]
    }
}

# ============================
# FUNCTIONS
# ============================
def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF using PyMuPDF (works for scanned/text PDFs)."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text.lower()

def match_keywords(keywords, text):
    return [kw for kw in keywords if kw.lower() in text]

def analyze_resume(resume_text):
    """Score resume based on keywords & experience."""
    score = 0
    feedback = {}
    results = {}

    # --- Tools ---
    matched_tools = match_keywords(CONFIG["keywords"]["tools"], resume_text)
    results["tools"] = matched_tools
    if matched_tools:
        score += (len(matched_tools) / len(CONFIG["keywords"]["tools"])) * CONFIG["weights"]["tools"]
    else:
        feedback["tools"] = "❌ Missing core tools like SQL, Python, Tableau, Power BI."

    # --- Projects ---
    matched_projects = match_keywords(CONFIG["keywords"]["projects"], resume_text)
    results["projects"] = matched_projects
    if matched_projects:
        score += (len(matched_projects) / len(CONFIG["keywords"]["projects"])) * CONFIG["weights"]["projects"]
    else:
        feedback["projects"] = "❌ Add relevant projects (dashboards, automation, analytics use cases)."

    # --- Experience ---
    exp_match = re.search(r'(\d+)\+?\s*year', resume_text)
    experience = int(exp_match.group(1)) if exp_match else 0
    results["experience_years"] = experience
    if experience >= 2:
        score += CONFIG["weights"]["experience"]
    elif experience >= 1:
        score += CONFIG["weights"]["experience"] * 0.5
        feedback["experience"] = "⚠️ Add more professional BA/DA experience."
    else:
        feedback["experience"] = "ℹ️ Fresher: Compensate with stronger academic projects & proof-of-work."

    # --- Domain Knowledge ---
    matched_domain = match_keywords(CONFIG["keywords"]["domain"], resume_text)
    results["domain"] = matched_domain
    if matched_domain:
        score += (len(matched_domain) / len(CONFIG["keywords"]["domain"])) * CONFIG["weights"]["domain"]
    else:
        feedback["domain"] = "❌ Emphasize FinTech/Banking/business domain knowledge."

    return round(score, 2), results, feedback
