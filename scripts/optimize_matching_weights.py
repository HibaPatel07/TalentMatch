import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

INPUT_PATH = "data/processed/v2_validation_features.csv"

def main():
    df = pd.read_csv(INPUT_PATH)

    y_true = df["shortlisted"]

    results = []

    for semantic_weight in [x / 100 for x in range(50, 81, 5)]:
        for skill_weight in [x / 100 for x in range(10, 41, 5)]:
            experience_weight = 1.0 - semantic_weight - skill_weight

            if experience_weight < 0.05 or experience_weight > 0.30:
                continue

            final_score = (
                semantic_weight * df["semantic_score"]
                + skill_weight * df["skill_score"]
                + experience_weight * df["experience_score"]
            )

            for threshold in [x / 100 for x in range(50, 91, 5)]:
                y_pred = (final_score >= threshold).astype(int)

                results.append({
                    "semantic_weight": semantic_weight,
                    "skill_weight": skill_weight,
                    "experience_weight": experience_weight,
                    "threshold": threshold,
                    "accuracy": accuracy_score(y_true, y_pred),
                    "precision": precision_score(y_true, y_pred, zero_division=0),
                    "recall": recall_score(y_true, y_pred, zero_division=0),
                    "f1": f1_score(y_true, y_pred, zero_division=0)
                })

    results_df = pd.DataFrame(results)

    best = results_df.loc[
        results_df["accuracy"].idxmax()
    ]

    print("\nBest Validation Configuration")
    print("-----------------------------")
    print(f"Semantic Weight: {best['semantic_weight']:.2f}")
    print(f"Skill Weight: {best['skill_weight']:.2f}")
    print(f"Experience Weight: {best['experience_weight']:.2f}")
    print(f"Threshold: {best['threshold']:.2f}")
    print(f"Accuracy: {best['accuracy']:.4f}")
    print(f"Precision: {best['precision']:.4f}")
    print(f"Recall: {best['recall']:.4f}")
    print(f"F1 Score: {best['f1']:.4f}")

    results_df.to_csv(
        "data/processed/weight_optimization_results.csv",
        index=False
    )

if __name__ == "__main__":
    main()