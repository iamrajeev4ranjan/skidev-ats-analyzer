import streamlit as st
import re
from ats_checker import analyze_resume, extract_text_from_pdf
from github_audit import analyze_github_profile

st.set_page_config(page_title="SkiDev ATS Analyzer", page_icon="🚀", layout="wide")

st.title("🚀 SkiDev ATS Analyzer (Pro)")
st.write("Upload your resume, paste a Job Description (optional), and get a premium ATS-style analysis + improvement roadmap.")

# === Resume Upload ===
uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type="pdf")

# === JD Input ===
jd_text = st.text_area("📑 Paste Job Description (or leave blank for default Data Analyst role)", height=200)

# === GitHub Input (optional override) ===
github_url = st.text_input("🌐 Paste your GitHub profile link (leave blank if in resume):")

if uploaded_file:
    # Save resume temp
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Extract text
    resume_text = extract_text_from_pdf("temp_resume.pdf")

    # Run ATS
    score, results, feedback, roadmap = analyze_resume(resume_text, jd_text)

    # --- Show Report ---
    st.subheader("📊 ATS Score")
    st.metric("Final Score", f"{score}/100")

    st.subheader("✅ Matched Keywords")
    st.json(results)

    st.subheader("⚠️ Feedback")
    for fb in feedback.values():
        st.write(f"- {fb}")

    st.subheader("🚀 Improvement Roadmap")
    for step in roadmap:
        st.write(f"- {step}")

    # --- GitHub Audit ---
    if github_url:
        st.subheader("🌐 GitHub Audit Report")
        gh_results = analyze_github_profile(github_url)
        st.write(f"**Repos found:** {gh_results['repos']}")
        st.write(f"**Relevant Skills:** {gh_results['keywords']}")
        st.markdown("### Feedback")
        for fb in gh_results["feedback"]:
            st.write(f"- {fb}")

    elif 'github.com' in resume_text:
        github_found = re.findall(r'(https?://github\.com/[^\s]+)', resume_text)
        if github_found:
            auto_github = github_found[0]
            st.subheader("🌐 GitHub Audit Report (Auto-Detected)")
            st.info(f"Detected from resume: {auto_github}")
            gh_results = analyze_github_profile(auto_github)
            st.write(f"**Repos found:** {gh_results['repos']}")
            st.write(f"**Relevant Skills:** {gh_results['keywords']}")
            st.markdown("### Feedback")
            for fb in gh_results["feedback"]:
                st.write(f"- {fb}")
    else:
        st.markdown("ℹ️ No GitHub profile detected in resume.")
