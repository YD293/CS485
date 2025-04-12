# gui.py

import streamlit as st
from openai import OpenAI

# 🔐 Load your OpenAI API key from file
with open("openai_key.txt") as f:
    api_key = f.read().strip()

# 🔗 Initialize OpenAI client
client = OpenAI(api_key=api_key)

# 🔧 Page setup
st.set_page_config(page_title="AI Resume Generator", layout="wide")
st.title("🧠 AI Resume & Cover Letter Generator")
st.write("Enter your personal info and paste a job description. The AI will tailor your resume accordingly.")

# === SIDEBAR: User Profile Input ===
st.sidebar.header("🧑 Your Profile")
name = st.sidebar.text_input("Full Name", placeholder="e.g., Yuxing Deng")
email = st.sidebar.text_input("Email (optional)")
linkedin = st.sidebar.text_input("LinkedIn (optional)")
education = st.sidebar.text_area("Education", "Currently pursuing B.S. in Computer Science at [University]")

skills = st.sidebar.text_area("Skills", "Python, Git, Machine Learning, Logistics, Inventory Management")
projects = st.sidebar.text_area("Projects", "- AI Resume Generator\n- Warehouse Optimization Tool")
experience = st.sidebar.text_area("Work Experience", "- International Logistics Coordinator at Global Freight Inc: Managed shipment tracking and customs paperwork for 30+ international orders weekly.")

# === MAIN PANEL: Job Description Input ===
st.subheader("📄 Job Description")
job_description = st.text_area("Paste the job description here:", height=300)

# === Generate Resume Button ===
if st.button("✨ Generate Tailored Resume"):
    if not job_description.strip():
        st.warning("Please paste a job description first.")
    else:
        # Construct GPT prompt
        prompt = f"""
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

        # 🧠 Call OpenAI API
        with st.spinner("Generating your resume..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI resume writer."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            st.success("✅ Resume generated successfully!")

            # Display the result
            st.markdown("### 📝 Tailored Resume")
            st.text(result)

            # Download button
            st.download_button(
                label="💾 Download as .txt",
                data=result,
                file_name="tailored_resume.txt",
                mime="text/plain"
            )

