def calculate_experience_match(
    experience_years,
    required_experience
):
    """
    Calculate experience match score between 0 and 1.
    """

    experience_years = float(experience_years)
    required_experience = float(required_experience)

    # No experience requirement
    if required_experience <= 0:
        return 1.0

    # Candidate meets or exceeds requirement
    if experience_years >= required_experience:
        return 1.0

    # Candidate has less experience
    return experience_years / required_experience