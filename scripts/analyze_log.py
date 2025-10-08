import google.generativeai as genai
import sys
import os

# Set API key from environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

log_file = sys.argv[1]
output_file = sys.argv[2]

# Read Jenkins console log
with open(log_file, "r", encoding="utf-8") as f:
    log_content = f.read()

# Create AI analysis using Gemini ChatCompletion
response = genai.ChatCompletion.create(
    model="gemini-2.5-pro",
    messages=[
        {
            "role": "system",
            "content": "You are an expert DevOps assistant. Analyze Jenkins build logs and suggest fixes."
        },
        {
            "role": "user",
            "content": f"Analyze the following Jenkins build log and provide actionable suggestions:\n{log_content}"
        }
    ],
    temperature=0.2,
    max_output_tokens=500
)

# Extract AI-generated text
analysis_text = response.choices[0].message["content"]

# Save the AI analysis
with open(output_file, "w", encoding="utf-8") as f:
    f.write(analysis_text)

print("AI Analysis complete. Output file:", output_file)
