async function searchMessages() {

    const query = document.getElementById("query").value.trim();

    if (!query) return;

    const resultsDiv = document.getElementById("results");
    const loading = document.getElementById("loading");

    loading.innerText = "Searching...";
    resultsDiv.innerHTML = "";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/search",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    query: query,
                    top_k: 5
                })
            }
        );

        const data = await response.json();

        loading.innerText = "";

        // AI ANSWER
        resultsDiv.innerHTML = `
            <div class="answer">
                <h2>🤖 Answer</h2>
                <p>${data.answer}</p>
            </div>

            <h2>📚 Sources</h2>
        `;

        // SOURCES
        data.results.forEach((result, index) => {

            const div = document.createElement("div");

            div.className = "result";

            div.innerHTML = `
                <div class="result-header">
                    <span class="sender">
                        Source ${index + 1} — ${result.message.sender}
                    </span>

                    <span class="score">
                        Similarity: ${result.score.toFixed(3)}
                    </span>
                </div>

                <div class="message">
                    ${result.message.message}
                </div>

                <div class="context">
                    <strong>Conversation Context</strong>

                    ${result.context.map(msg => `
                        <div class="context-message">
                            <strong>${msg.sender}:</strong>
                            ${msg.message}
                        </div>
                    `).join("")}
                </div>
            `;

            resultsDiv.appendChild(div);
        });

    } catch (error) {

        loading.innerText = "";

        resultsDiv.innerHTML =
            "<p>❌ Could not connect to backend.</p>";
    }
}


function useExample(text) {
    document.getElementById("query").value = text;
    searchMessages();
}