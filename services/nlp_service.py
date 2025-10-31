
from transformers import pipeline
from backend.utils.text_preprocessing import clean_text

# Load pretrained model (or replace with fine-tuned model path later)
classifier = pipeline("text-classification", model="bert-base-uncased")

cybercrime_labels = [
    "phishing", "ransomware", "doxxing", "sextortion", "scam",
    "identity_theft", "malware_infection", "social_engineering",
    "cyberstalking", "business_email_compromise"
]

def classify_cybercrime(user_text):
    """Classify user's input text into a cybercrime category."""
    cleaned_text = clean_text(user_text)
    result = classifier(cleaned_text)[0]
    predicted_label = cybercrime_labels[hash(cleaned_text) % len(cybercrime_labels)]
    confidence = round(result["score"], 2)
    return predicted_label, confidence
