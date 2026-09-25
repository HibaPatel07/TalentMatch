import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

TEST_PATH = "data/processed/finetuning/test.csv"
MODEL_PATH = "models/TalentMatch_BGE_V2"
OUTPUT_PATH = "data/processed/evaluation_results_v2.csv"
THRESHOLD = 0.80

def main():
    df = pd.read_csv(TEST_PATH)

    model = SentenceTransformer(MODEL_PATH)

    resume_embeddings = model.encode(
        df["resume_text_clean"].tolist(),
        batch_size=16,
        show_progress_bar=True
    )

    job_embeddings = model.encode(
        df["job_description_clean"].tolist(),
        batch_size=16,
        show_progress_bar=True
    )

    similarities = []

    for resume_embedding, job_embedding in zip(
        resume_embeddings,
        job_embeddings
    ):
        score = model.similarity(
            resume_embedding,
            job_embedding
        ).item()
        similarities.append(score)

    df["similarity_score"] = similarities
    df["predicted"] = (
        df["similarity_score"] >= THRESHOLD
    ).astype(int)

    y_true = df["shortlisted"]
    y_pred = df["predicted"]

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("\nTalentMatch V2 Evaluation")
    print("-------------------------")
    print(f"Threshold: {THRESHOLD}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print(f"\nResults saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()