import requests
from bs4 import BeautifulSoup

# ============================
# GITHUB AUDIT
# ============================

def analyze_github_profile(github_url):
    """
    Audit a GitHub profile for proof-of-work signals:
    - Number of repos
    - Stars / forks
    - Tech stack keywords
    - Activity level
    """

    results = {
        "repos": 0,
        "stars": 0,
        "keywords": [],
        "feedback": []
    }

    try:
        # --- Basic scrape ---
        response = requests.get(github_url)
        if response.status_code != 200:
            results["feedback"].append("❌ Could not access GitHub profile.")
            return results

        soup = BeautifulSoup(response.text, "html.parser")

        # --- Count repositories ---
        repo_tags = soup.find_all("a", {"itemprop": "name codeRepository"})
        results["repos"] = len(repo_tags)

        # --- Extract repo names for keywords ---
        repo_names = [tag.text.strip().lower() for tag in repo_tags]
        keywords = ["sql", "python", "r", "excel", "power bi", "tableau",
                    "machine learning", "ai", "dashboard", "analytics"]
        matched = [kw for kw in keywords if any(kw in repo for repo in repo_names)]
        results["keywords"] = matched

        # --- Feedback ---
        if results["repos"] == 0:
            results["feedback"].append("❌ No public projects found. Add proof-of-work!")
        elif results["repos"] < 3:
            results["feedback"].append("⚠️ Few projects. Add more diverse repos to showcase skills.")
        else:
            results["feedback"].append("✅ Good project count on GitHub.")

        if not matched:
            results["feedback"].append("❌ Projects do not clearly show DA/FinTech skills.")
        else:
            results["feedback"].append("✅ Relevant tools/skills reflected in projects.")

    except Exception as e:
        results["feedback"].append(f"❌ Error analyzing GitHub: {e}")

    return results
