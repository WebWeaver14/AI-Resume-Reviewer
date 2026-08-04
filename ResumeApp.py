import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from dotenv import load_dotenv
import os

from utils import extract_text_from_pdf

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄"
)

st.title("📄 AI Resume Reviewer")

job_role = st.text_input("Enter Job Role")

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if st.button("Review Resume"):

    if resume is None:
        st.warning("Upload a resume.")
        st.stop()

    if job_role == "":
        st.warning("Enter a job role.")
        st.stop()

    resume_text = extract_text_from_pdf(resume)

    prompt = f"""
You are an expert ATS Resume Reviewer.

Review this resume for the role of:

{job_role}

Resume:

{resume_text}

Return the response in this format:

ATS Score:
/100

Strengths:
- ...

Weaknesses:
- ...

Missing Skills:
- ...

Suggestions:
- ...

Overall Feedback:
...
"""

    with st.spinner("Analyzing Resume..."):

       response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
)

    result = response.text

    st.success("Analysis Complete!")

    st.markdown(result)