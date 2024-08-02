import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import langchain.prompts as lp
import langchain.chains as lc

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt_template = lp.PromptTemplate(
    input_variables=["text", "jd"],
    template="""
    As an advanced and highly experienced Applicant Tracking System (ATS) with a deep understanding of technology fields including software engineering, data science, data analysis, and big data engineering, your goal is to evaluate the provided resume in comparison to the given job description.

    Given the competitive nature of the job market, please provide a thorough and detailed evaluation, focusing on the following:

    1. **Overall Match Percentage**: Calculate and provide a precise percentage that reflects how well the resume matches the job description.
    2. **Strengths**: Highlight the key strengths of the candidate in relation to the job requirements.
    3. **Weaknesses**: Identify areas where the resume falls short, and specify which job requirements are not met.
    4. **Missing Keywords**: List important keywords or phrases from the job description that are missing from the resume.
    5. **Improvement Suggestions**: Offer specific advice on how the candidate can improve their resume to better match the job description.
    6. **Resources for Skill Development**: Provide recommendations for resources (e.g., online courses, books, certifications) to help the candidate acquire the missing skills.

    Please format your response in markdown.

    **Resume:**
    {text}

    **Job Description:**
    {jd}
    """
)


def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text


st.title("ATS")
st.text("Make your resume ATS friendly")
jd = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        text = input_pdf_text(uploaded_file)
        input_prompt = prompt_template.format(text=text, jd=jd)
        response = get_gemini_response(input_prompt)
        st.markdown(response)
    else:
        st.error("Please upload the resume and enter the job description")
