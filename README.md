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

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Use the notebook in `notebooks/01_bge_matching.ipynb` as the main workflow entry point.
