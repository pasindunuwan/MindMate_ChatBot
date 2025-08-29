# test_openai.py
import openai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=r"C:\Users\User\Desktop\test_rasa3\.env")

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Test: Generate a simple response."}],
        max_tokens=50
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"OpenAI error: {e}")