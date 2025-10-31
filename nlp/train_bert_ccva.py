import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch

# 1️⃣ Load dataset (JSON)
df = pd.read_json("ccva_cybercrime_dataset_1000.json")

# 2️⃣ Encode labels to integers
labels = list(df["label"].unique())
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}
df["label_id"] = df["label"].map(label2id)

# 3️⃣ Split data into train/test
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["text"].tolist(), df["label_id"].tolist(), test_size=0.2, random_state=42
)

# 4️⃣ Tokenize text data
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# 5️⃣ Create Torch dataset class
class CyberCrimeDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CyberCrimeDataset(train_encodings, train_labels)
val_dataset = CyberCrimeDataset(val_encodings, val_labels)

# 6️⃣ Load BERT model
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

# 7️⃣ Define training arguments
training_args = TrainingArguments(
    output_dir="./bert_ccva_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=1,
)

# 8️⃣ Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
)

# 9️⃣ Train model
trainer.train()

# 🔟 Save model & tokenizer
model.save_pretrained("./bert_ccva_model")
tokenizer.save_pretrained("./bert_ccva_model")

print("✅ BERT fine-tuning complete! Model saved in ./bert_ccva_model")
