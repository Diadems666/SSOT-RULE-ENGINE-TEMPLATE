/**
 * AI Integration Module for SSOT Rule Engine Dashboard
 * Handles AI chat, rule generation, and knowledge graph integration
 */

class AIIntegration {
    constructor() {
        this.endpoint = '/api/ai';
        this.chatHistory = [];
        this.isProcessing = false;
        this.context = {};
        this.retryCount = 0;
        this.maxRetries = 3;
        this.retryDelay = 1000; // 1 second
        this.initialize();
    }

    async initialize() {
        try {
            // Check initial status
            const status = await this.checkStatus();
            this._updateStatus(status.error ? 'Error: ' + status.error : 'Ready');

            // Setup event listeners
            this._setupEventListeners();

            // Load chat history if available
            await this._loadChatHistory();

            // Initialize Knowledge Graph visualization
            await this._initializeKGVisualization();

        } catch (error) {
            console.error('Initialization failed:', error);
            this._updateStatus('Initialization failed');
        }
    }

    async sendQuery(query, retryCount = 0) {
        if (this.isProcessing) return;

        try {
            this.isProcessing = true;
            this._updateStatus('Processing...');
            this._showTypingIndicator();

            const response = await fetch(`${this.endpoint}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    query,
                    context: this.context
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (!data.success && retryCount < this.maxRetries) {
                // Retry with exponential backoff
                await new Promise(resolve => setTimeout(resolve, this.retryDelay * Math.pow(2, retryCount)));
                return this.sendQuery(query, retryCount + 1);
            }

            // Update chat history and context
            this.chatHistory.push({
                id: Date.now().toString(),
                query,
                response: data.response,
                context: data.context,
                confidence: data.confidence,
                timestamp: new Date()
            });

            // Update context for next query
            this.context = {
                ...this.context,
                ...data.context
            };

            this._updateStatus('Ready');
            this._updateChatDisplay();
            this._hideTypingIndicator();
            this._saveChatHistory();

            return data;

        } catch (error) {
            console.error('AI query failed:', error);
            this._updateStatus('Error: ' + error.message);
            this._hideTypingIndicator();
            throw error;
        } finally {
            this.isProcessing = false;
        }
    }

    async generateRule(description) {
        try {
            const response = await fetch(`${this.endpoint}/generate-rule`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ description })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to generate rule:', error);
            throw error;
        }
    }

    async submitFeedback(feedback, queryId) {
        try {
            const response = await fetch(`${this.endpoint}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ feedback, query_id: queryId })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to submit feedback:', error);
            throw error;
        }
    }

    async checkStatus() {
        try {
            const response = await fetch(`${this.endpoint}/status`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const status = await response.json();
            this._updateStatusIndicator(status);
            return status;
        } catch (error) {
            console.error('Failed to check AI status:', error);
            this._updateStatusIndicator({ error: error.message });
            return { error: error.message };
        }
    }

    _setupEventListeners() {
        // Chat form submission
        const form = document.getElementById('ai-chat-form');
        const input = document.getElementById('ai-chat-input');

        if (form && input) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const query = input.value.trim();
                if (!query) return;

                try {
                    input.value = '';
                    input.disabled = true;
                    await this.sendQuery(query);
                } catch (error) {
                    console.error('Failed to send query:', error);
                } finally {
                    input.disabled = false;
                    input.focus();
                }
            });
        }

        // Feedback buttons
        document.addEventListener('click', async (e) => {
            if (e.target.classList.contains('feedback-btn')) {
                const queryId = e.target.dataset.queryId;
                const feedback = e.target.dataset.feedback;
                try {
                    await this.submitFeedback(feedback, queryId);
                    this._updateFeedbackUI(queryId, feedback);
                } catch (error) {
                    console.error('Failed to submit feedback:', error);
                }
            }
        });
    }

    async _loadChatHistory() {
        const saved = localStorage.getItem('aiChatHistory');
        if (saved) {
            this.chatHistory = JSON.parse(saved).map(chat => ({
                ...chat,
                timestamp: new Date(chat.timestamp)
            }));
            this._updateChatDisplay();
        }
    }

    _saveChatHistory() {
        localStorage.setItem('aiChatHistory', JSON.stringify(this.chatHistory));
    }

    async _initializeKGVisualization() {
        try {
            const response = await fetch(`${this.endpoint}/kg/visualize`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this._updateKGVisualization(data);
        } catch (error) {
            console.error('Failed to initialize KG visualization:', error);
        }
    }

    _updateStatus(message) {
        const statusElement = document.getElementById('ai-status');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    _updateStatusIndicator(status) {
        const indicator = document.getElementById('ai-status-indicator');
        if (indicator) {
            indicator.className = 'status-indicator ' + 
                (status.error ? 'error' : 
                 status.model_loaded ? 'active' : 'inactive');
            indicator.title = status.error ? status.error : 
                            status.model_loaded ? 'AI system active' : 'AI system inactive';
        }
    }

    _showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        
        const chat = document.getElementById('ai-chat-history');
        if (chat) {
            chat.appendChild(indicator);
            chat.scrollTop = chat.scrollHeight;
        }
    }

    _hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    _updateChatDisplay() {
        const chatElement = document.getElementById('ai-chat-history');
        if (!chatElement) return;

        chatElement.innerHTML = this.chatHistory
            .map(chat => `
                <div class="chat-entry" data-query-id="${chat.id}">
                    <div class="query">
                        <span class="label">Q:</span>
                        <span class="content">${this._escapeHtml(chat.query)}</span>
                    </div>
                    <div class="response">
                        <span class="label">A:</span>
                        <span class="content">${this._escapeHtml(chat.response)}</span>
                        <div class="metadata">
                            <span class="confidence">Confidence: ${(chat.confidence * 100).toFixed(1)}%</span>
                            <span class="timestamp">${chat.timestamp.toLocaleString()}</span>
                        </div>
                    </div>
                    <div class="feedback">
                        <button class="feedback-btn" data-query-id="${chat.id}" data-feedback="helpful">👍 Helpful</button>
                        <button class="feedback-btn" data-query-id="${chat.id}" data-feedback="not_helpful">👎 Not Helpful</button>
                    </div>
                </div>
            `)
            .join('');

        chatElement.scrollTop = chatElement.scrollHeight;
    }

    _updateFeedbackUI(queryId, feedback) {
        const chatEntry = document.querySelector(`.chat-entry[data-query-id="${queryId}"]`);
        if (chatEntry) {
            const buttons = chatEntry.querySelectorAll('.feedback-btn');
            buttons.forEach(btn => {
                btn.disabled = true;
                if (btn.dataset.feedback === feedback) {
                    btn.classList.add('selected');
                }
            });
        }
    }

    _updateKGVisualization(data) {
        const container = document.getElementById('kg-visualization');
        if (!container) return;

        // Implement visualization using your preferred library
        // (e.g., D3.js, vis.js, or Cytoscape.js)
        console.log('KG visualization data:', data);
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

// Export for global access
window.aiIntegration = ai; 