from openai import OpenAI

# Load OpenAI API key
with open("openai_key.txt") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# === User Profile ===
name = input("Your Full Name: ")
email = input("Email (optional): ")
linkedin = input("LinkedIn (optional): ")
education = input("Education: ")

# === Recruiter Info ===
recruiter_name = input("Recruiter's Name: ")
recruiter_title = input("Recruiter's Title: ")
company_name = input("Company Name: ")
company_address = input("Company Address (Street, City, State): ")

# === Skills ===
skills = input("List your skills (comma separated): ")

# === Projects ===
projects_list = []
num_projects = int(input("How many projects do you want to include? "))
for i in range(num_projects):
    pname = input(f"Project {i+1} name: ")
    pdesc = input(f"Project {i+1} description: ")
    projects_list.append(f"{pname}: {pdesc}")

# === Work Experience ===
work_experiences = []
num_jobs = int(input("How many jobs do you want to include? "))
for i in range(num_jobs):
    title = input(f"Job {i+1} Title: ")
    company = input(f"Job {i+1} Company: ")
    time = input(f"Job {i+1} Duration: ")
    desc = input(f"Job {i+1} Description: ")
    work_experiences.append(f"{title} at {company} ({time}): {desc}")

# === Upload Old Resume (Paste manually) ===
print("\nPaste your old resume here if you want us to reuse it. Press ENTER twice when done:")
resume_lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    resume_lines.append(line)
resume_text = "\n".join(resume_lines)

# === Job Description Input ===
print("\nPaste the job description below. Press ENTER twice when done:")
job_lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    job_lines.append(line)
job_description = "\n".join(job_lines)

# === Conditional content handling ===
linkedin_line = f"LinkedIn: {linkedin}" if linkedin.strip() else ""
experience_block = (
    "No work experience yet."
    if len(work_experiences) == 0 and resume_text.strip() == ""
    else "\n".join(work_experiences)
)

# === Prompt Construction ===
prompt = f"""
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
{linkedin_line}
Education: {education}

Projects:
{chr(10).join(projects_list)}

Experience:
{experience_block}

Skills:
{skills}

Old Resume Content (optional):
{resume_text}

### Recruiter Info:
{recruiter_name}
{recruiter_title}
{company_name}
{company_address}

### Job Description:
{job_description}
"""

# === API Call ===
print("\nGenerating cover letter... Please wait...\n")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that writes professional cover letters."},
        {"role": "user", "content": prompt}
    ]
)

result = response.choices[0].message.content

# === Output ===
print("=== Tailored Cover Letter ===\n")
print(result)

# Save to file
with open("cover_letter_output.txt", "w") as f:
    f.write(result)

print("\n✅ Cover letter saved as cover_letter_output.txt")
