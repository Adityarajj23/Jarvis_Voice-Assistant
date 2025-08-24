import google.generativeai as genai

genai.configure(api_key="API key")  # Replace with your actual API key

model = genai.GenerativeModel('models/gemini-2.5-flash')  # or 'gemini-1.5-flash' if you want

# models = genai.list_models()

# Print only text-capable models
# for m in models:
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)

def ask_gemini(question: str) -> str:
    """
    Send a question to Gemini and return the response text.
    """
    try:
        response = model.generate_content(question)
        return response.text.strip() if response.text else "Sorry, I didn’t get any response."
    except Exception as e:

        return f"Error while contacting Gemini: {e}"
