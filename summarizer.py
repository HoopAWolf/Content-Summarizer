from transformers import pipeline
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from newspaper import Article
from textblob import TextBlob
from keybert import KeyBERT

def summarize_with_bart(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # Split text into chunks if too long (BART has a token limit)
    max_chunk = 1024
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=60, min_length=1, do_sample=False)
        summaries.append(summary[0]["summary_text"])
        summaries.append('\n\n')
    return " ".join(summaries)

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

def extract_keywords(text):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=10)
    return [kw[0] for kw in keywords]

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract paragraphs (adjust based on website structure)
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text[:5000]  # Limit to avoid overwhelming the LLM
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_with_newspaper(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text[:5000]