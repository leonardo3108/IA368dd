import evaluate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import torch
import os
#import pyserini
import datasets
from datasets import load_dataset
#from pyserini.index import IndexReader
#from pyserini.search import SimpleSearcher
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration,AutoModelForSeq2SeqLM, T5Config, AdamW, Adafactor
from pathlib import Path

model_name = 't5-base'
batch_size=22
gradient_accumulation_steps=8
epochs=100
model_output_dir = 'model_output'
model_save_dir = 'model_save'
dataset_dir = 'exercicios/Aula_6/data'

sacrebleu_metric = evaluate.load("sacrebleu")

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]
    return preds, labels

def compute_metrics(preds, labels):
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)
  
    result = sacrebleu_metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}

    return result

class MSMARCODataset(Dataset):
    def __init__(self, data_df, tokenizer, max_len):
        self.data = data_df
       
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        query = self.data.loc[index, "query"]
        relevant_passage = self.data.loc[index, "relevant_passage"]
        tokenized_inputs = self.tokenizer( relevant_passage, return_tensors="pt", max_length=self.max_len, padding="max_length", truncation=True)
        tokenized_target = self.tokenizer( query, return_tensors="pt", max_length=self.max_len, padding="max_length", truncation=True).input_ids

        tokenized_target=torch.where(tokenized_target == 0, torch.tensor(-100, dtype=tokenized_target.dtype), tokenized_target)

        return {"input_ids": tokenized_inputs["input_ids"].squeeze(0), "attention_mask": tokenized_inputs["attention_mask"].squeeze(0), "labels": tokenized_target.squeeze(0)}

if torch.cuda.is_available(): 
   dev = "cuda:0"
else: 
   dev = "cpu"
device = torch.device(dev)
print('Using {}'.format(device))

data= pd.read_csv(dataset_dir + '/msmarco_triples.train.tiny.tsv', delimiter="\t", header=None, names=["query", "relevant_passage", "non_relevant_passage"])

print('Dataset:', len(data), 'lines.')

# get the number of rows to sample for df1
n = int(len(data)*0.05)

# randomly sample n rows for val
valid_data = data.sample(n)

# get the remaining rows for train
train_data = data.drop(valid_data.index)

train_data = train_data.reset_index(drop=True)
valid_data = valid_data.reset_index(drop=True)


tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
print(type(model))
dataset_train = MSMARCODataset(train_data, tokenizer, max_len=256)
dataloader_train = DataLoader(dataset_train, batch_size=32, shuffle=True)

dataset_val = MSMARCODataset(valid_data, tokenizer, max_len=256)
dataloader_val = DataLoader(dataset_val, batch_size=32, shuffle=True)

# Treine o modelo seq2seq
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# optimizer = AdamW(model.parameters(), lr=2e-4)
optimizer = Adafactor(model.parameters(), relative_step=False,lr=2e-4)
epochs = 25
during_training_metrics=[]
model.train()
for epoch in range(epochs):
    
    for step, batch in tqdm(enumerate(dataloader_train), total=len(dataloader_train), desc=f"epoch {epoch}"):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)

        loss = outputs.loss
        loss.backward()

        optimizer.step()
        optimizer.zero_grad()

    
    acc={
        "bleu":0,
        "val_loss": 0
    }
    with torch.no_grad():
      for val_batch in tqdm(dataloader_val, total=len(dataloader_val), desc="evaluating"):
        input_ids = val_batch["input_ids"].to(device)
        attention_mask = val_batch["attention_mask"].to(device)
        labels = val_batch["labels"]

        gen_ids = model.generate(input_ids=input_ids, attention_mask=attention_mask)
        metric_result=compute_metrics(gen_ids, labels)
        
        labels = val_batch["labels"].to(device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)

        metric_result["val_loss"] = outputs.loss.cpu().item()

        for metric in acc:
          acc[metric]+=metric_result[metric]
      
      for metric in acc:
        acc[metric]=acc[metric]/len(dataloader_val)

      acc["train_loss"]= loss.cpu().item()
      during_training_metrics.append(acc)
      print(acc)
    save_path=Path(model_save_dir, "train", f"epoch_{epoch}")
    os.makedirs(save_path.parent, exist_ok=True)
    model.save_pretrained(save_path)

# Define the metrics to plot
metrics = ["bleu", "val_loss", "train_loss"]

# Plot each metric in a separate subplot
fig, axs = plt.subplots(len(metrics), 1, figsize=(10, 8))
for i, metric in enumerate(metrics):
    axs[i].plot([x[metric] for x in during_training_metrics])
    axs[i].set_title(metric)
    axs[i].set_xlabel("Epoch")
    axs[i].set_ylabel(metric)
plt.tight_layout()
plt.show()
