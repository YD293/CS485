from openai import OpenAI

# Read API key from file
with open("openai_key.txt") as f:
    api_key = f.read().strip()

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Load a job description from file
with open("job_posts/sample_job.txt") as f:
    job_description = f.read()

# Send to OpenAI to generate resume summary
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful resume assistant."},
        {"role": "user", "content": f"Generate a resume summary and 5 bullet points based on this job description:\n\n{job_description}"}
    ]
)

# Print the AI's response
print("\n=== Generated Resume Section ===\n")
print(response.choices[0].message.content)

