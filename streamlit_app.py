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
        "experience": 20,
        "domain": 15,
        "proof": 15
    },
    "keywords": {
        "tools": ["sql", "python", "excel", "power bi", "tableau", "r", "pandas", "numpy", "matplotlib"],
        "projects": ["dashboard", "etl", "analysis", "visualization", "automation"],
        "domain": ["banking", "fintech", "risk", "regulatory", "credit", "fraud", "kpi", "metrics"],
        "proof": ["github", "portfolio", "tableau public", "kaggle"]
    }
}

# ============================
# PDF Extractor
# ============================
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text.lower()

# ============================
# Keyword Matcher
# ============================
def match_keywords(keywords, text):
    return [kw for kw in keywords if kw in text]

# ============================
# Resume Analyzer
# ============================
def analyze_resume(resume_text, jd_text=""):
    score = 0
    results = {}
    feedback = {}

    # --- Tools ---
    matched_tools = match_keywords(CONFIG["keywords"]["tools"], resume_text)
    results["tools"] = matched_tools
    score += (len(matched_tools) / len(CONFIG["keywords"]["tools"])) * CONFIG["weights"]["tools"]
    if len(matched_tools) < 4:
        feedback["tools"] = f"❌ Add missing tools like: {', '.join(set(CONFIG['keywords']['tools']) - set(matched_tools))}"

    # --- Projects ---
    matched_projects = match_keywords(CONFIG["keywords"]["projects"], resume_text)
    results["projects"] = matched_projects
    score += (len(matched_projects) / len(CONFIG["keywords"]["projects"])) * CONFIG["weights"]["projects"]
    if not matched_projects:
        feedback["projects"] = "❌ Highlight projects: build dashboards, ETL pipelines, or business analysis reports."

    # --- Experience ---
    exp_match = re.search(r'(\d+)\+?\s*year', resume_text)
    experience = int(exp_match.group(1)) if exp_match else 0
    results["experience_years"] = experience
    if experience >= 2:
        score += CONFIG["weights"]["experience"]
    elif experience >= 1:
        score += CONFIG["weights"]["experience"] * 0.5
        feedback["experience"] = "⚠️ Add more relevant BA/DA experience."
    else:
        feedback["experience"] = "ℹ️ Fresher: Compensate with strong academic projects & proof-of-work."

    # --- Domain Knowledge ---
    matched_domain = match_keywords(CONFIG["keywords"]["domain"], resume_text)
    results["domain"] = matched_domain
    if matched_domain:
        score += (len(matched_domain) / len(CONFIG["keywords"]["domain"])) * CONFIG["weights"]["domain"]
    else:
        feedback["domain"] = "❌ Add FinTech/Banking case studies. Example: fraud detection, credit risk dashboards."

    # --- Proof of Work ---
    matched_proof = match_keywords(CONFIG["keywords"]["proof"], resume_text)
    results["proof"] = matched_proof
    if matched_proof:
        score += CONFIG["weights"]["proof"]
    else:
        feedback["proof"] = "❌ Showcase GitHub repos, Tableau dashboards, or Kaggle case studies."

    # ============================
    # DETAILED IMPROVEMENT PLAN
    # ============================
    improvement_plan = []
    if score < 50:
        improvement_plan.append("⚠️ Major improvements needed to reach industry level.")
        improvement_plan.append("📌 Learn & implement: SQL + Python + Tableau/Power BI.")
        improvement_plan.append("📊 Build at least 2 GitHub projects (e.g., ETL pipeline, interactive dashboard).")
        improvement_plan.append("🚀 Participate in open datasets competitions to showcase applied skills.")
    elif 50 <= score < 70:
        improvement_plan.append("⚠️ Borderline profile – needs stronger proof of work.")
        improvement_plan.append("📌 Add 2 end-to-end projects on GitHub (data cleaning, dashboard, and automation).")
        improvement_plan.append("📊 Example Capstone: Customer segmentation analysis using SQL + Python + BI tool.")
    elif 70 <= score < 80:
        improvement_plan.append("✅ Strong profile – but polish is required to cross premium hiring standards.")
        improvement_plan.append("📌 Include business impact language: 'Improved KPIs by X%', 'Reduced errors by Y%'.")
        improvement_plan.append("🚀 Add one premium capstone: e.g., Credit Risk Analytics, Fraud Detection, KPI Dashboard.")
    else:
        improvement_plan.append("🌟 Excellent! Profile is ready for premium opportunities.")
        improvement_plan.append("📌 Keep updating proof-of-work with advanced case studies and live dashboards.")
        improvement_plan.append("🚀 Join SkiDev masterclasses to maintain industry alignment.")

    return round(score, 2), results, feedback, improvement_plan
