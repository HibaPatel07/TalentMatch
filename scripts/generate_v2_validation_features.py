import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from src.matching.skill_match import calculate_skill_match
from src.matching.experience_match import calculate_experience_match

INPUT_PATH = "data/processed/finetuning/validation.csv"
MODEL_PATH = "models/TalentMatch_BGE_V2"
OUTPUT_PATH = "data/processed/v2_validation_features.csv"

def main():
    df = pd.read_csv(INPUT_PATH)

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

    output = df[
        [
            "resume_id",
            "semantic_score",
            "skill_score",
            "experience_score",
            "shortlisted"
        ]
    ]

    os.makedirs("data/processed", exist_ok=True)
    output.to_csv(OUTPUT_PATH, index=False)

    print("\nV2 validation features generated successfully!")
    print(f"Rows: {len(output)}")
    print(f"Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()