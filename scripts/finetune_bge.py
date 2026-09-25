import os
import pandas as pd
from datasets import Dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments
)
from sentence_transformers.losses import ContrastiveLoss

TRAIN_PATH = "data/processed/finetuning/train.csv"
VALIDATION_PATH = "data/processed/finetuning/validation.csv"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
OUTPUT_DIR = "models/TalentMatch_BGE_V2"

def load_dataset(path):
    df = pd.read_csv(path)

    df = df[
        [
            "resume_text_clean",
            "job_description_clean",
            "shortlisted"
        ]
    ].dropna()

    dataset = Dataset.from_pandas(
        df,
        preserve_index=False
    )

    dataset = dataset.rename_columns({
        "resume_text_clean": "sentence1",
        "job_description_clean": "sentence2",
        "shortlisted": "label"
    })

    return dataset

def main():
    train_dataset = load_dataset(TRAIN_PATH)
    validation_dataset = load_dataset(VALIDATION_PATH)

    model = SentenceTransformer(MODEL_NAME)

    loss = ContrastiveLoss(model=model)

    training_args = SentenceTransformerTrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        learning_rate=2e-5,
        warmup_steps=0.1,
        fp16=False,
        bf16=False,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=50,
        save_total_limit=1,
        report_to="none"
    )

    trainer = SentenceTransformerTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        loss=loss
    )

    trainer.train()

    model.save_pretrained(OUTPUT_DIR)

    print("\nFine-tuning completed successfully!")
    print(f"Model saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()