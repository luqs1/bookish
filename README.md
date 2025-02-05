# Bookish

Bookish is a command-line tool that asks a question about the content of a PDF file by leveraging your local LLM running on ollama.

# Installation Guide

Follow these steps to install the project using `pip` and `venv`.

## Prerequisites

- Python 3.x installed on your system

## Steps

1. **Clone the repository:**

  ```bash
  git clone https://github.com/luqs1/bookish.git
  cd yourproject
  ```

2. **Create a virtual environment:**

  ```bash
  python3 -m venv .venv
  ```

3. **Activate the virtual environment:**

  - On macOS and Linux:

    ```bash
    source .venv/bin/activate
    ```

  - On Windows:

    ```bash
    .\.venv\Scripts\activate
    ```

4. **Install the dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

5. **Run the project:**

Ensure ollama is running.

  ```bash
  python main.py --pdf_path [PATH_TO_PDF]
  ```

You can optionally specify which model to use on ollama

  ```bash
  python main.py --pdf_path [PATH_TO_PDF] --model [MODEL_NAME]
  ```

## Deactivating the virtual environment

When you are done working, you can deactivate the virtual environment by running:

```bash
deactivate
```
