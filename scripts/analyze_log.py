#!/opt/venv/bin/python3
import os
import sys
import requests
import google.generativeai as genai

# ---------------------------------------------------------------------------
# 1️⃣  Validate inputs
# ---------------------------------------------------------------------------
if len(sys.argv) < 2:
    print("Usage: analyze_log.py <log_file_path>")
    sys.exit(1)

log_path = sys.argv[1]
if not os.path.exists(log_path):
    print(f"Log file not found: {log_path}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 2️⃣  Read build log
# ---------------------------------------------------------------------------
with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    build_log = f.read()

# ---------------------------------------------------------------------------
# 3️⃣  Configure Gemini client
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not set.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# ---------------------------------------------------------------------------
# 4️⃣  Generate analysis using Gemini
# ---------------------------------------------------------------------------
prompt = f"""
Analyze this Jenkins build log for errors and suggest potential fixes.
Keep it short and structured in Markdown with sections:
- Root Cause
- Possible Fix
- File or Module (if any)
- Confidence (High/Medium/Low)
- Next Steps

Build log:
{build_log[:15000]}  # truncated for safety
"""

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    analysis_text = response.text.strip() if response and response.text else "No response from Gemini."
except Exception as e:
    analysis_text = f"Error during Gemini API call: {str(e)}"

# ---------------------------------------------------------------------------
# 5️⃣  Decide posting target: PR or local log
# ---------------------------------------------------------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER", "").strip()
REPO_NAME = os.getenv("REPO_NAME", "").strip()

if PR_NUMBER and GITHUB_TOKEN and REPO_NAME:
    # ✅ Running for a Pull Request build
    print(f"Posting AI analysis to PR #{PR_NUMBER} in {REPO_NAME}...")
    try:
        url = f"https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        payload = {"body": f"🤖 **Gemini Build Log Analysis**\n\n{analysis_text}"}
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()
        print("✅ Successfully posted AI analysis to PR.")
    except Exception as e:
        print(f"⚠️ Failed to post PR comment: {e}")
        print("Falling back to local log.")
        print("\n---- AI Analysis ----\n")
        print(analysis_text)
else:
    # ✅ Manual build — just print to console
    print("No PR context detected — printing analysis to console.\n")
    print("---- AI Build Log Analysis ----\n")
    print(analysis_text)
