# main.py

from openai import OpenAI

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

# === Job Description ===
print("\nPaste the job description below. Press ENTER twice when you're done:")
job_lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    job_lines.append(line)
job_description = "\n".join(job_lines)

# === Prompt Construction ===
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
{chr(10).join(projects_list)}
Experience:
{chr(10).join(work_experiences)}

Job Description:
{job_description}
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
