/**
 * AI Integration Module for SSOT Rule Engine Dashboard
 */

class AIIntegration {
    constructor() {
        this.endpoint = '/api/ai';
        this.chatHistory = [];
        this.isProcessing = false;
    }

    async sendQuery(query) {
        try {
            this.isProcessing = true;
            this._updateStatus('Processing...');

            const response = await fetch(`${this.endpoint}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.chatHistory.push({
                query,
                response: data.response,
                timestamp: new Date()
            });

            this._updateStatus('Ready');
            this._updateChatDisplay();
            return data;

        } catch (error) {
            console.error('AI query failed:', error);
            this._updateStatus('Error: ' + error.message);
            throw error;
        } finally {
            this.isProcessing = false;
        }
    }

    async checkStatus() {
        try {
            const response = await fetch(`${this.endpoint}/status`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Failed to check AI status:', error);
            return { error: error.message };
        }
    }

    _updateStatus(message) {
        const statusElement = document.getElementById('ai-status');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    _updateChatDisplay() {
        const chatElement = document.getElementById('ai-chat-history');
        if (!chatElement) return;

        chatElement.innerHTML = this.chatHistory
            .map(chat => `
                <div class="chat-entry">
                    <div class="query">Q: ${this._escapeHtml(chat.query)}</div>
                    <div class="response">A: ${this._escapeHtml(chat.response.answer)}</div>
                    <div class="timestamp">${chat.timestamp.toLocaleString()}</div>
                </div>
            `)
            .join('');
    }

    _escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Initialize AI integration
const ai = new AIIntegration();

// Setup chat form handler
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('ai-chat-form');
    const input = document.getElementById('ai-chat-input');

    if (form && input) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const query = input.value.trim();
            if (!query) return;

            try {
                input.value = '';
                await ai.sendQuery(query);
            } catch (error) {
                console.error('Failed to send query:', error);
            }
        });
    }
});

// Export for global access
window.aiIntegration = ai; 