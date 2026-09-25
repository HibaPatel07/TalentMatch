import os

import pandas as pd

from src.models.embedding_model import load_embedding_model
from src.matching.similarity import cosine_similarity
from src.matching.skill_match import calculate_skill_match
from src.matching.experience_match import calculate_experience_match
from src.matching.scorer import calculate_match_score


INPUT_PATH = "data/raw/talentmatch_dummy_dataset.csv"
OUTPUT_PATH = "data/processed/match_results.csv"


def main():

    # Load dataset
    df = pd.read_csv(INPUT_PATH)

    # Load BGE model once
    model = load_embedding_model()

    results = []

    for _, row in df.iterrows():

        # Generate embeddings
        resume_embedding = model.encode(row["resume_text"])[0]
        job_embedding = model.encode(row["job_description"])[0]

        # Semantic similarity
        semantic_score = cosine_similarity(
            resume_embedding,
            job_embedding
        )

        # Skill matching
        skill_score = calculate_skill_match(
            row["candidate_skills"],
            row["required_skills"]
        )

        # Experience matching
        experience_score = calculate_experience_match(
            row["experience_years"],
            row["required_experience"]
        )

        # Final score
        final_score = calculate_match_score(
            semantic_score=semantic_score,
            skill_score=skill_score,
            experience_score=experience_score
        )

        results.append({
            "candidate_id": row["candidate_id"],
            "job_id": row["job_id"],
            "job_title": row["job_title"],
            "semantic_score": round(semantic_score, 4),
            "skill_score": round(skill_score, 4),
            "experience_score": round(experience_score, 4),
            "final_match_score": final_score,
            "match_label": row["match_label"]
        })

    # Create processed directory
    os.makedirs("data/processed", exist_ok=True)

    # Save results
    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nMatch scoring completed successfully!\n")
    print(results_df.to_string(index=False))

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()