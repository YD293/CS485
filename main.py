# main.py

from openai import OpenAI
import os

# Load API key
with open("openai_key.txt") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# === User Profile ===
name = input("Your Full Name: ")
email = input("Email (optional): ")
linkedin = input("LinkedIn (optional): ")
education = input("Education: ")

# === Skills ===
skills = input("List your skills (comma separated): ")

# === Projects ===
projects_list = []
num_projects = int(input("How many projects do you want to add? "))
for i in range(num_projects):
    pname = input(f"Project {i+1} name: ")
    pdesc = input(f"Project {i+1} description: ")
    projects_list.append(f"{pname}: {pdesc}")

# === Work Experience ===
work_experiences = []
num_jobs = int(input("How many work experiences do you want to add? "))
for i in range(num_jobs):
    title = input(f"Job {i+1} Title: ")
    company = input(f"Job {i+1} Company: ")
    time = input(f"Job {i+1} Duration: ")
    desc = input(f"Job {i+1} Description: ")
    work_experiences.append(f"{title} at {company} ({time}): {desc}")

# === Old Resume Upload (Optional) ===
print("\nPaste your old resume content here if you'd like to reuse parts of it. Press ENTER twice when done:")
resume_lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    resume_lines.append(line)
resume_text = "\n".join(resume_lines)

# === Job Description ===
print("\nPaste the job description below. Press ENTER twice when you're done:")
job_lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    job_lines.append(line)
job_description = "\n".join(job_lines)

# === Field Logic ===
linkedin_line = f"LinkedIn: {linkedin}" if linkedin.strip() else ""
experience_block = (
    "No work experience yet."
    if len(work_experiences) == 0 and resume_text.strip() == ""
    else "\n".join(work_experiences)
)

# === Prompt Construction ===
prompt = f"""
You are a helpful AI assistant that creates resumes. Use only the content provided.
Do not fabricate fields like location, graduation dates, or job titles.
If any fields are missing, skip them.

Candidate Profile:
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

Old Resume (for reuse, if applicable):
{resume_text}

Job Description:
{job_description}

Instructions:
Use the old resume only if the user didn’t overwrite a section. If a section is new, replace the old one.
Place 'Skills' at the end. Do not add a 'Summary' section.
"""

# === Generate Resume ===
print("\nGenerating resume... Please wait...\n")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful AI resume writer."},
        {"role": "user", "content": prompt}
    ]
)

result = response.choices[0].message.content

# === Output ===
print("=== Tailored Resume ===\n")
print(result)

# Optional: Save to file
with open("resume_output.txt", "w") as f:
    f.write(result)
print("\n✅ Resume saved as resume_output.txt")
