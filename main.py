from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from newspaper import Article
from transformers import pipeline
import spacy
from collections import Counter
import string

# Initialize FastAPI app
app = FastAPI()

# Allow all origins (for development purposes only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load Sentiment Analysis pipeline from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

# Load Spacy NLP model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Initialize transformer for summarization (BART or T5)
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

class SentimentRequest(BaseModel):
    text: str

class URLRequest(BaseModel):
    url: str

@app.post("/analyze/")
async def analyze_sentiment(data: SentimentRequest):
    # Perform sentiment analysis on the plain text
    result = sentiment_pipeline(data.text)
    sentiment = result[0]['label']

    # Extract Top Keywords
    keywords = extract_keywords(data.text)

    # Generate Summary
    summary = generate_summary(data.text)

    return {
        "text": data.text,
        "sentiment": sentiment,
        "top_keywords": keywords,
        "summary": summary
    }

@app.post("/analyze-url/")
async def analyze_url(data: URLRequest):
    try:
        # Download and parse the article
        article = Article(data.url)
        article.download()
        article.parse()
        text = article.text

        # Perform sentiment analysis on the article's content
        result = sentiment_pipeline(text[:512])  # Limit to 512 tokens
        sentiment = result[0]['label']

        # Extract Top Keywords
        keywords = extract_keywords(text)

        # Generate Summary of the article
        summary = generate_summary(text)

        return {
            "url": data.url,
            "sentiment": sentiment,
            "top_keywords": keywords,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def extract_keywords(text: str):
    # Tokenize and remove stopwords/punctuation using spaCy
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

    # Count frequency of keywords
    keyword_counts = Counter(keywords)

    # Return top 5 most common keywords
    top_keywords = [word for word, _ in keyword_counts.most_common(5)]
    return top_keywords

def generate_summary(text: str):
    # Use transformers model (BART or T5) to generate a summary
    summary = summarization_pipeline(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Run with: uvicorn main:app --reload
# Note: You can also use Docker to run this FastAPI app in a container.