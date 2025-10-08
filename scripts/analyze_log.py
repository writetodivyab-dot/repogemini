import os
import sys
from google import genai
from google.genai import types

# Set API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)

log_file = sys.argv[1]
output_file = sys.argv[2]

# Read Jenkins console log
with open(log_file, "r", encoding="utf-8") as f:
    log_content = f.read()

# Prepare messages for the AI
messages = [
    {
        "role": "system",
        "content": "You are an expert DevOps assistant. Analyze Jenkins build logs and suggest fixes."
    },
    {
        "role": "user",
        "content": f"Analyze the following Jenkins build log and provide actionable suggestions:\n{log_content}"
    }
]

# Synchronous ChatCompletion call
response = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=messages,
    temperature=0.2,
    max_output_tokens=500
)

# Extract AI-generated text
analysis_text = response.choices[0].message["content"]

# Save AI analysis to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(analysis_text)

print("AI Analysis complete. Output file:", output_file)
