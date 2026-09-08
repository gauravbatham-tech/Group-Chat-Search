const queryInput = document.getElementById("query");
const searchButton = document.getElementById("search-button");
const resultsDiv = document.getElementById("results");
const loading = document.getElementById("loading");
const chatFile = document.getElementById("chat-file");
const uploadStatus = document.getElementById("upload-status");
let activeChatId = null;
const historyKey = "chatsense-history";
const savedKey = "chatsense-saved";
const authTokenKey = "chatsense-token";
const authUserKey = "chatsense-user";
let authMode = "login";
const authGate = document.getElementById("auth-gate");
const appShell = document.getElementById("app-shell");
const authForm = document.getElementById("auth-form");
const authSwitch = document.getElementById("auth-switch");
const authName = document.getElementById("auth-name");
const authEmail = document.getElementById("auth-email");
const authPassword = document.getElementById("auth-password");
const authError = document.getElementById("auth-error");

function getAuthToken() {
    return sessionStorage.getItem(authTokenKey);
}

function setAuthSession(data) {
    sessionStorage.setItem(authTokenKey, data.token);
    sessionStorage.setItem(authUserKey, JSON.stringify(data.user));
    const initials = data.user.name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();
    document.getElementById("user-avatar").textContent = initials;
    authGate.classList.add("is-hidden");
    appShell.classList.remove("is-locked");
    handleRoute();
}

function showAuthMode(mode) {
    authMode = mode;
    const signup = mode === "signup";
    document.getElementById("auth-overline").textContent = signup ? "Make it yours" : "Welcome back";
    document.getElementById("auth-title").textContent = signup ? "Create your ChatSense account" : "Sign in to ChatSense";
    document.getElementById("auth-subtitle").textContent = signup ? "A private home for your conversation memories." : "Your conversation workspace is waiting.";
    document.getElementById("name-field").classList.toggle("is-hidden", !signup);
    document.getElementById("auth-submit").innerHTML = signup ? "Create account <span>→</span>" : "Sign in <span>→</span>";
    document.getElementById("auth-switch-copy").textContent = signup ? "Already have an account?" : "New to ChatSense?";
    authSwitch.textContent = signup ? "Sign in" : "Create an account";
    authPassword.setAttribute("autocomplete", signup ? "new-password" : "current-password");
    authError.textContent = "";
}

authSwitch.addEventListener("click", () => showAuthMode(authMode === "login" ? "signup" : "login"));

authForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = document.getElementById("auth-submit");
    submit.disabled = true;
    authError.textContent = "";
    try {
        const response = await fetch(`http://127.0.0.1:8000/auth/${authMode}`, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: authName.value, email: authEmail.value, password: authPassword.value })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Authentication failed.");
        setAuthSession(data);
        authForm.reset();
    } catch (error) {
        authError.textContent = error.message;
    } finally {
        submit.disabled = false;
    }
});

async function signOut() {
    const token = getAuthToken();
    if (token) await fetch("http://127.0.0.1:8000/auth/logout", { method: "POST", headers: { Authorization: `Bearer ${token}` } });
    sessionStorage.removeItem(authTokenKey);
    sessionStorage.removeItem(authUserKey);
    activeChatId = null;
    authGate.classList.remove("is-hidden");
    appShell.classList.add("is-locked");
    showAuthMode("login");
}

document.getElementById("signout-button").addEventListener("click", signOut);

function getHistory() {
    return JSON.parse(localStorage.getItem(historyKey) || "[]");
}

function getSaved() {
    return JSON.parse(localStorage.getItem(savedKey) || "[]");
}

function routeTo(route) {
    const activeRoute = route || "home";
    document.querySelectorAll(".route-view").forEach((view) => {
        view.classList.toggle("is-hidden", view.dataset.view && view.dataset.view !== activeRoute);
    });
    document.querySelectorAll(".side-nav a[data-route]").forEach((link) => {
        link.classList.toggle("active", link.dataset.route === activeRoute);
    });
    if (activeRoute === "home") renderHome();
    if (activeRoute === "insights") renderInsights();
}

function handleRoute() {
    const route = location.hash.replace("#", "") || "home";
    routeTo(["home", "search", "insights", "learn"].includes(route) ? route : "home");
}

window.addEventListener("hashchange", handleRoute);

queryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") searchMessages();
});

chatFile.addEventListener("change", uploadChat);

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
    }[character]));
}

function formatAnswer(value) {
    return escapeHtml(value).replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}

function formatDate(timestamp) {
    return new Intl.DateTimeFormat("en-IN", {
        day: "numeric", month: "short", year: "numeric", hour: "numeric", minute: "2-digit"
    }).format(new Date(timestamp));
}

function searchType(query) {
    const normalized = query.toLowerCase();
    if (/last month|this month|last week|yesterday|when/.test(normalized)) return "Temporal search";
    if (/what did|who|said|say|from|by/.test(normalized)) return "Attributed search";
    return "Semantic search";
}

function rememberSearch(query, answer) {
    const next = [{ query, answer, createdAt: new Date().toISOString() }, ...getHistory().filter((item) => item.query !== query)].slice(0, 12);
    localStorage.setItem(historyKey, JSON.stringify(next));
}

function renderRecent(targetId, emptyText) {
    const target = document.getElementById(targetId);
    const history = getHistory();
    target.innerHTML = history.length ? history.slice(0, 5).map((item) => `<button class="recent-item" onclick="repeatSearch(${JSON.stringify(item.query)})"><span class="recent-symbol">⌕</span><span>${escapeHtml(item.query)}<small>${formatDate(item.createdAt)}</small></span><b>→</b></button>`).join("") : `<p class="muted-copy">${emptyText}</p>`;
}

function renderHome() {
    document.getElementById("metric-searches").textContent = getHistory().length;
    document.getElementById("metric-saved").textContent = getSaved().length;
    renderRecent("home-recent", "Your questions will appear here after your first search.");
}

function renderInsights() {
    renderRecent("history-list", "No recent questions yet.");
    const saved = getSaved();
    document.getElementById("saved-count").textContent = saved.length;
    document.getElementById("saved-list").innerHTML = saved.length ? saved.map((item, index) => `<article class="saved-item"><div class="saved-item-top"><span>Saved answer ${String(index + 1).padStart(2, "0")}</span><button class="icon-button" onclick="removeSaved(${index})" aria-label="Remove saved answer">×</button></div><h4>${escapeHtml(item.query)}</h4><p>${formatAnswer(item.answer)}</p></article>`).join("") : `<p class="muted-copy">Save an answer from search results to keep it here.</p>`;
}

function repeatSearch(query) {
    location.hash = "search";
    queryInput.value = query;
    searchMessages();
}

function saveAnswer(query, answer) {
    const saved = getSaved();
    if (!saved.some((item) => item.query === query)) {
        saved.unshift({ query, answer });
        localStorage.setItem(savedKey, JSON.stringify(saved.slice(0, 20)));
    }
    renderInsights();
}

function removeSaved(index) {
    const saved = getSaved();
    saved.splice(index, 1);
    localStorage.setItem(savedKey, JSON.stringify(saved));
    renderInsights();
}

async function uploadChat() {
    const file = chatFile.files[0];
    if (!file) return;

    uploadStatus.textContent = "Reading your archive...";
    uploadStatus.classList.add("is-loading");
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", { method: "POST", headers: { Authorization: `Bearer ${getAuthToken()}` }, body: formData });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Upload failed");

        activeChatId = data.chat_id;
        document.getElementById("archive-name").textContent = file.name.replace(/\.(txt|json)$/i, "");
        document.getElementById("archive-details").textContent = `${data.message_count.toLocaleString()} messages · ${data.participant_count} people`;
        uploadStatus.textContent = `${data.message_count.toLocaleString()} messages ready`;
        uploadStatus.classList.remove("is-loading");
    } catch (error) {
        uploadStatus.textContent = error.message;
        uploadStatus.classList.remove("is-loading");
        activeChatId = null;
    } finally {
        chatFile.value = "";
    }
}

async function searchMessages() {
    const query = queryInput.value.trim();
    if (!query || searchButton.disabled) return;

    searchButton.disabled = true;
    loading.innerHTML = `<div class="loading-state"><span class="loading-bars"><i></i><i></i><i></i></span> Searching the archive...</div>`;
    resultsDiv.innerHTML = "";

    try {
        const endpoint = new URL("http://127.0.0.1:8000/search");
        if (activeChatId) endpoint.searchParams.set("chat_id", activeChatId);
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${getAuthToken()}` },
            body: JSON.stringify({ query, top_k: 5 })
        });
        if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
        const data = await response.json();
        rememberSearch(query, data.answer || "");
        renderResults(data, query);
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error-state"><strong>Couldn’t reach your archive</strong>Start the FastAPI server at <b>127.0.0.1:8000</b>, then try this search again.</div>`;
    } finally {
        loading.innerHTML = "";
        searchButton.disabled = false;
    }
}

function renderResults(data, query) {
    const results = Array.isArray(data.results) ? data.results : [];
    const answer = data.answer || "I couldn't find enough information in the conversation.";
    const cards = results.map((result, index) => {
        const message = result.message || {};
        const context = Array.isArray(result.context) ? result.context : [];
        return `<article class="result">
            <div class="result-header"><span class="sender">Source ${String(index + 1).padStart(2, "0")} · ${escapeHtml(message.sender)}</span><span class="score">match ${Number(result.score || 0).toFixed(3)}</span></div>
            <div class="result-meta"><span>${formatDate(message.timestamp)}</span><span>·</span><span>message #${escapeHtml(message.id)}</span></div>
            <p class="message">${escapeHtml(message.message)}</p>
            <div class="context"><div class="context-title"><span>Conversation context</span><span>${context.length} messages</span></div>${context.map((item) => `<div class="context-message ${item.id === message.id ? "highlight" : ""}"><strong>${escapeHtml(item.sender)}</strong><span>${escapeHtml(item.message)}</span></div>`).join("")}</div>
        </article>`;
    }).join("");

    resultsDiv.innerHTML = `<div class="results-heading"><h2>What surfaced <span>for you</span></h2><p>${searchType(query)} · ${results.length} sources</p></div>
        <div class="answer"><div class="answer-mark">✦</div><div><div class="answer-label">ChatSense answer <button class="save-button" onclick="saveAnswer(${JSON.stringify(query)}, ${JSON.stringify(answer)})">♡ Save answer</button></div><p>${formatAnswer(answer)}</p></div></div>
        <p class="source-label">Evidence from your conversations</p>${cards || `<div class="empty-state"><h2>No messages surfaced</h2><p>Try asking the same thought in a different way.</p></div>`}`;
    resultsDiv.scrollIntoView({ behavior: "smooth", block: "start" });
}

function useExample(text) {
    location.hash = "search";
    queryInput.value = text;
    queryInput.focus();
    searchMessages();
}

document.getElementById("clear-history").addEventListener("click", () => {
    localStorage.removeItem(historyKey);
    renderInsights();
});

if (getAuthToken()) {
    const savedUser = JSON.parse(sessionStorage.getItem(authUserKey) || "null");
    if (savedUser) setAuthSession({ token: getAuthToken(), user: savedUser });
    else showAuthMode("login");
} else {
    showAuthMode("login");
}