// Authentication tab switching
const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginPanel = document.getElementById("loginPanel");
const registerPanel = document.getElementById("registerPanel");
const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");

function showAuthPanel(panel) {
  const isLogin = panel === "login";
  loginPanel.classList.toggle("hidden", !isLogin);
  registerPanel.classList.toggle("hidden", isLogin);
  loginTab.classList.toggle("active", isLogin);
  registerTab.classList.toggle("active", !isLogin);
  loginTab.setAttribute("aria-selected", String(isLogin));
  registerTab.setAttribute("aria-selected", String(!isLogin));
}

loginTab.addEventListener("click", () => showAuthPanel("login"));
registerTab.addEventListener("click", () => showAuthPanel("register"));
showRegister.addEventListener("click", () => showAuthPanel("register"));
showLogin.addEventListener("click", () => showAuthPanel("login"));

const state = { token: localStorage.getItem("diet_token"), currentPlan: null };

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const headers = options.headers || {};
  headers["Content-Type"] = headers["Content-Type"] || "application/json";
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(path, {...options, headers});
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function message(id, text) { $(id).textContent = text || ""; }

async function refreshDashboard() {
  if (!state.token) {
    $("dashboard").classList.add("hidden");
    $("authState").textContent = "Not logged in";
    return;
  }
  try {
    const data = await api("/api/profile");
    $("dashboard").classList.remove("hidden");
    $("authState").textContent = "Authenticated";
    $("userName").textContent = data.user.name;
    const p = data.profile || {};
    for (const [key, value] of Object.entries(p)) {
      const el = document.querySelector(`#profileForm [name="${key}"]`);
      if (el) el.value = value ?? "";
    }
    await loadPlans();
    await loadFiles();
  } catch (err) {
    state.token = null;
    localStorage.removeItem("diet_token");
    message("loginMsg", err.message);
  }
}

$("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  try {
    await api("/api/register", {method:"POST", body:JSON.stringify(Object.fromEntries(form))});
    message("registerMsg", "Registration successful. You can now log in.");
    e.target.reset();
  } catch (err) { message("registerMsg", err.message); }
});

$("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  try {
    const data = await api("/api/login", {method:"POST", body:JSON.stringify(Object.fromEntries(form))});
    state.token = data.token;
    localStorage.setItem("diet_token", state.token);
    message("loginMsg", "Login successful.");
    location.hash = "#dashboard";
    await refreshDashboard();
  } catch (err) { message("loginMsg", err.message); }
});

$("profileForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  const data = Object.fromEntries(form);
  data.age = data.age ? Number(data.age) : null;
  data.height_cm = data.height_cm ? Number(data.height_cm) : null;
  data.weight_kg = data.weight_kg ? Number(data.weight_kg) : null;
  try {
    await api("/api/profile", {method:"PUT", body:JSON.stringify(data)});
    message("profileMsg", "Profile saved.");
  } catch (err) { message("profileMsg", err.message); }
});

$("generateBtn").addEventListener("click", async () => {
  try {
    const data = await api("/api/generate-plan", {method:"POST"});
    state.currentPlan = data.plan;
    renderPlan(data.plan);
    message("planMsg", "Plan generated.");
  } catch (err) { message("planMsg", err.message); }
});

function renderPlan(plan) {
  $("planPreview").classList.remove("hidden");
  $("savePlanBtn").classList.remove("hidden");
  $("planPreview").innerHTML = `
    <div class="meal"><strong>Breakfast</strong>${escapeHtml(plan.breakfast)}</div>
    <div class="meal"><strong>Lunch</strong>${escapeHtml(plan.lunch)}</div>
    <div class="meal"><strong>Snack</strong>${escapeHtml(plan.snack)}</div>
    <div class="meal"><strong>Dinner</strong>${escapeHtml(plan.dinner)}</div>
    <div class="meal"><strong>Summary</strong>${escapeHtml(plan.nutrition_summary)}</div>
    <div class="small">Source: ${escapeHtml(plan.source || "engine")}</div>
  `;
}

$("savePlanBtn").addEventListener("click", async () => {
  if (!state.currentPlan) return;
  try {
    const data = await api("/api/plans", {method:"POST", body:JSON.stringify(state.currentPlan)});
    message("planMsg", `Saved plan #${data.plan_id}.`);
    await loadPlans();
  } catch (err) { message("planMsg", err.message); }
});

async function loadPlans() {
  const data = await api("/api/plans");
  $("plans").innerHTML = data.plans.length ? data.plans.map(p => `
    <div class="list-item">
      <strong>Plan #${p.id}</strong>
      <div class="small">${new Date(p.created_at).toLocaleString()}</div>
      <div>${escapeHtml(p.breakfast)} · ${escapeHtml(p.lunch)} · ${escapeHtml(p.dinner)}</div>
      <button class="link-button" onclick="deletePlan(${p.id})">Delete</button>
    </div>`).join("") : "<p class='small'>No saved plans yet.</p>";
}

window.deletePlan = async function(id) {
  try { await api(`/api/plans/${id}`, {method:"DELETE"}); await loadPlans(); }
  catch (err) { alert(err.message); }
};

$("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = $("fileInput").files[0];
  if (!file) return;
  const form = new FormData();
  form.append("file", file);
  try {
    const response = await fetch("/api/upload", {
      method:"POST",
      headers:{Authorization:`Bearer ${state.token}`},
      body:form
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Upload failed");
    message("uploadMsg", "File uploaded.");
    e.target.reset();
    await loadFiles();
  } catch (err) { message("uploadMsg", err.message); }
});

async function loadFiles() {
  const data = await api("/api/files");
  $("files").innerHTML = data.files.length ? data.files.map(f => `
    <div class="list-item">
      <strong>${escapeHtml(f.filename)}</strong>
      <div class="small">${escapeHtml(f.storage_path)}</div>
      <button class="link-button" onclick="deleteFile(${f.id})">Delete</button>
    </div>`).join("") : "<p class='small'>No uploaded files yet.</p>";
}

window.deleteFile = async function(id) {
  try { await api(`/api/files/${id}`, {method:"DELETE"}); await loadFiles(); }
  catch (err) { alert(err.message); }
};

$("logoutBtn").addEventListener("click", () => {
  state.token = null;
  localStorage.removeItem("diet_token");
  location.hash = "#home";
  refreshDashboard();
  message("loginMsg", "Logged out.");
});

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}

refreshDashboard();
