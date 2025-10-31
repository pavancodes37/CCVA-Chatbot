
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report
import json
from datasets import load_dataset, Dataset

MODEL_PATH = "../model/bert_ccva_model"
DATASET_PATH = "../dataset/ccva_cybercrime_dataset_1000.json"

# Load label mappings
with open(f"{MODEL_PATH}/label_map.json", "r") as f:
    label_maps = json.load(f)
label2id = label_maps["label2id"]
id2label = {v: k for k, v in label2id.items()}

# Load model and tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)

# Load dataset
with open(DATASET_PATH, "r") as f:
    data = json.load(f)
texts = [d["text"] for d in data]
labels = [label2id[d["label"]] for d in data]

dataset = Dataset.from_dict({"text": texts, "label": labels})
dataset = dataset.train_test_split(test_size=0.2)

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=128)
dataset = dataset.map(tokenize, batched=True)

# Evaluation
preds, true_labels = [], []
for batch in dataset["test"]:
    inputs = tokenizer(batch["text"], return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=-1).item()
    preds.append(pred)
    true_labels.append(batch["label"])

accuracy = accuracy_score(true_labels, preds)
report = classification_report(true_labels, preds, target_names=id2label.values())

print(f"✅ Evaluation Accuracy: {accuracy:.4f}")
print("📊 Classification Report:\n", report)
