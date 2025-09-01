import streamlit as st
import tempfile
import os

from ats_checker import extract_text_from_pdf, analyze_resume
from github_audit import analyze_github_profile

# ============================
# STREAMLIT APP
# ============================
st.set_page_config(page_title="SkiDev ATS Analyzer (Pro)", layout="wide")

st.title("🚀 SkiDev ATS Analyzer (Pro)")
st.write("Premium ATS Resume + GitHub Project Analyzer for Data Analyst / FinTech roles.")

# --- Resume Upload ---
st.header("📂 Upload Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# --- JD Input ---
st.header("📑 Job Description")
jd_text = st.text_area("Paste the Job Description (or leave blank to use default role).")

# --- GitHub Input ---
st.header("🌐 GitHub Profile (Optional)")
github_url = st.text_input("Enter GitHub profile URL (optional):")

# --- Run Analysis Button ---
if st.button("Run ATS Analysis"):
    if not uploaded_file:
        st.error("❌ Please upload a resume PDF.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            resume_path = tmp_file.name

        try:
            # --- Extract text & run ATS ---
            resume_text = extract_text_from_pdf(resume_path)
            score, results, feedback = analyze_resume(resume_text)

            st.subheader("📊 ATS Screening Report")
            st.write(f"**Role:** { 'Custom JD' if jd_text else 'Data Analyst (Default)' }")
            st.write(f"**Final ATS Score:** {score}/100")

            # --- Show matched keywords ---
            st.markdown("### ✅ Matched Keywords")
            for k, v in results.items():
                st.write(f"- **{k}**: {v}")

            # --- Feedback ---
            st.markdown("### ⚠️ Feedback")
            for k, v in feedback.items():
                st.write(f"- {v}")

            # --- GitHub Audit (if provided) ---
            if github_url:
                st.subheader("🌐 GitHub Audit Report")
                gh_results = analyze_github_profile(github_url)
                st.write(f"**Repos found:** {gh_results['repos']}")
                st.write(f"**Relevant Skills:** {gh_results['keywords']}")
                st.markdown("### Feedback")
                for fb in gh_results["feedback"]:
                    st.write(f"- {fb}")

        except Exception as e:
            st.error(f"❌ Error: {e}")

        finally:
            os.remove(resume_path)
