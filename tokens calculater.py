import fitz
import tiktoken
# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text
def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

PDF_PATH = "cv.pdf"
cv_text = extract_text_from_pdf(PDF_PATH)
print(cv_text)
questions = "\n".join(["What is the candidate's name?", "What are the candidate's key skills?", "What is the candidate's work experience?"])
system_prompt = "You are an AI assistant that extracts information from resumes (CVs) and answers specific questions."
total_tokens = count_tokens(cv_text) + count_tokens(questions) + count_tokens(system_prompt)
print(f"Total estimated tokens: {total_tokens}")
