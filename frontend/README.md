# TalentMatch frontend

The plain HTML/CSS/JS frontend is served by the FastAPI application from the
repository root. For the complete local setup and command, see the root
[README](../README.md).

The UI sends `POST /match` with `resume` and `job_description` and displays the
returned match score, skill lists, and component breakdown.
