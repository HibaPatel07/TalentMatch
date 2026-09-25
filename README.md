# TalentMatch

TalentMatch is a project for matching resumes to job opportunities using embedding-based similarity and evaluation pipelines.

## Project structure

TalentMatch/
│
├── data/
│   └── raw/
│       └── resume_data.csv
│
├── notebooks/
│   └── 01_bge_matching.ipynb
│
├── src/
│   ├── preprocessing/
│   ├── model/
│   ├── matching/
│   └── evaluation/
│
├── models/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore

## Run locally

From the repository root, create and activate a virtual environment, install the
dependencies, and start the combined FastAPI application:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

Open <http://localhost:8000>. FastAPI serves the frontend and exposes
`POST /match`. The first startup loads the `BAAI/bge-small-en-v1.5` embedding
model; an internet connection is needed the first time so it can be downloaded.

The frontend can also be served separately for development:

```powershell
python -m http.server 5500 --directory frontend
```

The `/match` request accepts `resume` and `job_description` strings. Its response
contains the weighted `match_score`, detected `matched_skills` and
`missing_skills`, plus semantic, skills, and experience component scores.

For offline model experimentation, see `notebooks/01_bge_matching.ipynb`.
