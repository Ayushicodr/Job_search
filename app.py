import streamlit as st
import requests
import fitz  

st.set_page_config(page_title="📄 Resume & Job Matcher", layout="centered")

st.title("📄 Resume & Job Matcher")

def extract_pdf_text(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def get_text_from_file(file_name) -> str:
    if file_name.type == "application/pdf":
        file_text = extract_pdf_text(file_name)
    else:
        file_text = file_name.read().decode("utf-8")
    return file_text


resume_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
job_file = st.file_uploader("Upload Job Description (PDF/TXT)", type=["pdf", "txt"])

if st.button("🔍 Match Resume with Job Description"):
    if resume_file and job_file:
    
        resume_text = get_text_from_file(resume_file)
     
        job_text = get_text_from_file(job_file)
    

        prompt = f"""
        You are an AI career assistant.
        
        Resume:
        {resume_text}

        Job Description:
        {job_text}

        Please analyze and return:
        1. A **Fit Score** (0-100%) of how well this resume matches the job.
        2. Key strengths (resume areas that align well).
        3. Specific recommendations to improve the resume to better fit the job.
        Format neatly in Markdown.
        """

        try:
            with st.spinner("⏳ Analyzing Resume vs Job Description..."):
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llama3", "prompt": prompt, "stream": False},
                )
                data = response.json()
                output = data.get("response", "⚠️ No response from model.")

           
            st.subheader("📌 Match Analysis")
            st.markdown(output)

           
            st.session_state["resume_match"] = output

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    else:
        st.warning("⚠️ Please upload both Resume and Job Description.")


if "resume_match" in st.session_state:
    st.download_button(
        "💾 Download Match Report",
        st.session_state["resume_match"],
        file_name="resume_match_report.md",
        mime="text/markdown"
    )
