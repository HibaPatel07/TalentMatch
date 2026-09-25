import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

INPUT_PATH = "data/processed/evaluation_results_v2.csv"

def main():
    df = pd.read_csv(INPUT_PATH)

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

    print("\nV2 Threshold Analysis")
    print("---------------------")
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

    best_accuracy = results_df.loc[
        results_df["accuracy"].idxmax()
    ]

    best_f1 = results_df.loc[
        results_df["f1"].idxmax()
    ]

    print("\nBest Accuracy:")
    print(best_accuracy)

    print("\nBest F1:")
    print(best_f1)

if __name__ == "__main__":
    main()