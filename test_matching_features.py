import pandas as pd

from src.matching.skill_match import calculate_skill_match
from src.matching.experience_match import calculate_experience_match
from src.matching.scorer import calculate_match_score


# Load dataset
df = pd.read_csv("data/raw/talentmatch_dummy_dataset.csv")

# Take first candidate-job pair
row = df.iloc[0]

# Calculate skill match
skill_score = calculate_skill_match(
    row["candidate_skills"],
    row["required_skills"]
)

# Calculate experience match
experience_score = calculate_experience_match(
    row["experience_years"],
    row["required_experience"]
)

# Calculate final match score
final_score = calculate_match_score(
    semantic_score=0.877809,
    skill_score=skill_score,
    experience_score=experience_score
)

print("Candidate:", row["candidate_id"])
print("Job:", row["job_id"])
print("Job Title:", row["job_title"])
print("Semantic Similarity:", 0.877809)
print("Skill Match Score:", round(skill_score, 4))
print("Experience Match Score:", round(experience_score, 4))
print("Final Match Score:", final_score)
print("Final Match Percentage:", round(final_score * 100, 2), "%")
print("Actual Match Label:", row["match_label"])