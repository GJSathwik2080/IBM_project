import streamlit as st
import pdfplumber
import pandas as pd
import re
from collections import defaultdict

# Streamlit UI
st.set_page_config(page_title="Resume Classifier", layout="wide")
st.title("📄 Resume Screening Assistant")
st.caption("Classify resumes into job roles using local keyword matching")

# Define job categories and keywords
job_keywords = {
    "Data Science": ["machine learning", "data analysis", "pandas", "numpy", "statistics", "python"],
    "Software Development": ["java", "c++", "git", "react", "node", "javascript", "software engineer"],
    "Human Resources (HR)": ["recruiting", "talent acquisition", "hr", "human resources", "onboarding", "training"],
    "Marketing": ["seo", "campaign", "brand", "marketing", "social media", "adwords"],
    "Finance": ["accounting", "finance", "financial analysis", "budget", "investment", "auditing"]
}

def classify_resume(text):
    text = text.lower()
    scores = defaultdict(int)
    for category, keywords in job_keywords.items():
        for keyword in keywords:
            if keyword in text:
                scores[category] += 1

    if not scores:
        return "Other"
    
    return max(scores, key=scores.get)

# Upload resumes
uploaded_files = st.file_uploader("Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("🚀 Classify Resumes") and uploaded_files:
    results = []

    for file in uploaded_files:
        try:
            with pdfplumber.open(file) as pdf:
                text = "\n".join(
                    page.extract_text() or "" for page in pdf.pages
                ).strip()
        except Exception as e:
            results.append({
                "File Name": file.name,
                "Predicted Category": f"Error reading file: {e}"
            })
            continue

        if not text:
            category = "No text found"
        else:
            category = classify_resume(text)

        results.append({
            "File Name": file.name,
            "Predicted Category": category
        })

    # Show results
    df = pd.DataFrame(results)
    st.success("✅ Classification Complete")
    st.dataframe(df)

    # CSV download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV Report", data=csv, file_name="resume_classification_report.csv", mime="text/csv")
