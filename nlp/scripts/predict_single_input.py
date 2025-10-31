import torch
from transformers import BertTokenizer, BertForSequenceClassification
import json
import os

# Path to your fine-tuned model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/bert_ccva_model")

# Load model and tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)

# Put model in evaluation mode
model.eval()

# Load labels from your JSON dataset (so predictions return readable names)
def load_labels():
    with open(os.path.join(os.path.dirname(__file__), "../dataset/ccva_cybercrime_dataset_1000.json"), "r") as f:
        data = json.load(f)
    labels = sorted(list(set([item["label"] for item in data])))
    return labels

labels = load_labels()

def predict(text: str):
    """Predicts the cybercrime category for a given text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    return labels[predicted_class]

if __name__ == "__main__":
    # Example: run directly from terminal
    test_text = input("Enter text to classify: ")
    prediction = predict(test_text)
    print(f"\n🧠 Predicted cybercrime category: {prediction}")
