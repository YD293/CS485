import streamlit as st
from openai import OpenAI

# Load OpenAI API key
with open("openai_key.txt") as f:
    api_key = f.read().strip()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Page setup
st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="wide")
st.title("🧠 AI Resume & Cover Letter Generator")
st.write("Enter your personal info once and use it to generate tailored resumes and cover letters.")

# === SIDEBAR: User Profile Input ===
st.sidebar.header("🧑 Your Profile")
name = st.sidebar.text_input("Full Name", placeholder="e.g., Yuxing Deng")
email = st.sidebar.text_input("Email (optional)")
linkedin = st.sidebar.text_input("LinkedIn (optional)")
education = st.sidebar.text_area("Education", "Currently pursuing B.S. in Computer Science at [University]")
skills = st.sidebar.text_area("Skills", "Python, Git, Machine Learning, Logistics, Inventory Management")
projects = st.sidebar.text_area("Projects", "- AI Resume Generator\n- Warehouse Optimization Tool")
experience = st.sidebar.text_area("Work Experience", "- International Logistics Coordinator at Global Freight Inc: Managed shipment tracking and customs paperwork for 30+ international orders weekly.")

# === TABS: Resume Generator | Cover Letter Generator ===
tab1, tab2 = st.tabs(["📄 Resume Generator", "✉️ Cover Letter Generator"])

# === TAB 1: Resume Generator ===
with tab1:
    st.subheader("📄 Resume Generator")
    st.write("Paste a job description below and generate a tailored resume.")

    job_description = st.text_area("Paste the job description here:", height=300)

    if st.button("✨ Generate Tailored Resume"):
        if not job_description.strip():
            st.warning("Please paste a job description first.")
        else:
            # Prompt for resume
            resume_prompt = f"""
Given the following candidate profile and job description, generate a professional resume.
Highlight the most relevant experience, skills, and projects for the specific job.
Format using clear sections: Summary, Skills, Experience, Education, Projects.

Candidate Profile:
Name: {name}
Email: {email}
LinkedIn: {linkedin}
Education: {education}
Skills: {skills}
Projects:
{projects}
Experience:
{experience}

Job Description:
{job_description}
"""
            with st.spinner("Generating your resume..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI resume writer."},
                        {"role": "user", "content": resume_prompt}
                    ]
                )
                result = response.choices[0].message.content
                st.success("✅ Resume generated successfully!")

                st.markdown("### 📝 Tailored Resume")
                st.text(result)

                st.download_button(
                    label="💾 Download as .txt",
                    data=result,
                    file_name="tailored_resume.txt",
                    mime="text/plain"
                )

# === TAB 2: Cover Letter Generator ===
with tab2:
    st.subheader("✉️ Cover Letter Generator")
    st.write("Use your profile and job description to auto-generate a professional cover letter.")

    job_desc_cl = st.text_area("📄 Paste the job description here:", key="cl_input", height=300)

    if st.button("Generate Cover Letter"):
        if not job_desc_cl.strip():
            st.warning("Please paste a job description first.")
        else:
            # Prompt for cover letter
            cl_prompt = f"""
Given the following candidate profile and job description, write a personalized, professional cover letter.
Use a standard format (greeting, body paragraphs, closing) and tailor the letter to the role.

Candidate:
Name: {name}
Email: {email}
LinkedIn: {linkedin}
Education: {education}
Skills: {skills}
Projects:
{projects}
Experience:
{experience}

Job Description:
{job_desc_cl}
"""
            with st.spinner("Generating your cover letter..."):
                cl_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful career assistant that writes professional cover letters."},
                        {"role": "user", "content": cl_prompt}
                    ]
                )
                cl_result = cl_response.choices[0].message.content
                st.success("✅ Cover letter generated!")

                st.markdown("### ✉️ Cover Letter Output")
                st.text(cl_result)

                st.download_button(
                    label="💾 Download as .txt",
                    data=cl_result,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )
