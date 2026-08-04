import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


from utils import extract_text_from_pdf

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

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

try:
     response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

     result = response.text

     st.success("Analysis Complete!")
     st.markdown(result)

except Exception as e:
    st.error(f"Error: {e}")

    st.success("Analysis Complete!")

    st.markdown(result)
