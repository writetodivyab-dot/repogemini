import sys
import os
import google.generativeai as genai

def analyze_log(log_content, output_file_path):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables.")

    genai.configure(api_key=api_key)

    prompt = f"""
    You are an AI assistant. Analyze the following Jenkins build log and summarize:
    - Errors encountered
    - Possible causes
    - Suggested fixes

    Build log:
    {log_content}
    """

    response = genai.chat.create(
        model="gemini-1.5",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_analysis = response.last.user_message.content

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(ai_analysis)

    print("\033[93m\n=== 🤖 AI Build Log Analysis ===\033[0m\n")
    print(ai_analysis)


if __name__ == "__main__":
    # If file is provided, read it; else read from stdin
    if len(sys.argv) == 2:
        output_file = sys.argv[1]
        log_content = sys.stdin.read()
    elif len(sys.argv) == 3:
        log_file = sys.argv[1]
        output_file = sys.argv[2]
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            log_content = f.read()
    else:
        print("Usage:")
        print("  echo <log> | python analyze_log.py <output_file>")
        print("  python analyze_log.py <log_file> <output_file>")
        sys.exit(1)

    analyze_log(log_content, output_file)
