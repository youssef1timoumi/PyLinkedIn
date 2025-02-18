import os
import fitz  # PyMuPDF for extracting text
from openai import AzureOpenAI

# -------------------- Step 1: Extract Text from PDF --------------------

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

PDF_PATH = "cv.pdf"
cv_text = extract_text_from_pdf(PDF_PATH)  # Extracted CV text

# -------------------- Step 2: Azure OpenAI Setup --------------------

# Azure OpenAI Credentials
endpoint = "URI"
api_key = "API key"
deployment = "deployment name"  # Use the correct Azure deployment name

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="model version",
)

# -------------------- Step 3: Define Questions --------------------

questions = [
    "Where did this candidate study?",
    "Is he good enough in desktop application development?",
    "Where did the candidate do his internships?"
]

# -------------------- Step 4: Send Request to OpenAI --------------------

chat_prompt = [
    {"role": "system", "content": "You are an AI assistant that extracts information from resumes (CVs) and answers specific questions about the candidate."},
    {"role": "user", "content": f"Here is a CV:\n{cv_text}\n\nAnswer the following questions:\n" + "\n".join(questions)}
]

completion = client.chat.completions.create(
    model=deployment,
    messages=chat_prompt,
    max_tokens="change this based on how much you wanna limit your token (integer)",
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

# -------------------- Step 5: Print Raw AI Response --------------------

raw_ai_response = completion.choices[0].message.content  # Full AI response
print("\n--- RAW AI RESPONSE ---\n")
print(raw_ai_response)
