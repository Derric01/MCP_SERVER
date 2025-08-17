import os
import time
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions

# -------------------------------
# Setup
# -------------------------------
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s"
)

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("Please set GOOGLE_API_KEY in .env file")
genai.configure(api_key=api_key)

# -------------------------------
# Retry wrapper
# -------------------------------
def get_response_with_retry(model, prompt, max_retries=3):
    """
    Try to call Gemini model with retry logic if quota/rate limit is hit.
    """
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempt {attempt}: Sending prompt -> {prompt[:50]}...")
            response = model.generate_content(prompt)
            return response
        except exceptions.ResourceExhausted as e:
            retry_seconds = 10
            logging.warning(f"Rate limit hit. Retrying in {retry_seconds}s...")
            time.sleep(retry_seconds)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            if attempt == max_retries:
                raise
    return None

# -------------------------------
# Simple file loaders
# -------------------------------
def read_pdf(file_path):
    """Read a PDF file into plain text (basic extraction)."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return ""

def read_csv(file_path):
    """Read a CSV into string (just preview style)."""
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.head().to_string()
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        return ""

# -------------------------------
# Main
# -------------------------------
def main():
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    # Example text input
    text = """
    LangChain makes it easy to build apps powered by large language models (LLMs).
    It helps with chaining prompts, managing memory, and connecting to vector databases like Chroma.
    """
    print("Original text:\n", text)

    # Process queries
    queries = [
        "Explain how AI works in a few words",
        "Summarize the above text in bullet points",
        "What is LangChain used for?"
    ]

    for query in queries:
        try:
            response = get_response_with_retry(model, query)
            if response:
                print(f"\nQuery: {query}")
                print("Response:", response.text.strip())
        except Exception as e:
            print(f"Failed to get response: {e}")

    # Optional: load from files
    pdf_text = read_pdf("example.pdf")
    if pdf_text:
        response = get_response_with_retry(model, f"Summarize this PDF content:\n{pdf_text[:2000]}")
        print("\nPDF Summary:", response.text.strip())

    csv_text = read_csv("example.csv")
    if csv_text:
        response = get_response_with_retry(model, f"Give insights from this CSV data:\n{csv_text}")
        print("\nCSV Insights:", response.text.strip())


if __name__ == "__main__":
    main()
