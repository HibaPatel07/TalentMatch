from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.matching.experience_match import calculate_experience_match
from src.matching.scorer import calculate_match_score
from src.matching.similarity import cosine_similarity
from src.matching.skill_match import calculate_skill_match
from src.matching.text_features import extract_experience_years, extract_skills
from src.models.embedding_model import load_embedding_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.embedding_model = load_embedding_model()
    yield


app = FastAPI(title="TalentMatch API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


class MatchRequest(BaseModel):
    resume: str = Field(min_length=20, max_length=50000)
    job_description: str = Field(min_length=20, max_length=50000)


@app.post("/match/")
@app.post("/match")
def match_documents(request: MatchRequest):
    resume_skills = extract_skills(request.resume)
    required_skills = extract_skills(request.job_description)
    matched_skills = sorted(set(resume_skills).intersection(required_skills))
    missing_skills = sorted(set(required_skills).difference(resume_skills))

    candidate_experience = extract_experience_years(request.resume)
    required_experience = extract_experience_years(request.job_description)
    experience_score = calculate_experience_match(
        candidate_experience if candidate_experience is not None else 0,
        required_experience if required_experience is not None else 0,
    )

    embeddings = app.state.embedding_model.encode(
        [request.resume, request.job_description]
    )
    semantic_score = max(
        0.0,
        min(1.0, cosine_similarity(embeddings[0], embeddings[1])),
    )
    skill_score = calculate_skill_match(
        ",".join(resume_skills),
        ",".join(required_skills),
    )
    match_score = calculate_match_score(
        semantic_score=semantic_score,
        skill_score=skill_score,
        experience_score=experience_score,
    )

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "components": {
            "semantic": round(semantic_score, 4),
            "skills": round(skill_score, 4),
            "experience": round(experience_score, 4),
        },
        "weights": {
            "semantic": 0.6,
            "skills": 0.3,
            "experience": 0.1,
        },
    }


FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
