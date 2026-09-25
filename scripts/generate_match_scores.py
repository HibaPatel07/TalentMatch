import os
import pandas as pd

from src.models.embedding_model import load_embedding_model
from src.matching.similarity import cosine_similarity
from src.matching.skill_match import calculate_skill_match
from src.matching.experience_match import calculate_experience_match
from src.matching.scorer import calculate_match_score


INPUT_PATH = "data/processed/Mahi_final_preprocessed_dataset.csv"
OUTPUT_PATH = "data/processed/match_results_mahi.csv"


def main():

    df = pd.read_csv(INPUT_PATH)

    model = load_embedding_model()

    resume_embeddings = model.encode(
        df["resume_text_clean"].tolist()
    )

    job_embeddings = model.encode(
        df["job_description_clean"].tolist()
    )

    results = []

    for index, row in df.iterrows():

        semantic_score = cosine_similarity(
            resume_embeddings[index],
            job_embeddings[index]
        )

        skill_score = calculate_skill_match(
            row["resume_skills_clean"],
            row["required_skills_clean"]
        )

        experience_score = calculate_experience_match(
            row["experience_years"],
            row["job_experience_required"]
        )

        final_score = calculate_match_score(
            semantic_score=semantic_score,
            skill_score=skill_score,
            experience_score=experience_score
        )

        results.append({
            "resume_id": row["resume_id"],
            "semantic_score": round(semantic_score, 4),
            "skill_score": round(skill_score, 4),
            "experience_score": round(experience_score, 4),
            "final_match_score": final_score,
            "shortlisted": row["shortlisted"]
        })

    os.makedirs("data/processed", exist_ok=True)

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nMatch scoring completed successfully!")
    print(f"Rows processed: {len(results_df)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()