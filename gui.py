# gui.py

import streamlit as st
from openai import OpenAI

# Load OpenAI API key
with open("openai_key.txt") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# App config
st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="wide")
st.title("🧠 AI Resume & Cover Letter Generator")
st.write("Enter your personal info once and use it to generate tailored resumes and cover letters.")

# === Sidebar: Personal Info ===
st.sidebar.header("🧑 Your Profile")
name = st.sidebar.text_input("Full Name", placeholder="e.g., Yuxing Deng")
email = st.sidebar.text_input("Email (optional)")
linkedin = st.sidebar.text_input("LinkedIn (optional)")
education = st.sidebar.text_area("Education", "Currently pursuing B.S. in Computer Science at [University]")

# === Skills with multiselect ===
common_skills = [
    "Python", "C++", "Java", "SQL", "Machine Learning", "Deep Learning", "Git",
    "Data Analysis", "Linux", "Communication", "Leadership", "Project Management"
]
skills = st.sidebar.multiselect("Select Your Skills", common_skills)

# === Work Experience Section ===
st.sidebar.subheader("💼 Work Experience")
work_experiences = []
num_jobs = st.sidebar.number_input("Number of Work Experiences", min_value=0, max_value=10, step=1, value=1)

for i in range(num_jobs):
    with st.sidebar.expander(f"Experience {i+1}"):
        title = st.text_input(f"Job Title {i+1}", key=f"title_{i}")
        company = st.text_input(f"Company {i+1}", key=f"company_{i}")
        time = st.text_input(f"Duration {i+1}", key=f"time_{i}")
        description = st.text_area(f"Description {i+1}", key=f"desc_{i}")
        work_experiences.append(f"{title} at {company} ({time}): {description}")

# === Project Experience Section ===
st.sidebar.subheader("🛠️ Projects")
projects_list = []
num_projects = st.sidebar.number_input("Number of Projects", min_value=0, max_value=10, step=1, value=1)

for i in range(num_projects):
    with st.sidebar.expander(f"Project {i+1}"):
        pname = st.text_input(f"Project Name {i+1}", key=f"pname_{i}")
        pdesc = st.text_area(f"Description {i+1}", key=f"pdesc_{i}")
        projects_list.append(f"{pname}: {pdesc}")

# === Tabs: Resume Generator | Cover Letter Generator ===
tab1, tab2 = st.tabs(["📄 Resume Generator", "✉️ Cover Letter Generator"])

# === Resume Generator ===
with tab1:
    st.subheader("📄 Resume Generator")
    job_description = st.text_area("Paste the job description here:", height=300)

    if st.button("✨ Generate Tailored Resume"):
        if not job_description.strip():
            st.warning("Please paste a job description first.")
        else:
            prompt = f"""
Given the following candidate profile and job description, generate a professional resume.
Highlight the most relevant experience, skills, and projects for the specific job.
Format using clear sections: Summary, Skills, Experience, Education, Projects.

Candidate Profile:
Name: {name}
Email: {email}
LinkedIn: {linkedin}
Education: {education}
Skills: {', '.join(skills)}
Projects:
{chr(10).join(projects_list)}
Experience:
{chr(10).join(work_experiences)}

Job Description:
{job_description}
"""
            with st.spinner("Generating your resume..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI resume writer."},
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.choices[0].message.content
                st.success("✅ Resume generated!")
                st.text(result)
                st.download_button("💾 Download Resume", result, file_name="resume.txt", mime="text/plain")

# === Cover Letter Generator ===
with tab2:
    st.subheader("✉️ Cover Letter Generator")
    job_desc_cl = st.text_area("Paste the job description here:", key="cl_input", height=300)

    if st.button("Generate Cover Letter"):
        if not job_desc_cl.strip():
            st.warning("Please paste a job description first.")
        else:
            cl_prompt = f"""
Given the following candidate profile and job description, write a personalized, professional cover letter.
Use a standard format (greeting, body paragraphs, closing) and tailor the letter to the role.

Candidate Profile:
Name: {name}
Email: {email}
LinkedIn: {linkedin}
Education: {education}
Skills: {', '.join(skills)}
Projects:
{chr(10).join(projects_list)}
Experience:
{chr(10).join(work_experiences)}

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
                st.text(cl_result)
                st.download_button("💾 Download Cover Letter", cl_result, file_name="cover_letter.txt", mime="text/plain")
