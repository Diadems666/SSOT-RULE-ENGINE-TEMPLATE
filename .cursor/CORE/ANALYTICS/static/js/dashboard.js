/**
 * Main Dashboard Module for SSOT Rule Engine
 */

class Dashboard {
    constructor() {
        this.healthCheckInterval = 30000; // 30 seconds
        this.ruleEngineCheckInterval = 30000;
        this.settings = this._loadSettings();
        this.intervals = [];
    }

    async initialize() {
        try {
            // Initialize components
            await this._initializeHealth();
            await this._initializeRuleEngine();
            this._initializeSettings();
            this._initializeTheme();
            this._setupIntervals();
            this._setupEventListeners();

        } catch (error) {
            console.error('Failed to initialize dashboard:', error);
            this._showError('Failed to initialize dashboard: ' + error.message);
        }
    }

    async _initializeHealth() {
        try {
            const response = await fetch('/api/health');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this._updateHealthDisplay(data);

        } catch (error) {
            console.error('Failed to initialize health:', error);
            throw error;
        }
    }

    async _initializeRuleEngine() {
        try {
            const response = await fetch('/api/rule-engine/status');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this._updateRuleEngineDisplay(data);

        } catch (error) {
            console.error('Failed to initialize rule engine:', error);
            throw error;
        }
    }

    _initializeSettings() {
        // Load saved settings
        const savedSettings = localStorage.getItem('dashboardSettings');
        if (savedSettings) {
            this.settings = { ...this.settings, ...JSON.parse(savedSettings) };
        }

        // Apply settings
        document.getElementById('theme-select').value = this.settings.theme;
        document.getElementById('refresh-interval').value = this.settings.refreshInterval;
        document.getElementById('notifications-enabled').checked = this.settings.notificationsEnabled;
    }

    _initializeTheme() {
        document.documentElement.setAttribute('data-theme', this.settings.theme);
    }

    _setupIntervals() {
        // Clear existing intervals
        this.intervals.forEach(clearInterval);
        this.intervals = [];

        // Setup new intervals
        this.intervals.push(
            setInterval(() => this._initializeHealth(), this.healthCheckInterval),
            setInterval(() => this._initializeRuleEngine(), this.ruleEngineCheckInterval)
        );
    }

    _setupEventListeners() {
        // Settings form
        document.getElementById('settings-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this._saveSettings();
        });

        // Settings toggle
        document.getElementById('settings-toggle').addEventListener('click', () => {
            const modal = new bootstrap.Modal(document.getElementById('settings-modal'));
            modal.show();
        });

        // Save settings
        document.getElementById('save-settings').addEventListener('click', () => {
            this._saveSettings();
            bootstrap.Modal.getInstance(document.getElementById('settings-modal')).hide();
        });
    }

    _updateHealthDisplay(data) {
        // Update score
        const scoreElement = document.getElementById('health-score');
        if (scoreElement) {
            scoreElement.textContent = Math.round(data.score);
            scoreElement.className = this._getHealthClass(data.score);
        }

        // Update details
        const detailsElement = document.getElementById('health-details');
        if (detailsElement) {
            detailsElement.innerHTML = this._generateHealthHTML(data);
        }

        // Show notification if needed
        if (this.settings.notificationsEnabled && data.score < 70) {
            this._showNotification('Health Warning', `System health score is ${data.score}`);
        }
    }

    _updateRuleEngineDisplay(data) {
        const element = document.getElementById('rule-engine-status');
        if (!element) return;

        element.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="mb-0">Status: ${this._escapeHtml(data.status)}</h6>
                <span class="badge ${data.status === 'operational' ? 'bg-success' : 'bg-warning'}">
                    ${this._escapeHtml(data.status)}
                </span>
            </div>
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Rule ID</th>
                            <th>Name</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.active_rules.map(rule => `
                            <tr>
                                <td>${this._escapeHtml(rule.id)}</td>
                                <td>${this._escapeHtml(rule.name)}</td>
                                <td>
                                    <span class="badge ${rule.status === 'active' ? 'bg-success' : 'bg-secondary'}">
                                        ${this._escapeHtml(rule.status)}
                                    </span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <small class="text-muted">Last updated: ${new Date(data.last_update).toLocaleString()}</small>
        `;
    }

    _generateHealthHTML(data) {
        return `
            <div class="list-group">
                ${Object.entries(data.components).map(([name, info]) => `
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">${this._escapeHtml(name)}</h6>
                            <span class="badge ${this._getHealthClass(info.score)}">
                                ${Math.round(info.score)}
                            </span>
                        </div>
                        <small class="text-muted">${this._escapeHtml(info.message)}</small>
                    </div>
                `).join('')}
            </div>
            <small class="text-muted mt-2 d-block">
                Last updated: ${new Date(data.timestamp).toLocaleString()}
            </small>
        `;
    }

    _getHealthClass(score) {
        if (score >= 90) return 'bg-success';
        if (score >= 70) return 'bg-warning';
        return 'bg-danger';
    }

    _saveSettings() {
        const newSettings = {
            theme: document.getElementById('theme-select').value,
            refreshInterval: parseInt(document.getElementById('refresh-interval').value),
            notificationsEnabled: document.getElementById('notifications-enabled').checked
        };

        // Update settings
        this.settings = { ...this.settings, ...newSettings };
        localStorage.setItem('dashboardSettings', JSON.stringify(this.settings));

        // Apply changes
        this._initializeTheme();
        this._setupIntervals();
        this._showToast('Settings saved successfully');
    }

    _loadSettings() {
        return {
            theme: 'light',
            refreshInterval: 30,
            notificationsEnabled: true
        };
    }

    _showNotification(title, message) {
        if (!("Notification" in window)) return;

        if (Notification.permission === "granted") {
            new Notification(title, { body: message });
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    new Notification(title, { body: message });
                }
            });
        }
    }

    _showToast(message) {
        const toastHTML = `
            <div class="toast" role="alert">
                <div class="toast-body">${this._escapeHtml(message)}</div>
            </div>
        `;

        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = new bootstrap.Toast(toastContainer.appendChild(
            document.createRange().createContextualFragment(toastHTML).firstElementChild
        ));
        toast.show();
    }

    _showError(message) {
        console.error(message);
        this._showToast('Error: ' + message);
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

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const dashboard = new Dashboard();
        await dashboard.initialize();
    } catch (error) {
        console.error('Failed to setup dashboard:', error);
    }
});
    