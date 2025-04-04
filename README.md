# Sentiment Analysis API

This project is a simple API that analyzes the sentiment of text using the `transformers` library. It uses the `pipeline` function for sentiment analysis, along with keyword extraction and text summarization. It's built with FastAPI.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd sentiment-api
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install fastapi uvicorn transformers newspaper python-dotenv spacy
    python -m spacy download en_core_web_sm
    ```

## Usage

1.  **Run the API:**

    ```bash
    uvicorn main:app --reload
    ```

    This will start the API server. By default, it runs on `http://127.0.0.1:8000`.

2.  **Interact with the API:**

    *   **Home Endpoint:**

        Visit `http://127.0.0.1:8000/` in your browser to see a welcome message.

    *   **Analyze Endpoint:**

        Send a POST request to `http://127.0.0.1:8000/analyze/` with a JSON payload containing the text you want to analyze. For example:

        ```json
        {
            "text": "This is a great day!"
        }
        ```

        You can use `curl`:

        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"text": "This is a great day!"}' http://127.0.0.1:8000/analyze/
        ```

        Or `python`:

        ```python
        import requests
        import json

        url = "http://127.0.0.1:8000/analyze/"
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"text": "This is a terrible day!"})
        response = requests.post(url, data=data, headers=headers)
        print(response.json())
        ```

        The API will return a JSON response like this:

        ```json
        {
            "text": "This is a great day!",
            "sentiment": "POSITIVE",
            "top_keywords": ["great", "day"],
            "summary": "This is a great day.",
        }
        ```
    *   **Analyze URL Endpoint:**

        Send a POST request to `http://127.0.0.1:8000/analyze-url/` with a JSON payload containing the URL of the article you want to analyze. For example:

        ```json
        {
            "url": "https://www.example.com/article"
        }
        ```

        You can use `curl`:

        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.example.com/article"}' http://127.0.0.1:8000/analyze-url/
        ```

        Or `python`:

        ```python
        import requests
        import json

        url = "http://127.0.0.1:8000/analyze-url/"
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"url": "https://www.example.com/article"})
        response = requests.post(url, data=data, headers=headers)
        print(response.json())
        ```

        The API will return a JSON response like this:

        ```json
        {
            "url": "https://www.example.com/article",
            "sentiment": "POSITIVE",
            "top_keywords": ["example", "article"],
            "summary": "This is a summary of the article.",
        }
        ```

## Description

The API has two main endpoints:

*   `/`: Returns a simple message indicating that the API is running.
*   `/analyze/`: Accepts a text string and returns the sentiment analysis result, including:
    *   The sentiment label (POSITIVE or NEGATIVE).
    *   The top 5 most common keywords in the text.
    *   A summary of the text.
*   `/analyze-url/`: Accepts a URL, downloads the article from the URL, and returns the sentiment analysis result, including:
    *   The sentiment label (POSITIVE or NEGATIVE).
    *   The top 5 most common keywords in the article.
    *   A summary of the article.
