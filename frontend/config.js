// The ONLY file you should need to edit when the backend is ready.
window.TALENTMATCH_CONFIG = {
  // Set to true to work without a backend (uses fake results).
  USE_MOCK: true,
  // Where the teammates' FastAPI server runs.
  API_BASE: "http://localhost:8000",
  // Endpoint + field names, taken from the project doc. Change here if the backend differs.
  MATCH_PATH: "/match",
  REQUEST_FIELDS: { resume: "resume", job: "job_description" },
  // Labels for the verdict. Replace with the team's calibrated threshold later.
  STRONG_AT: 0.70,
  WEAK_BELOW: 0.40
};
