const queryInput = document.getElementById("query");
const searchButton = document.getElementById("search-button");
const resultsDiv = document.getElementById("results");
const loading = document.getElementById("loading");

queryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") searchMessages();
});

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

async function searchMessages() {
    const query = queryInput.value.trim();
    if (!query || searchButton.disabled) return;

    searchButton.disabled = true;
    loading.innerHTML = `<div class="loading-state"><span class="loading-bars"><i></i><i></i><i></i></span> Searching the archive...</div>`;
    resultsDiv.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, top_k: 5 })
        });
        if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
        const data = await response.json();
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
        <div class="answer"><div class="answer-mark">✦</div><div><div class="answer-label">ChatSense answer</div><p>${formatAnswer(data.answer || "I couldn't find enough information in the conversation.")}</p></div></div>
        <p class="source-label">Evidence from your conversations</p>${cards || `<div class="empty-state"><h2>No messages surfaced</h2><p>Try asking the same thought in a different way.</p></div>`}`;
    resultsDiv.scrollIntoView({ behavior: "smooth", block: "start" });
}

function useExample(text) {
    queryInput.value = text;
    queryInput.focus();
    searchMessages();
}