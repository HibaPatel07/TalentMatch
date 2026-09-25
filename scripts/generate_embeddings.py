import pandas as pd

from src.models.embedding_model import load_embedding_model
from src.matching.similarity import cosine_similarity


INPUT_PATH = "data/raw/talentmatch_dummy_dataset.csv"
OUTPUT_PATH = "data/processed/similarity_results.csv"


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

        # Calculate semantic similarity
        similarity_score = cosine_similarity(
            resume_embedding,
            job_embedding
        )

        results.append({
            "candidate_id": row["candidate_id"],
            "job_id": row["job_id"],
            "job_title": row["job_title"],
            "similarity_score": similarity_score,
            "match_label": row["match_label"]
        })

    # Create results directory if required
    import os
    os.makedirs("data/processed", exist_ok=True)

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_PATH, index=False)

    print("\nSimilarity results generated successfully!")
    print(results_df.to_string(index=False))
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()