import re


_SKILL_ALIASES = {
    "python": ("python",),
    "sql": ("sql",),
    "machine learning": ("machine learning", "ml"),
    "pandas": ("pandas",),
    "numpy": ("numpy",),
    "scikit-learn": ("scikit-learn", "sklearn"),
    "tensorflow": ("tensorflow",),
    "pytorch": ("pytorch", "torch"),
    "deep learning": ("deep learning",),
    "java": ("java",),
    "javascript": ("javascript",),
    "typescript": ("typescript",),
    "react": ("react",),
    "node.js": ("node.js", "nodejs"),
    "fastapi": ("fastapi",),
    "django": ("django",),
    "flask": ("flask",),
    "docker": ("docker",),
    "kubernetes": ("kubernetes",),
    "aws": ("aws", "amazon web services"),
    "azure": ("azure",),
    "gcp": ("gcp", "google cloud"),
    "git": ("git",),
    "mlflow": ("mlflow",),
    "airflow": ("airflow",),
    "spark": ("spark", "apache spark"),
    "hadoop": ("hadoop",),
    "tableau": ("tableau",),
    "power bi": ("power bi",),
    "excel": ("excel",),
    "linux": ("linux",),
    "rest api": ("rest api", "restful api"),
    "graphql": ("graphql",),
    "postgresql": ("postgresql", "postgres"),
    "mongodb": ("mongodb",),
    "c++": ("c\\+\\+",),
    "c#": ("c#",),
    "go": ("golang",),
    "rust": ("rust",),
    "html": ("html",),
    "css": ("css",),
    "data analysis": ("data analysis",),
    "data visualization": ("data visualization",),
    "statistics": ("statistics",),
    "natural language processing": ("natural language processing", "nlp"),
    "computer vision": ("computer vision",),
    "data engineering": ("data engineering",),
}


def extract_skills(text):
    """Return recognized skills using whole-term matches to avoid substring hits."""
    found = []
    normalized_text = text.lower()

    for skill, aliases in _SKILL_ALIASES.items():
        alternatives = "|".join(
            rf"(?<![a-z0-9]){alias}(?![a-z0-9])" for alias in aliases
        )
        if re.search(alternatives, normalized_text):
            found.append(skill)

    return found


def extract_experience_years(text):
    """Return the first stated year requirement or experience duration, if present."""
    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:\+|-\s*\d+(?:\.\d+)?)?\s*(?:years?|yrs?)\b",
        text,
        flags=re.IGNORECASE,
    )
    return float(match.group(1)) if match else None
