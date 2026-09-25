const C = window.TALENTMATCH_CONFIG;
const $ = id => document.getElementById(id);
const updateCount = (inputId, countId) => {
  const count = $(inputId).value.length;
  $(countId).textContent = count + (count === 1 ? " character" : " characters");
};

["resume", "job"].forEach(id => {
  $(id).addEventListener("input", () => updateCount(id, id + "-count"));
});
const LABELS = { semantic: "Meaning", skills: "Skills", experience: "Experience", education: "Education" };

const SAMPLE = {
  resume: "Data analyst with 3 years of experience building dashboards and models. Strong in Python, SQL, pandas and machine learning. Used Git daily. Bachelor of Engineering in Computer Science.",
  job: "We are hiring a Machine Learning Engineer with 3+ years of experience. You will work with Python, SQL, machine learning, pandas, Docker and AWS to ship models. Bachelor's degree required."
};

$("mode").textContent = C.USE_MOCK ? "Demo mode (no backend)" : "Live: " + C.API_BASE;
$("sample").onclick = () => {
  $("resume").value = SAMPLE.resume;
  $("job").value = SAMPLE.job;
  updateCount("resume", "resume-count");
  updateCount("job", "job-count");
};
$("clear").onclick = () => {
  $("resume").value = "";
  $("job").value = "";
  updateCount("resume", "resume-count");
  updateCount("job", "job-count");
  $("result").hidden = true;
  $("error").textContent = "";
};

// --- Talking to the backend -------------------------------------------------
async function fetchMatch(resume, job) {
  if (C.USE_MOCK) return normalizeMatch(await mockMatch(resume, job));
  let res;
  try {
    res = await fetch(C.API_BASE + C.MATCH_PATH, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [C.REQUEST_FIELDS.resume]: resume, [C.REQUEST_FIELDS.job]: job })
    });
  } catch {
    throw new Error("Can't reach the server at " + C.API_BASE + ". Check that it is running.");
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const detail = typeof data?.detail === "string"
      ? data.detail
      : Array.isArray(data?.detail)
        ? data.detail
          .map(issue => issue && typeof issue.msg === "string" ? issue.msg : "")
          .filter(Boolean)
          .join(" ")
        : "";
    throw new Error(detail || "The server returned an error (" + res.status + ").");
  }
  return normalizeMatch(data);
}

// Fake backend so the UI works alone. Same shape as the doc's example output.
function mockMatch(resume, job) {
  const vocab = ["python","sql","machine learning","pandas","numpy","docker","aws","airflow","mlflow","git","pytorch","fastapi"];
  const has = (t, s) => t.toLowerCase().includes(s);
  const needed = vocab.filter(s => has(job, s));
  const matched = needed.filter(s => has(resume, s));
  const missing = needed.filter(s => !has(resume, s));
  const skills = needed.length ? matched.length / needed.length : 1;
  return new Promise(r => setTimeout(() => r({
    match_score: +(0.5 + 0.5 * skills * 0.9).toFixed(2),
    matched_skills: matched.map(cap), missing_skills: missing.map(cap)
  }), 500));
}
const ACRONYMS = ["sql","aws"];
const cap = s => ACRONYMS.includes(s) ? s.toUpperCase() : s.replace(/\b\w/g, c => c.toUpperCase());

// --- Showing the result -----------------------------------------------------
function chips(el, items, cls) {
  el.replaceChildren();
  if (!items || !items.length) { el.innerHTML = '<span class="none">None</span>'; return; }
  items.forEach(s => { const c = document.createElement("span"); c.className = "chip " + cls; c.textContent = s; el.append(c); });
}

function normalizeMatch(data) {
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    throw new Error("The server returned an invalid match response.");
  }

  const score = data.match_score;
  if (typeof score !== "number" || !Number.isFinite(score) || score < 0 || score > 1) {
    throw new Error("The server response is missing a valid match score.");
  }

  const components = data.components && typeof data.components === "object" && !Array.isArray(data.components)
    ? Object.fromEntries(Object.entries(data.components).filter(([, value]) =>
      typeof value === "number" && Number.isFinite(value) && value >= 0 && value <= 1))
    : {};
  const weights = data.weights && typeof data.weights === "object" && !Array.isArray(data.weights)
    ? Object.fromEntries(Object.entries(data.weights).filter(([, value]) =>
      typeof value === "number" && Number.isFinite(value) && value >= 0))
    : {};

  return {
    match_score: score,
    matched_skills: Array.isArray(data.matched_skills)
      ? data.matched_skills.filter(skill => typeof skill === "string")
      : [],
    missing_skills: Array.isArray(data.missing_skills)
      ? data.missing_skills.filter(skill => typeof skill === "string")
      : [],
    components,
    weights
  };
}

function render(d) {
  const pct = Math.round(d.match_score * 100);
  $("result").hidden = false;
  $("score").textContent = pct + "%";
  $("verdict").textContent = d.match_score >= C.STRONG_AT ? "Strong match" : d.match_score >= C.WEAK_BELOW ? "Partial match" : "Weak match";
  $("marker").style.left = pct + "%";
  chips($("matched"), d.matched_skills, "good");
  chips($("missing"), d.missing_skills, "bad");

  // Optional: only shown if the backend sends a component breakdown.
  const comps = d.components;
  const componentKeys = Object.keys(comps);
  $("breakdown").hidden = componentKeys.length === 0;
  $("bars").replaceChildren(...componentKeys.map(k => {
    const value = Math.round(comps[k] * 100);
    const row = document.createElement("div");
    row.className = "bar";
    const label = document.createElement("span");
    label.textContent = LABELS[k] || k;
    const track = document.createElement("div");
    track.className = "track";
    const fill = document.createElement("div");
    fill.className = "fill";
    fill.style.width = value + "%";
    track.append(fill);
    const detail = document.createElement("span");
    detail.className = "w";
    const weight = d.weights?.[k];
    detail.textContent = value + "%" + (weight !== undefined ? " × " + weight : "");
    row.append(label, track, detail);
    return row;
  }));
}

$("go").onclick = async () => {
  $("error").textContent = "";
  if ($("resume").value.trim().length < 20 || $("job").value.trim().length < 20) {
    $("error").textContent = "Add at least a couple of sentences to both boxes."; return;
  }
  $("go").disabled = true; $("go").textContent = "Checking…";
  try { render(await fetchMatch($("resume").value, $("job").value)); }
  catch (e) { $("error").textContent = e.message; }
  finally { $("go").disabled = false; $("go").textContent = "Check match"; }
};
