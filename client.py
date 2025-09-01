import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

try:
    response = model.generate_content("What is coding?")
    print("Jarvis:", response.text)
except Exception as e:
    print("Error communicating with Gemini:", e)
