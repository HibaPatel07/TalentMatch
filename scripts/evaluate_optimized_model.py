import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from src.matching.skill_match import calculate_skill_match
from src.matching.experience_match import calculate_experience_match

TEST_PATH = "data/processed/finetuning/test.csv"
MODEL_PATH = "models/TalentMatch_BGE_V2"
OUTPUT_PATH = "data/processed/evaluation_optimized_v2.csv"

SEMANTIC_WEIGHT = 0.70
SKILL_WEIGHT = 0.25
EXPERIENCE_WEIGHT = 0.05
THRESHOLD = 0.65

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

    semantic_scores = []

    for resume_embedding, job_embedding in zip(
        resume_embeddings,
        job_embeddings
    ):
        score = model.similarity(
            resume_embedding,
            job_embedding
        ).item()
        semantic_scores.append(score)

    df["semantic_score"] = semantic_scores

    df["skill_score"] = df.apply(
        lambda row: calculate_skill_match(
            row["resume_skills_clean"],
            row["required_skills_clean"]
        ),
        axis=1
    )

    df["experience_score"] = df.apply(
        lambda row: calculate_experience_match(
            row["experience_years"],
            row["job_experience_required"]
        ),
        axis=1
    )

    df["final_match_score"] = (
        SEMANTIC_WEIGHT * df["semantic_score"]
        + SKILL_WEIGHT * df["skill_score"]
        + EXPERIENCE_WEIGHT * df["experience_score"]
    )

    df["predicted"] = (
        df["final_match_score"] >= THRESHOLD
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

    print("\nOptimized TalentMatch V2 Test Evaluation")
    print("----------------------------------------")
    print(f"Semantic Weight: {SEMANTIC_WEIGHT}")
    print(f"Skill Weight: {SKILL_WEIGHT}")
    print(f"Experience Weight: {EXPERIENCE_WEIGHT}")
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