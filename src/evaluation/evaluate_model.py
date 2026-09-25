import os
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

INPUT_PATH = "data/processed/match_results.csv"
OUTPUT_PATH = "data/processed/evaluation_results.csv"

# Baseline threshold
THRESHOLD = 0.60


def main():

    # Load match results
    df = pd.read_csv(INPUT_PATH)

    # Convert match score into predicted label
    df["predicted_label"] = (
        df["final_match_score"] >= THRESHOLD
    ).astype(int)

    # Actual and predicted labels
    y_true = df["match_label"]
    y_pred = df["predicted_label"]

    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )
    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )
    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Create evaluation summary
    evaluation_results = pd.DataFrame([
        {
            "threshold": THRESHOLD,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "true_negatives": cm[0][0],
            "false_positives": cm[0][1],
            "false_negatives": cm[1][0],
            "true_positives": cm[1][1]
        }
    ])

    # Create output directory
    os.makedirs("data/processed", exist_ok=True)

    # Save evaluation results
    evaluation_results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n===== TalentMatch Evaluation =====")
    print(f"Threshold : {THRESHOLD}")
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nEvaluation results saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()