import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("Please set GOOGLE_API_KEY in .env file")

genai.configure(api_key=api_key)

def get_response_with_retry(model, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except exceptions.ResourceExhausted as e:
            if "retry_delay" in str(e):
                # Extract retry delay from error message
                retry_seconds = 10  # default delay
                print(f"\nRate limit hit. Waiting {retry_seconds} seconds before retrying...")
                time.sleep(retry_seconds)
            else:
                print("\nQuota exceeded. Please wait or upgrade your plan.")
                raise
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            raise

# Initialize the model with free version
model = genai.GenerativeModel('models/gemini-2.0-flash')

# Example text
text = """
LangChain makes it easy to build apps powered by large language models (LLMs).
It helps with chaining prompts, managing memory, and connecting to vector databases like Chroma.
"""

print("Original text:")
print(text)

# Process a query
query = "Explain how AI works in a few words"

try:
    response = get_response_with_retry(model, query)
    print("\nQuery:", query)
    print("Response:", response.text)
except Exception as e:
    print(f"Failed to get response after retries: {e}")