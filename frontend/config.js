window.TALENTMATCH_CONFIG = {
  // Set to true to work without a backend (uses fake results).
  USE_MOCK: false,
  // FastAPI serves this UI on the same origin; this also works with a separate dev server.
  API_BASE: "http://localhost:8000",
  // Endpoint and request field names used by the FastAPI service.
  MATCH_PATH: "/match",
  REQUEST_FIELDS: { resume: "resume", job: "job_description" },
  // Labels for the verdict. Replace with the team's calibrated threshold later.
  STRONG_AT: 0.70,
  WEAK_BELOW: 0.40
};
