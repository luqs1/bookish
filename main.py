import json
import requests
from PyPDF2 import PdfReader
import argparse

def parse_arguments():
  parser = argparse.ArgumentParser(description="Generate questions about a book using a local LLM.")
  parser.add_argument("--pdf_path", type=str, required=True, help="The path to the PDF file of the book.")
  parser.add_argument("--model", type=str, required=False, default="llama2", help="The model name to use for the LLM.")
  return parser.parse_args()

args = parse_arguments()
MODEL = args.model
PDF_PATH = args.pdf_path

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

def ask_questions_about_book(book_text, focus: str, max_prompt_length=2000,):
    """
    Constructs a prompt with the book text (truncated if necessary)
    and calls the local LLM API on Ollama to generate questions about the book.
    """
    # Truncate the text if it's too long for the prompt.
    truncated_text = book_text[:max_prompt_length]
    
    # Construct the prompt for the LLM.
    prompt = (
        "You are an insightful literature teacher. "
        "Based on the following excerpt from a book, please provide one highly specific"
        "open-ended question that could help a reader reflect on and understand the content better:\n\n"
        "Wrap the question in <q> and <q/> tags."
        f"Ensure the question is focused around {focus}"
        f"{truncated_text}\n\nQuestions:"
    )

    # Define the API endpoint and payload.
    # Adjust the URL and payload parameters based on your Ollama API documentation.
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "prompt": prompt,
        "max_tokens": 150,      # Adjust based on how long you expect the output to be.
        "temperature": 0.7,     # Creativity of the LLM output.
        "model": MODEL,      # Replace with the actual model name.
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

def extract_question(question_string):
    start_tag = "<q>"
    end_tag = "<q/>"
    start_index = questions.find(start_tag)
    end_index = questions.find(end_tag)

    if start_index != -1 and end_index != -1:
      extracted_question = questions[start_index + len(start_tag):end_index].strip()
    else:
      return question_string

if __name__ == "__main__":
    # Path to the PDF file of the book.
    pdf_path = PDF_PATH

    # Step 1: Extract the book text.
    print("Extracting text from the PDF...")
    book_text = extract_text_from_pdf(pdf_path)
    if not book_text:
        print("Failed to extract any text from the PDF.")
        exit(1)
    
    # Ask the user what they want to focus on.
    focus = input("What aspect of the book would you like to focus on (e.g., themes, characters, plot)? ")
    
    # Step 2: Call the local LLM via REST API to get questions.
    print("Requesting question from the local LLM...")
    questions = ask_questions_about_book(book_text, focus)
    # Extract the question from the response using <q> and <q/> tags.
    extracted_question = extract_question(questions)

    # Step 3: Output the questions.
    print("\nQuestion about the book:" )
    print(extracted_question)
