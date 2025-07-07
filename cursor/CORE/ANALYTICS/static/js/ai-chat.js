// AI Chat Interface

class AIChatInterface {
    constructor() {
        this.chatContainer = document.getElementById('ai-chat-container');
        this.messageList = document.getElementById('ai-messages');
        this.inputForm = document.getElementById('ai-input-form');
        this.inputField = document.getElementById('ai-input');
        this.context = {};
        
        this.initialize();
    }

    initialize() {
        // Initialize event listeners
        this.inputForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Initialize chat container if needed
        if (!this.chatContainer) {
            this.createChatInterface();
        }

        // Get initial AI status
        this.checkAIStatus();
    }

    createChatInterface() {
        // Create chat container
        this.chatContainer = document.createElement('div');
        this.chatContainer.id = 'ai-chat-container';
        this.chatContainer.className = 'chat-container';

        // Create message list
        this.messageList = document.createElement('div');
        this.messageList.id = 'ai-messages';
        this.messageList.className = 'message-list';

        // Create input form
        this.inputForm = document.createElement('form');
        this.inputForm.id = 'ai-input-form';
        this.inputForm.className = 'input-form';

        // Create input field
        this.inputField = document.createElement('input');
        this.inputField.id = 'ai-input';
        this.inputField.type = 'text';
        this.inputField.placeholder = 'Ask me anything...';
        this.inputField.className = 'input-field';

        // Create send button
        const sendButton = document.createElement('button');
        sendButton.type = 'submit';
        sendButton.textContent = 'Send';
        sendButton.className = 'send-button';

        // Assemble the interface
        this.inputForm.appendChild(this.inputField);
        this.inputForm.appendChild(sendButton);
        this.chatContainer.appendChild(this.messageList);
        this.chatContainer.appendChild(this.inputForm);

        // Add to page
        document.body.appendChild(this.chatContainer);
    }

    async sendMessage() {
        const message = this.inputField.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage('user', message);
        this.inputField.value = '';

        try {
            const response = await fetch('/api/ai/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: message })
            });

            const data = await response.json();
            
            if (data.error) {
                this.addMessage('error', `Error: ${data.error}`);
            } else {
                this.addMessage('ai', data.response);
                if (data.context) {
                    this.context = data.context;
                }
            }
        } catch (error) {
            this.addMessage('error', `Error: ${error.message}`);
        }
    }

    addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentP = document.createElement('p');
        contentP.textContent = content;
        messageDiv.appendChild(contentP);

        this.messageList.appendChild(messageDiv);
        this.messageList.scrollTop = this.messageList.scrollHeight;
    }

    async checkAIStatus() {
        try {
            const response = await fetch('/api/ai/status');
            const data = await response.json();
            
            if (data.error) {
                console.error('AI Status Error:', data.error);
            } else {
                console.log('AI Status:', data);
            }
        } catch (error) {
            console.error('Error checking AI status:', error);
        }
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiChat = new AIChatInterface();
}); 