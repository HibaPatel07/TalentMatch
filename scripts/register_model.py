import mlflow
from mlflow import MlflowClient
from sentence_transformers import SentenceTransformer

EXPERIMENT_NAME = "TalentMatch_Baseline"
MODEL_NAME = "TalentMatch_BGE_Embedding"
MODEL_PATH = "models/TalentMatch_BGE_V2"

SEMANTIC_WEIGHT = 0.70
SKILL_WEIGHT = 0.25
EXPERIENCE_WEIGHT = 0.05
THRESHOLD = 0.65

ACCURACY = 0.8689
PRECISION = 0.9198
RECALL = 0.9063
F1_SCORE = 0.9130

def main():

    mlflow.set_experiment(EXPERIMENT_NAME)

    model = SentenceTransformer(MODEL_PATH)

    with mlflow.start_run(run_name="TalentMatch_BGE_V2") as run:

        mlflow.log_params({
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "model_version": "v2",
            "embedding_dimension": 384,
            "dataset": "Mahi_final_preprocessed_dataset",
            "training_samples": 4200,
            "validation_samples": 900,
            "test_samples": 900,
            "epochs": 1,
            "learning_rate": 2e-5,
            "batch_size": 4,
            "semantic_weight": SEMANTIC_WEIGHT,
            "skill_weight": SKILL_WEIGHT,
            "experience_weight": EXPERIENCE_WEIGHT,
            "threshold": THRESHOLD
        })

        mlflow.log_metrics({
            "test_accuracy": ACCURACY,
            "test_precision": PRECISION,
            "test_recall": RECALL,
            "test_f1": F1_SCORE
        })

        mlflow.set_tags({
            "model_stage": "validation",
            "model_type": "fine_tuned",
            "dataset_version": "Mahi_6000",
            "matching_configuration": "semantic_skill_experience"
        })

        mlflow.log_dict(
            {
                "semantic_weight": SEMANTIC_WEIGHT,
                "skill_weight": SKILL_WEIGHT,
                "experience_weight": EXPERIENCE_WEIGHT,
                "threshold": THRESHOLD
            },
            "matching_config.json"
        )

        mlflow.sentence_transformers.log_model(
            model,
            name="model",
            registered_model_name=MODEL_NAME
        )

        run_id = run.info.run_id

        client = MlflowClient()

        versions = client.search_model_versions(
            f"name='{MODEL_NAME}'"
        )

        latest_version = max(
            int(version.version)
            for version in versions
        )

        print("\n===== Model Registration Completed =====")
        print(f"Model Name     : {MODEL_NAME}")
        print(f"Run ID         : {run_id}")
        print(f"Model Version  : {latest_version}")
        print(f"Accuracy       : {ACCURACY:.4f}")
        print(f"Precision      : {PRECISION:.4f}")
        print(f"Recall         : {RECALL:.4f}")
        print(f"F1 Score       : {F1_SCORE:.4f}")
        print(f"Threshold      : {THRESHOLD}")
        print("Semantic Weight: 0.70")
        print("Skill Weight   : 0.25")
        print("Experience Weight: 0.05")

if __name__ == "__main__":
    main()