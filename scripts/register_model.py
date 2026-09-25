import mlflow
from mlflow import MlflowClient
from src.models.embedding_model import load_embedding_model

EXPERIMENT_NAME = "TalentMatch_Baseline"
MODEL_NAME = "TalentMatch_BGE_Embedding"


def main():

    mlflow.set_experiment(EXPERIMENT_NAME)

    model = load_embedding_model()

    with mlflow.start_run(run_name="TalentMatch_BGE_V1") as run:

        mlflow.log_param(
            "embedding_model",
            "BAAI/bge-small-en-v1.5"
        )

        mlflow.log_param(
            "model_version",
            "v1"
        )

        mlflow.log_param(
            "embedding_dimension",
            384
        )

        mlflow.set_tag(
            "model_stage",
            "baseline"
        )

        mlflow.sentence_transformers.log_model(
            model.model,
            name="model",
            registered_model_name=MODEL_NAME
        )

        run_id = run.info.run_id

        print("\n===== Model Registration Completed =====")
        print(f"Model Name : {MODEL_NAME}")
        print(f"Run ID     : {run_id}")
        print("Model Version : 1")


if __name__ == "__main__":
    main()