def calculate_skill_match(candidate_skills, required_skills):
    """
    Calculate the proportion of required skills
    that are present in the candidate's skills.
    """

    # Convert comma-separated strings into sets
    candidate_set = {
        skill.strip().lower()
        for skill in str(candidate_skills).split(",")
        if skill.strip()
    }

    required_set = {
        skill.strip().lower()
        for skill in str(required_skills).split(",")
        if skill.strip()
    }

    # Avoid division by zero
    if not required_set:
        return 0.0

    matched_skills = candidate_set.intersection(required_set)

    return len(matched_skills) / len(required_set)