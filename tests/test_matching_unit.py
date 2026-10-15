"""Fast unit tests for the matching logic (no model download, no dataset needed)."""
import pytest

from src.matching.experience_match import calculate_experience_match
from src.matching.scorer import calculate_match_score
from src.matching.similarity import cosine_similarity
from src.matching.skill_match import calculate_skill_match
from src.matching.text_features import extract_experience_years, extract_skills


def test_score_weights_sum_to_one():
    assert calculate_match_score(1.0, 1.0, 1.0) == 1.0
    assert calculate_match_score(0.0, 0.0, 0.0) == 0.0


def test_score_is_weighted_60_30_10():
    assert calculate_match_score(1.0, 0.0, 0.0) == 0.6
    assert calculate_match_score(0.0, 1.0, 0.0) == 0.3
    assert calculate_match_score(0.0, 0.0, 1.0) == 0.1


def test_skill_match_partial_overlap():
    assert calculate_skill_match("Python, SQL", "python, sql, aws, docker") == 0.5


def test_skill_match_no_required_skills():
    assert calculate_skill_match("python", "") == 0.0


def test_experience_match_cases():
    assert calculate_experience_match(5, 3) == 1.0   # exceeds requirement
    assert calculate_experience_match(1, 4) == 0.25  # partial
    assert calculate_experience_match(0, 0) == 1.0   # no requirement


def test_cosine_similarity_of_unit_vectors():
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_extract_skills_whole_word_only():
    skills = extract_skills("Experienced in Python, SQL and Docker. Javascript too.")
    assert {"python", "sql", "docker", "javascript"} <= set(skills)
    assert "java" not in skills  # 'javascript' must not trigger 'java'


def test_extract_experience_years():
    assert extract_experience_years("3+ years of experience") == 3.0
    assert extract_experience_years("no number here") is None
