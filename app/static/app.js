document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form");
    const promptInput = document.getElementById("prompt");
    const chatHistory = document.getElementById("chat-history");
    const conversationList = document.getElementById("conversation-list");
    const newConvoBtn = document.getElementById("new-convo-btn");

    let messages = [];
    let currentChatId = null;
    const SESSION_ID = "4A73CB69-FA33-4022-B9C2-B1E9C859C9CC";

    // Adiciona DOMPurify via CDN
    const domPurifyScript = document.createElement('script');
    domPurifyScript.src = 'https://cdn.jsdelivr.net/npm/dompurify@3.0.8/dist/purify.min.js';
    domPurifyScript.defer = true;
    document.head.appendChild(domPurifyScript);

    function appendMessage(role, content) {
        const wrapper = document.createElement("div");
        wrapper.className = `d-flex mb-3 ${role === "user" ? "justify-content-end" : "justify-content-start"}`;
        if (role === "user") {
            wrapper.innerHTML = `
      <div class="p-3 rounded-4 shadow-sm bg-primary text-white" style="max-width: 80%;">
        ${escapeHTML(content)}
      </div>
    `;
        } else {
            const rawMarkdown = marked.parse(content, { breaks: true, gfm: true });
            const safeMarkdown = window.DOMPurify ? window.DOMPurify.sanitize(rawMarkdown) : rawMarkdown;
            wrapper.innerHTML = `
      <div class="p-3 rounded-4 shadow-sm bg-light text-dark markdown-body" style="max-width: 80%;">
        ${safeMarkdown}
      </div>
    `;
        }
        chatHistory.appendChild(wrapper);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function clearChatUI() {
        messages = [];
        chatHistory.innerHTML = "";
        promptInput.value = "";
        promptInput.focus();
    }

    async function createNewChat() {
        try {
            const res = await fetch('/api/new_chat', {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: SESSION_ID })
            });
            const data = await res.json();
            if (data.error) throw new Error(data.error);
            return data.chat_id;
        } catch (err) {
            console.error("Failed to create new chat:", err);
            return null;
        }
    }

    async function loadConversations() {
        conversationList.innerHTML = "";
        try {
            const res = await fetch(`/api/conversations?session_id=${SESSION_ID}`);
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            const chats = await res.json();
            if (!Array.isArray(chats) || chats.length === 0) {
                const noChatsEl = document.createElement("li");
                noChatsEl.textContent = "No conversations found.";
                noChatsEl.className = "text-muted";
                conversationList.appendChild(noChatsEl);
                return;
            }
            chats.forEach(chat => {
                const li = document.createElement("li");
                li.className = "mb-2";
                const safeTitle = escapeHTML(chat.chat_title || chat.chat_id);
                li.innerHTML = `<button class="btn btn-outline-light w-100 rounded-pill">${safeTitle}</button>`;
                const btn = li.querySelector("button");
                btn.addEventListener("click", () => loadChat(chat.chat_id));
                conversationList.appendChild(li);
            });
        } catch (err) {
            console.error("Error loading conversations:", err);
            const errorEl = document.createElement("li");
            errorEl.textContent = `Error loading conversations: ${err.message}`;
            errorEl.className = "text-danger";
            conversationList.appendChild(errorEl);
        }
    }

    async function loadChat(chatId) {
        if (!chatId) return;
        currentChatId = chatId;
        clearChatUI();
        try {
            const res = await fetch(`/chat/${chatId}?session_id=${SESSION_ID}`);
            const data = await res.json();
            if (data.error) throw new Error(data.error);
            (data.messages || []).forEach(msg => {
                const role = msg.speaker === "user" ? "user" : "assistant";
                messages.push({ role, content: msg.message });
                appendMessage(role, msg.message);
            });
        } catch (err) {
            console.error("Failed to load chat:", err);
        }
    }

    async function sendMessage(messageText) {
        const sendBtn = form.querySelector('button[type="submit"]');
        if (sendBtn) sendBtn.disabled = true;
        if (!currentChatId) {
            currentChatId = await createNewChat();
            if (!currentChatId) {
                if (sendBtn) sendBtn.disabled = false;
                return;
            }
            await loadConversations();
        }
        messages.push({ role: "user", content: messageText });
        appendMessage("user", messageText);
        promptInput.value = "";
        const thinkingEl = document.createElement("div");
        thinkingEl.className = "d-flex mb-3 justify-content-start";
        thinkingEl.innerHTML = `
      <div class="p-3 rounded-4 shadow-sm bg-light text-dark markdown-body" style="max-width: 80%;">
        _Thinking_
      </div>
    `;
        chatHistory.appendChild(thinkingEl);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        try {
            const lastMessages = messages.slice(-5);
            const res = await fetch(`/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    messages: lastMessages,
                    chat_id: currentChatId,
                    session_id: SESSION_ID
                })
            });
            const data = await res.json();
            const response = data.response || "*[Empty response]*";
            messages.push({ role: "assistant", content: response });
            thinkingEl.innerHTML = `
        <div class="p-3 rounded-4 shadow-sm bg-light text-dark markdown-body" style="max-width: 80%;">
          ${marked.parse(response)}
        </div>
      `;
        } catch (err) {
            console.error("Chat error:", err);
            thinkingEl.innerHTML = `
        <div class="p-3 rounded-4 shadow-sm bg-danger text-white" style="max-width: 80%;">
          Error: ${escapeHTML(err.message)}
        </div>
      `;
        } finally {
            if (sendBtn) sendBtn.disabled = false;
        }
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, function(tag) {
            const chars = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            };
            return chars[tag] || tag;
        });
    }

    newConvoBtn.addEventListener("click", async () => {
        clearChatUI();
        currentChatId = await createNewChat();
        if (currentChatId) await loadConversations();
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userMessage = promptInput.value.trim();
        if (!userMessage) return;
        await sendMessage(userMessage);
    });

    promptInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            form.requestSubmit();
        }
    });

    loadConversations();
});
