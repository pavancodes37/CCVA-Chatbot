from flask import Blueprint, request, jsonify
from utils.response_templates import get_guidance_for_crime
from utils.mongo_connection import save_incident
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os
import json

chatbot_bp = Blueprint("chatbot_bp", __name__)

# Load the fine-tuned model
model_path = os.path.join(os.path.dirname(__file__), "../nlp/model/bert_ccva_model")
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()

# Load label map from dataset
dataset_path = os.path.join(os.path.dirname(__file__), "../nlp/dataset/ccva_cybercrime_dataset_1000.json")
with open(dataset_path, "r", encoding="utf-8") as f:
    data = json.load(f)
labels = sorted(list(set(item["label"] for item in data)))

@chatbot_bp.route("/predict", methods=["POST"])
def predict():
    try:
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # Tokenize input
        inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
            predicted_label = torch.argmax(outputs.logits, dim=1).item()

        detected_crime = labels[predicted_label]
        guidance = get_guidance_for_crime(detected_crime)

        # Store in DB (without sensitive info)
        save_incident(detected_crime)

        return jsonify({
            "crime_type": detected_crime,
            "guidance": guidance
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
