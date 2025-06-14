import streamlit as st
import requests

st.title("📄 AI Resume Parser & Matcher")
st.write("Upload a resume (PDF/DOCX) and a job description (TXT) to get parsed info and a match score.")

resume_file = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_file = st.file_uploader("Job Description (TXT)", type=["txt"])

if st.button("Analyze") and resume_file and jd_file:
    files = {
        "file": (resume_file.name, resume_file, resume_file.type),
        "jd": (jd_file.name, jd_file, jd_file.type)
    }
    response = requests.post("http://127.0.0.1:8000/upload/", files=files)
    if response.status_code == 200:
        result = response.json()
        st.subheader("📌 Parsed Resume Data")
        st.json(result["resume_data"])
        st.success(f"💯 Match Score: {result['match_score'] * 100:.2f}%")
    else:
        st.error("Error analyzing files. Please check the backend.")
