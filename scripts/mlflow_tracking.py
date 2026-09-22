import os
import pandas as pd
import mlflow


# -----------------------------
# File paths
# -----------------------------
EVALUATION_PATH = "data/processed/evaluation_results.csv"


# -----------------------------
# MLflow experiment
# -----------------------------
EXPERIMENT_NAME = "TalentMatch_Baseline"


def main():

    # Load evaluation results
    evaluation_df = pd.read_csv(EVALUATION_PATH)
    results = evaluation_df.iloc[0]

    # Create or select experiment
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Start MLflow run
    with mlflow.start_run():

        # -----------------------------
        # Log parameters
        # -----------------------------
        mlflow.log_param(
            "embedding_model",
            "BAAI/bge-small-en-v1.5"
        )

        mlflow.log_param(
            "dataset",
            "talentmatch_dummy_dataset.csv"
        )

        mlflow.log_param(
            "threshold",
            results["threshold"]
        )

        mlflow.log_param(
            "semantic_weight",
            0.60
        )

        mlflow.log_param(
            "skill_weight",
            0.30
        )

        mlflow.log_param(
            "experience_weight",
            0.10
        )

        # -----------------------------
        # Log evaluation metrics
        # -----------------------------
        mlflow.log_metric(
            "accuracy",
            results["accuracy"]
        )

        mlflow.log_metric(
            "precision",
            results["precision"]
        )

        mlflow.log_metric(
            "recall",
            results["recall"]
        )

        mlflow.log_metric(
            "f1_score",
            results["f1_score"]
        )

        # -----------------------------
        # Log confusion matrix values
        # -----------------------------
        mlflow.log_metric(
            "true_negatives",
            results["true_negatives"]
        )

        mlflow.log_metric(
            "false_positives",
            results["false_positives"]
        )

        mlflow.log_metric(
            "false_negatives",
            results["false_negatives"]
        )

        mlflow.log_metric(
            "true_positives",
            results["true_positives"]
        )

        # -----------------------------
        # Log evaluation file
        # -----------------------------
        mlflow.log_artifact(
            EVALUATION_PATH,
            artifact_path="evaluation"
        )

        # -----------------------------
        # Add run tags
        # -----------------------------
        mlflow.set_tag(
            "model_stage",
            "baseline"
        )

        mlflow.set_tag(
            "model_version",
            "v1"
        )

        print("\n===== MLflow Run Completed =====")
        print(f"Experiment : {EXPERIMENT_NAME}")
        print(
            f"Run ID     : "
            f"{mlflow.active_run().info.run_id}"
        )
        print(f"Accuracy   : {results['accuracy']:.4f}")
        print(f"Precision  : {results['precision']:.4f}")
        print(f"Recall     : {results['recall']:.4f}")
        print(f"F1 Score   : {results['f1_score']:.4f}")


if __name__ == "__main__":
    main()