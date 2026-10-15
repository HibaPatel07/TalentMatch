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

## Run with Docker

```bash
docker build -t talentmatch-api .
docker run -p 8000:8000 talentmatch-api
# or
docker compose up --build
```

Open <http://localhost:8000> (UI + `POST /match`); health probe at `/health`.
The BGE model is downloaded and baked into the image at build time, so the
container starts without internet access. To also start the MLflow UI on
<http://localhost:5000>: `docker compose --profile mlflow up`.
