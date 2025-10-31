
import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import json
import os

# Paths
DATASET_PATH = "../dataset/ccva_cybercrime_dataset_1000.json"
MODEL_SAVE_PATH = "../model/bert_ccva_model"

# Load dataset
def load_ccva_dataset():
    with open(DATASET_PATH, "r") as f:
        data = json.load(f)

    texts = [item["text"] for item in data if "text" in item and "label" in item]
    labels = [item["label"] for item in data if "text" in item and "label" in item]

    unique_labels = sorted(list(set(labels)))
    label2id = {label: i for i, label in enumerate(unique_labels)}
    id2label = {i: label for label, i in label2id.items()}
    encoded_labels = [label2id[label] for label in labels]

    dataset = {"text": texts, "label": encoded_labels}
    return dataset, label2id, id2label

dataset, label2id, id2label = load_ccva_dataset()

# Save label mappings
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
with open(os.path.join(MODEL_SAVE_PATH, "label_map.json"), "w") as f:
    json.dump({"label2id": label2id, "id2label": id2label}, f)

# Convert to Hugging Face dataset
from datasets import Dataset
dataset = Dataset.from_dict(dataset)
dataset = dataset.train_test_split(test_size=0.2)

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=128)
dataset = dataset.map(tokenize, batched=True)

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=len(label2id), id2label=id2label, label2id=label2id
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
)

trainer.train()

# Save model
model.save_pretrained(MODEL_SAVE_PATH)
tokenizer.save_pretrained(MODEL_SAVE_PATH)

print(f"✅ Model fine-tuned and saved to {MODEL_SAVE_PATH}")
