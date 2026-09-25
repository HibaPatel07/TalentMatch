import pandas as pd

from src.models.embedding_model import load_embedding_model
from src.matching.similarity import cosine_similarity


# Load dataset
df = pd.read_csv("data/raw/talentmatch_dummy_dataset.csv")

# Take first resume-job pair
row = df.iloc[0]

# Load BGE model
model = load_embedding_model()

# Generate embeddings
resume_embedding = model.encode(row["resume_text"])[0]
job_embedding = model.encode(row["job_description"])[0]

# Calculate similarity
score = cosine_similarity(resume_embedding, job_embedding)

print("Candidate:", row["candidate_id"])
print("Job:", row["job_id"])
print("Job Title:", row["job_title"])
print("Similarity Score:", round(score, 4))