
import re

def clean_text(text):
    """Cleans and normalizes user text before NLP classification."""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
