import sys
import os
import google.generativeai as genai

def analyze_log_with_gemini(log_file_path, output_file_path):
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables.")

    genai.configure(api_key=api_key)

    # Read the Jenkins build log
    with open(log_file_path, "r", encoding="utf-8", errors="ignore") as f:
        log_content = f.read()

    # Prepare prompt for Gemini
    prompt = f"""
    You are an AI assistant. Analyze the following Jenkins build log and summarize:
    - Errors encountered
    - Possible causes
    - Suggested fixes

    Build log:
    {log_content}
    """

    # Call Gemini API
    response = genai.chat.create(
        model="gemini-1.5",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_analysis = response.last.user_message.content

    # Write AI analysis to output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(ai_analysis)

    print("\033[93m\n=== 🤖 AI Build Log Analysis ===\033[0m\n")
    print(ai_analysis)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze_log.py <log_file> <output_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2]

    analyze_log_with_gemini(log_file, output_file)
