import json
import requests
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extracts all text from the given PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def ask_questions_about_book(book_text, max_prompt_length=2000):
    """
    Constructs a prompt with the book text (truncated if necessary)
    and calls the local LLM API on Ollama to generate questions about the book.
    """
    # Truncate the text if it's too long for the prompt.
    truncated_text = book_text[:max_prompt_length]
    
    # Construct the prompt for the LLM.
    prompt = (
        "You are an insightful literature teacher. "
        "Based on the following excerpt from a book, please generate several thoughtful, "
        "open-ended questions that could help a reader reflect on and understand the content better:\n\n"
        f"{truncated_text}\n\nQuestions:"
    )

    # Define the API endpoint and payload.
    # Adjust the URL and payload parameters based on your Ollama API documentation.
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "prompt": prompt,
        "max_tokens": 150,      # Adjust based on how long you expect the output to be.
        "temperature": 0.7,     # Creativity of the LLM output.
        "model": "llama2",      # Replace with the actual model name.
        "stream": False         # Set to True for long-running generation tasks.
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        # Assuming the API returns a JSON with a key like "response" or "text"
        result: dict = response.json()
        # Check for different response key names based on your API.
        output = result.get("response") or result.get("text")
        return output if output else "No questions returned by the LLM."
    except requests.exceptions.RequestException as e:
        return f"Error during API call: {e}"

if __name__ == "__main__":
    # Path to the PDF file of the book.
    pdf_path = "/Users/luqmaan/personal/paper.pdf"  # <-- Replace with your PDF file path.

    # Step 1: Extract the book text.
    print("Extracting text from the PDF...")
    book_text = extract_text_from_pdf(pdf_path)
    if not book_text:
        print("Failed to extract any text from the PDF.")
        exit(1)

    # Step 2: Call the local LLM via REST API to get questions.
    print("Requesting questions from the local LLM...")
    questions = ask_questions_about_book(book_text)
    
    # Step 3: Output the questions.
    print("\nQuestions about the book:")
    print(questions)
