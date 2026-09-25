import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

VALIDATION_PATH = "data/processed/finetuning/validation.csv"
MODEL_PATH = "models/TalentMatch_BGE_V2"

def main():
    df = pd.read_csv(VALIDATION_PATH)

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

    y_true = df["shortlisted"]

    results = []

    thresholds = [round(x / 100, 2) for x in range(30, 91, 5)]

    for threshold in thresholds:
        y_pred = (
            df["similarity_score"] >= threshold
        ).astype(int)

        results.append({
            "threshold": threshold,
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0)
        })

    results_df = pd.DataFrame(results)

    print("\nV2 Validation Threshold Analysis")
    print("--------------------------------")
    print(
        results_df.to_string(
            index=False,
            formatters={
                "accuracy": "{:.4f}".format,
                "precision": "{:.4f}".format,
                "recall": "{:.4f}".format,
                "f1": "{:.4f}".format
            }
        )
    )

    best = results_df.loc[
        results_df["f1"].idxmax()
    ]

    print("\nSelected Threshold:")
    print(f"Threshold: {best['threshold']:.2f}")
    print(f"Accuracy: {best['accuracy']:.4f}")
    print(f"Precision: {best['precision']:.4f}")
    print(f"Recall: {best['recall']:.4f}")
    print(f"F1: {best['f1']:.4f}")

if __name__ == "__main__":
    main()