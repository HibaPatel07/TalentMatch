# TalentMatch frontend

Plain HTML/CSS/JS. No build step, no installs.

## Run it
    cd frontend
    python -m http.server 5500
Open http://localhost:5500. It starts in **demo mode**, so it works without a backend.

## Connect to the real API
1. Edit `config.js`: set `USE_MOCK: false` and `API_BASE` to the backend URL.
2. The backend must allow this page's origin (CORS). Ask the backend owner to add to FastAPI:

       from fastapi.middleware.cors import CORSMiddleware
       app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5500"],
                          allow_methods=["*"], allow_headers=["*"])

## API contract (from the project doc)
POST /match  { "resume": "...", "job_description": "..." }
->           { "match_score": 0.84, "matched_skills": [...], "missing_skills": [...] }

Optional extra fields, shown if present: `components` and `weights`
(keys: semantic, skills, experience, education).
