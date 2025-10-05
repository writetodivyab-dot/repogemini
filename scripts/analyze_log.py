import os
import sys
import re
from google import genai
from google.genai import types

# Known error patterns
KNOWN_ERRORS = {
    r"ModuleNotFoundError: No module named '(\w+)'": "Missing Python module: {}",
    r"ImportError: cannot import name '(\w+)'": "Import error: {}",
    r"SyntaxError: (.+)": "Syntax error: {}",
    r"Exception: (.+)": "General exception: {}"
}

def analyze_log_with_gemini(log_file, output_file=None):
    # Read log safely (replace invalid characters)
    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
        log_content = f.read()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Analyze the following Jenkins build log. Identify the root cause of failure,
    summarize clearly, and suggest specific fixes:

    {log_content}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )

    analysis = response.text.strip()

    # Detect known issues
    alerts = []
    for pattern, message in KNOWN_ERRORS.items():
        match = re.search(pattern, log_content)
        if match:
            alerts.append(message.format(*match.groups()))

    # Print console output
    print("\033[93m\n=== 🤖 AI Build Log Analysis ===\033[0m\n")
    if alerts:
        print("\033[91m⚠️ Known Issues Detected:\033[0m")
        for alert in alerts:
            print(f"\033[91m- {alert}\033[0m")
        print("\033[91m------------------------------\033[0m")
    print(f"\033[94m{analysis}\033[0m")
    print("\033[93m\n===============================\033[0m\n")

    # Save to file
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            if alerts:
                f.write("Known Issues:\n")
                for alert in alerts:
                    f.write(f"- {alert}\n")
                f.write("\n")
            f.write(analysis)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_log.py <log_file> [output_file]")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    analyze_log_with_gemini(log_file, output_file)
