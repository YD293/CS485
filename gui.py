import streamlit as st
from openai import OpenAI
from streamlit_tags import st_tags
import docx2txt
import pdfplumber
import textwrap

# Load OpenAI API key
with open("openai_key.txt") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# App config
st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="wide")
st.title("AI Resume & Cover Letter Generator")
st.write("Enter your personal info once and use it to generate tailored resumes and cover letters.")

# === Sidebar: Personal Info ===
st.sidebar.header("Your Profile")
name = st.sidebar.text_input("Full Name", placeholder="e.g., Yuxing Deng")
email = st.sidebar.text_input("Email (optional)")
linkedin = st.sidebar.text_input("LinkedIn (optional)")
education = st.sidebar.text_area("Education")
phone = st.sidebar.text_input("Phone Number (optional)")
address = st.sidebar.text_input("Address (optional)")

with st.sidebar:
    st.subheader("🧠 Skills")
    all_skills = st_tags(
        label="Select or Add Your Skills",
        text="Type a skill and press enter",
        value=[],
        suggestions=[
            "Python", "C++", "Java", "SQL", "Machine Learning", "Deep Learning", "Git",
            "Data Analysis", "Linux", "Communication", "Leadership", "Project Management"
        ],
        key="skills_input"
    )

# === Work Experience Section ===
st.sidebar.subheader("💼 Work Experience")
work_experiences = []
num_jobs = st.sidebar.number_input("Number of Work Experiences", min_value=0, max_value=10, step=1, value=1)

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
years = [str(y) for y in range(2000, 2026)]

for i in range(num_jobs):
    with st.sidebar.expander(f"Experience {i+1}"):
        title = st.text_input(f"Job Title {i+1}", key=f"title_{i}")
        company = st.text_input(f"Company {i+1}", key=f"company_{i}")

        # Start and End Date pickers
        start_month = st.selectbox("Start Month", months, key=f"start_month_{i}")
        start_year = st.selectbox("Start Year", years, key=f"start_year_{i}")
        end_month = st.selectbox("End Month", months, key=f"end_month_{i}")
        end_year = st.selectbox("End Year", years, key=f"end_year_{i}")
        duration = f"{start_month} {start_year} – {end_month} {end_year}"

        description = st.text_area(f"Description {i+1}", key=f"desc_{i}")
        work_experiences.append(f"{title} at {company} ({duration}): {description}")


# === Project Experience Section ===
st.sidebar.subheader("Projects")
projects_list = []
num_projects = st.sidebar.number_input("Number of Projects", min_value=0, max_value=10, step=1, value=1)

for i in range(num_projects):
    with st.sidebar.expander(f"Project {i+1}"):
        pname = st.text_input(f"Project Name {i+1}", key=f"pname_{i}")
        pdesc = st.text_area(f"Description {i+1}", key=f"pdesc_{i}")
        projects_list.append(f"{pname}: {pdesc}")

st.sidebar.subheader("📤 Upload Existing Resume (Optional)")
uploaded_resume = st.sidebar.file_uploader("Upload your old resume (.pdf or .docx)", type=["pdf", "docx"])
resume_text = ""

if uploaded_resume is not None:
    if uploaded_resume.type == "application/pdf":
        with pdfplumber.open(uploaded_resume) as pdf:
            resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_resume.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = docx2txt.process(uploaded_resume)
    st.sidebar.success("✅ Resume uploaded and processed.")




# === Tabs: Resume Generator | Cover Letter Generator ===
tab1, tab2 = st.tabs(["📄 Resume Generator", "✉️ Cover Letter Generator"])

# === Resume Generator ===
with tab1:
    st.subheader("📄 Resume Generator")
    job_description = st.text_area("Paste the job description here:", height=300)

    # Uploaded resume content
    resume_text = ""
    if uploaded_resume is not None:
        if uploaded_resume.type == "application/pdf":
            with pdfplumber.open(uploaded_resume) as pdf:
                resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif uploaded_resume.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = docx2txt.process(uploaded_resume)

    # Prepare conditional fields
    linkedin_line = f"LinkedIn: {linkedin}" if linkedin.strip() else ""
    phone_line = f"Phone: {phone}" if phone.strip() else ""
    address_line = f"Address: {address}" if address.strip() else ""
    experience_block = (
        "No work experience yet."
        if len(work_experiences) == 0 and resume_text.strip() == ""
        else "\n".join(work_experiences)
    )

    if "result" not in st.session_state:
        st.session_state.result = ""

    if st.button("✨ Generate Tailored Resume"):
        if not job_description.strip():
            st.warning("Please paste a job description first.")
        else:
            prompt = textwrap.dedent(f"""\
You are a helpful AI assistant that creates resumes. Use only the content provided.
Do not fabricate fields like location, graduation dates, or job titles.
If any fields are missing, skip them.

Candidate Profile:
Name: {name}
Email: {email}
{phone_line}
{address_line}
{linkedin_line}
Education: {education}

Projects:
{chr(10).join(projects_list)}

Experience:
{experience_block}

Skills:
{', '.join(all_skills)}

Old Resume (for reuse, if applicable):
{resume_text}

Job Description:
{job_description}

Instructions:
Use the old resume only if the user didn’t overwrite a section. If phone number or address is provided above, use those values instead of anything in the uploaded resume. Place 'Skills' at the end. Do not add a 'Summary' section.
""")

            with st.spinner("Generating your resume..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI resume writer."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.session_state.result = response.choices[0].message.content
                st.success("✅ Resume generated!")
                st.text(st.session_state.result)
                st.download_button("💾 Download Resume", st.session_state.result, file_name="resume.txt", mime="text/plain")

    # === Feedback for Resume Improvement ===
    if st.session_state.result.strip():
        st.markdown("---")
        st.subheader("📝 Give Feedback to Improve Resume")

        section_choice = st.selectbox("Which section would you like to improve?", 
            ["Skills", "Experience", "Education", "Projects"])

        feedback_comment = st.text_area("What would you like us to improve or change?")

        if st.button("♻️ Regenerate Resume Based on Feedback"):
            if not feedback_comment.strip():
                st.warning("Please write some feedback.")
            else:
                improvement_prompt = f"""
You are a helpful AI assistant that improves resumes.
The user wants to improve the **{section_choice}** section of the following resume.
Here is the original resume:
{st.session_state.result}

User Feedback:
{feedback_comment}

Regenerate a better version of the resume, improving only the {section_choice} section while keeping the rest unchanged.
"""
                with st.spinner("Regenerating..."):
                    improved_response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a resume-enhancing assistant."},
                            {"role": "user", "content": improvement_prompt}
                        ]
                    )
                    improved_resume = improved_response.choices[0].message.content
                    st.success("✅ Resume improved!")
                    st.text(improved_resume)
                    st.download_button("💾 Download Improved Resume", improved_resume, file_name="resume_improved.txt", mime="text/plain")

# === Cover Letter Generator ===
with tab2:
    st.subheader("✉️ Cover Letter Generator")

    st.markdown("#### Recruiter / Company Info")
    recruiter_name = st.text_input("Recruiter's Name", placeholder="e.g., Ms. Meena Nagappan")
    recruiter_title = st.text_input("Recruiter's Title", placeholder="e.g., Recruiting Manager")
    company_name = st.text_input("Company Name", placeholder="e.g., Amazon.com Inc")
    company_address = st.text_area("Company Address", placeholder="e.g., 410 Terry Ave, Seattle, WA")

    st.markdown("#### Job Description")
    job_desc_cl = st.text_area("Paste the job description here:", key="cl_input", height=300)

    # Uploaded resume content
    resume_text = ""
    if uploaded_resume is not None:
        if uploaded_resume.type == "application/pdf":
            with pdfplumber.open(uploaded_resume) as pdf:
                resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif uploaded_resume.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = docx2txt.process(uploaded_resume)

    # Optional fields
    linkedin_line = f"LinkedIn: {linkedin}" if linkedin.strip() else ""
    phone_line = f"Phone: {phone}" if phone.strip() else ""
    address_line = f"Address: {address}" if address.strip() else ""
    experience_block = (
        "No work experience yet."
        if len(work_experiences) == 0 and resume_text.strip() == ""
        else "\n".join(work_experiences)
    )

    if st.button("📬 Generate Cover Letter"):
        if not job_desc_cl.strip():
            st.warning("Please paste a job description.")
        elif not recruiter_name or not company_name:
            st.warning("Please enter at least the recruiter's name and company.")
        else:
            cl_prompt = textwrap.dedent(f"""\
                You are a professional cover letter writer.

                Please generate a formal cover letter using the structure below. Do not invent any fields or information.
                Only use the data provided. Use the old resume content only to supplement gaps in the new input.

                ### Required Format:
                - Header:
                    Candidate's name and contact info
                    Recruiter's name, title, company, address
                    Date
                    RE: Job Title
                - Greeting (Dear [Recruiter Name],)
                - First paragraph: Why the applicant is interested in this job at this company
                - Second paragraph: Prior experience relevant to the role
                - Third paragraph: Passion for company/values and alignment
                - Closing: request for follow-up, formal signature
                - Final line: “Enclosure: Resume”

                ### Candidate Info:
                Name: {name}
                Email: {email}
                {phone_line}
                {address_line}
                {linkedin_line}
                Education: {education}

                Projects:
                {chr(10).join(projects_list)}

                Experience:
                {experience_block}

                Skills:
                {', '.join(all_skills)}

                Old Resume Content (optional):
                {resume_text}

                ### Recruiter Info:
                {recruiter_name}
                {recruiter_title}
                {company_name}
                {company_address}

                ### Job Description:
                {job_desc_cl}

                Instructions:
                If phone number or address is provided above, use them instead of anything found in the uploaded resume.
            """)

            with st.spinner("Generating your cover letter..."):
                cl_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes professional cover letters."},
                        {"role": "user", "content": cl_prompt}
                    ]
                )
                cl_result = cl_response.choices[0].message.content
                st.success("✅ Cover letter generated!")
                st.text(cl_result)
                st.download_button("💾 Download Cover Letter", cl_result, file_name="cover_letter.txt", mime="text/plain")

