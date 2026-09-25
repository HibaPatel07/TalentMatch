def calculate_match_score(
    semantic_score,
    skill_score,
    experience_score
):
    """
    Calculate the final candidate-job match score.

    Weights:
    - Semantic similarity: 60%
    - Skill match: 30%
    - Experience match: 10%
    """

    final_score = (
        0.60 * semantic_score
        + 0.30 * skill_score
        + 0.10 * experience_score
    )

    return round(final_score, 4)