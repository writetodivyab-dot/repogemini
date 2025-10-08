import os
import sys
from google import genai
from google.genai import types

# Set your API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)

log_file = sys.argv[1]
output_file = sys.argv[2]

# Read the Jenkins console log
with open(log_file, "r", encoding="utf-8") as f:
    log_content = f.read()

# Prepare the content for analysis
contents = [
    types.Part.from_bytes(
        data=log_content.encode("utf-8"),
        mime_type="text/plain",
    ),
    "Analyze the following Jenkins build log and provide actionable suggestions:",
]

# Generate AI analysis
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=contents,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    ),
)

# Extract and save the analysis
analysis_text = response.text
with open(output_file, "w", encoding="utf-8") as f:
    f.write(analysis_text)

print("AI Analysis complete. Output file:", output_file)
