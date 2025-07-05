// AI Integration for SSOT Rule Engine Dashboard

class AIIntegration {
    constructor() {
        this.initializeAI();
        this.setupEventListeners();
    }

    initializeAI() {
        // Initialize AI components
        this.ruleGenerator = new RuleGenerator();
        this.documentationGenerator = new DocumentationGenerator();
        this.mcpEnhancer = new MCPEnhancer();
        this.codebaseAnalyzer = new CodebaseAnalyzer();
    }

    setupEventListeners() {
        // AI-assisted rule generation
        document.getElementById('ai-generate-rule').addEventListener('click', async () => {
            const context = this.gatherRuleContext();
            const loadingToast = showToast('Generating rule...', 'info', -1);
            
            try {
                const response = await fetch('/ai/generate-rule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(context)
                });
                
                const data = await response.json();
                if (data.success) {
                    this.ruleGenerator.displayRule(data.rule);
                    loadingToast.remove();
                    showToast('Rule generated successfully', 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                loadingToast.remove();
                showToast(`Failed to generate rule: ${error.message}`, 'error');
            }
        });

        // AI-assisted documentation generation
        document.getElementById('ai-generate-docs').addEventListener('click', async () => {
            const ruleConfig = this.gatherRuleConfig();
            const loadingToast = showToast('Generating documentation...', 'info', -1);
            
            try {
                const response = await fetch('/ai/generate-docs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(ruleConfig)
                });
                
                const data = await response.json();
                if (data.success) {
                    this.documentationGenerator.displayDocs(data.documentation);
                    loadingToast.remove();
                    showToast('Documentation generated successfully', 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                loadingToast.remove();
                showToast(`Failed to generate documentation: ${error.message}`, 'error');
            }
        });

        // AI-enhanced MCP memory
        document.getElementById('ai-enhance-memory').addEventListener('click', async () => {
            const memoryEntry = this.gatherMemoryEntry();
            const loadingToast = showToast('Enhancing memory...', 'info', -1);
            
            try {
                const response = await fetch('/ai/enhance-memory', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(memoryEntry)
                });
                
                const data = await response.json();
                if (data.success) {
                    this.mcpEnhancer.updateMemory(data.enhanced_memory);
                    loadingToast.remove();
                    showToast('Memory enhanced successfully', 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                loadingToast.remove();
                showToast(`Failed to enhance memory: ${error.message}`, 'error');
            }
        });

        // AI codebase analysis
        document.getElementById('ai-analyze-codebase').addEventListener('click', async () => {
            const paths = this.gatherAnalysisPaths();
            const loadingToast = showToast('Analyzing codebase...', 'info', -1);
            
            try {
                const response = await fetch('/ai/analyze-codebase', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ paths })
                });
                
                const data = await response.json();
                if (data.success) {
                    this.codebaseAnalyzer.displayAnalysis(data.analysis);
                    loadingToast.remove();
                    showToast('Analysis completed successfully', 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                loadingToast.remove();
                showToast(`Failed to analyze codebase: ${error.message}`, 'error');
            }
        });
    }

    gatherRuleContext() {
        return {
            name: document.getElementById('rule-name').value,
            description: document.getElementById('rule-description').value,
            template: document.getElementById('rule-template').value,
            language: document.getElementById('rule-language').value,
            projectContext: this.getProjectContext()
        };
    }

    gatherRuleConfig() {
        const rulePreview = document.getElementById('rule-preview');
        return {
            name: rulePreview.getAttribute('data-name'),
            content: rulePreview.textContent,
            language: rulePreview.getAttribute('data-language'),
            template: rulePreview.getAttribute('data-template')
        };
    }

    gatherMemoryEntry() {
        const selectedNode = document.querySelector('.node.selected');
        return {
            id: selectedNode?.getAttribute('data-id'),
            type: selectedNode?.getAttribute('data-type'),
            content: selectedNode?.getAttribute('data-content')
        };
    }

    gatherAnalysisPaths() {
        // Get selected paths from file tree or use default project paths
        const selectedPaths = Array.from(document.querySelectorAll('.file-tree .selected'))
            .map(el => el.getAttribute('data-path'));
        return selectedPaths.length > 0 ? selectedPaths : ['.'];
    }

    getProjectContext() {
        return {
            rootDir: document.body.getAttribute('data-project-root'),
            activeBranch: document.body.getAttribute('data-git-branch'),
            recentFiles: this.getRecentFiles()
        };
    }

    getRecentFiles() {
        return Array.from(document.querySelectorAll('.recent-files .file'))
            .map(el => ({
                path: el.getAttribute('data-path'),
                lastModified: el.getAttribute('data-modified')
            }));
    }
}

class RuleGenerator {
    displayRule(rule) {
        const preview = document.getElementById('rule-preview');
        preview.textContent = rule.template;
        preview.setAttribute('data-name', rule.name);
        preview.setAttribute('data-language', rule.language);
        preview.setAttribute('data-template', rule.template);

        // Add to rule list
        const ruleList = document.getElementById('rule-list');
        const ruleItem = document.createElement('div');
        ruleItem.className = 'rule-item';
        ruleItem.innerHTML = `
            <span>${rule.name}</span>
            <div class="rule-actions">
                <button onclick="copyRule(this)">Copy</button>
                <button onclick="saveRule(this)">Save</button>
                <button onclick="deleteRule(this)">Delete</button>
                <button onclick="generateDocs(this)">Generate Docs</button>
            </div>
        `;
        ruleList.appendChild(ruleItem);
    }
}

class DocumentationGenerator {
    displayDocs(documentation) {
        const docsContainer = document.getElementById('documentation-container');
        docsContainer.innerHTML = marked(documentation);
        
        // Update table of contents
        const toc = this.generateTOC(documentation);
        document.getElementById('docs-toc').innerHTML = toc;
    }

    generateTOC(markdown) {
        const headings = markdown.match(/#{1,6}.+/g) || [];
        return headings.map(heading => {
            const level = heading.match(/^#+/)[0].length;
            const text = heading.replace(/^#+\s*/, '');
            return `<div class="toc-item level-${level}">${text}</div>`;
        }).join('');
    }
}

class MCPEnhancer {
    updateMemory(enhancedMemory) {
        // Update Knowledge Graph visualization
        network.updateNode({
            id: enhancedMemory.id,
            label: enhancedMemory.label,
            title: enhancedMemory.description,
            color: this.getNodeColor(enhancedMemory.type)
        });

        // Update node details panel
        this.updateNodeDetails(enhancedMemory);
    }

    getNodeColor(type) {
        const colors = {
            file: '#27ae60',
            function: '#2980b9',
            class: '#8e44ad',
            module: '#c0392b',
            package: '#d35400'
        };
        return colors[type] || '#95a5a6';
    }

    updateNodeDetails(memory) {
        const detailsPanel = document.getElementById('node-details');
        detailsPanel.innerHTML = `
            <h3>${memory.label}</h3>
            <div class="details-content">
                <p><strong>Type:</strong> ${memory.type}</p>
                <p><strong>Description:</strong> ${memory.description}</p>
                <div class="relationships">
                    <h4>Relationships</h4>
                    ${this.formatRelationships(memory.relationships)}
                </div>
                <div class="metadata">
                    <h4>Metadata</h4>
                    ${this.formatMetadata(memory.metadata)}
                </div>
            </div>
        `;
    }

    formatRelationships(relationships) {
        return relationships.map(rel => `
            <div class="relationship-item">
                <span class="rel-type">${rel.type}</span>
                <span class="rel-target">${rel.target}</span>
            </div>
        `).join('');
    }

    formatMetadata(metadata) {
        return Object.entries(metadata).map(([key, value]) => `
            <div class="metadata-item">
                <span class="meta-key">${key}:</span>
                <span class="meta-value">${value}</span>
            </div>
        `).join('');
    }
}

class CodebaseAnalyzer {
    displayAnalysis(analysis) {
        const analysisContainer = document.getElementById('analysis-container');
        
        // Display suggested rules
        const rulesList = analysis.suggestedRules.map(rule => `
            <div class="suggested-rule">
                <h4>${rule.name}</h4>
                <p>${rule.description}</p>
                <div class="rule-context">
                    <strong>Context:</strong>
                    <pre><code>${rule.context}</code></pre>
                </div>
                <button onclick="applyRule('${rule.id}')" class="btn btn-primary">Apply Rule</button>
            </div>
        `).join('');

        // Display documentation needs
        const docsList = analysis.documentationNeeds.map(doc => `
            <div class="doc-need">
                <h4>${doc.title}</h4>
                <p>${doc.description}</p>
                <button onclick="generateDocumentation('${doc.id}')" class="btn btn-secondary">
                    Generate Documentation
                </button>
            </div>
        `).join('');

        analysisContainer.innerHTML = `
            <div class="analysis-section">
                <h3>Suggested Rules</h3>
                <div class="suggested-rules">${rulesList}</div>
            </div>
            <div class="analysis-section">
                <h3>Documentation Needs</h3>
                <div class="documentation-needs">${docsList}</div>
            </div>
        `;
    }
}

// Initialize AI integration when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    window.aiIntegration = new AIIntegration();
}); 