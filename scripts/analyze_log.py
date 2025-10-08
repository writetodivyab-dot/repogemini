import google.generativeai as genai
import sys

# Set your API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # or use os.environ

log_file = sys.argv[1]
output_file = sys.argv[2]

with open(log_file, "r", encoding="utf-8") as f:
    log_content = f.read()

# Use the new chat or text completion API
response = genai.Completion.create(
    model="models/text-bison-001",
    prompt=f"Analyze the following Jenkins build log and suggest possible fixes:\n{log_content}",
    temperature=0.2,
    max_output_tokens=500
)

analysis_text = response.result  # the generated text

# Write the AI analysis to a file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(analysis_text)

print("AI Analysis complete, written to:", output_file)
