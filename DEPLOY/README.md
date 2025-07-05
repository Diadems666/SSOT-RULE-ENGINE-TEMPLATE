# SSOT Rule Engine Template

A comprehensive template for integrating the SSOT Rule Engine system into new or existing projects. This template provides a complete analytics dashboard, Knowledge Graph visualization, and rule management interface.

## Features

### Analytics Dashboard
- Real-time project health monitoring (0-100 scoring)
- Interactive visualizations and metrics
- System status indicators
- Performance tracking
- Error monitoring

### Knowledge Graph Visualization
- Interactive graph visualization using vis.js
- Entity and relationship management
- Type-based color coding
- Advanced search and filtering
- Graph analytics tools
- MCP persistence integration

### Rule Engine Interface
- Visual rule management
- Rule template system
- Rule effectiveness tracking
- Custom rule creation
- Rule impact analysis

### SSOT System
- Centralized project state management
- History tracking
- Context awareness
- Progress monitoring
- Fact management

### MCP Integration
- Knowledge Graph server
- Sequential Thinking server
- Filesystem server
- Memory persistence
- Real-time updates

## Requirements

- Python 3.8+
- Node.js 14+
- Git
- PowerShell (Windows) or Bash (Unix)

## Quick Start

### Windows
```powershell
# Clone the template
git clone https://github.com/your-org/ssot-rule-engine-template.git

# Run deployment script
cd ssot-rule-engine-template
.\DEPLOY\deploy.ps1 "C:\path\to\your\project"
```

### Unix/Linux/macOS
```bash
# Clone the template
git clone https://github.com/your-org/ssot-rule-engine-template.git

# Run deployment script
cd ssot-rule-engine-template
./DEPLOY/deploy.sh /path/to/your/project
```

## Manual Installation

1. Copy the template structure to your project:
   ```
   .cursor/
     CORE/
       RULE-ENGINE/
       ANALYTICS/
       SSOT/
       MCP/
   ```

2. Install Python dependencies:
   ```bash
   pip install -r DEPLOY/requirements.txt
   ```

3. Configure MCP:
   - Copy `mcp.json` to your project root
   - Update settings as needed

4. Initialize the system:
   ```
   !!-ADD-.ENGINE-!!
   ```

5. Install MCP servers:
   ```
   !!-INSTALL-MCP-!!
   ```

6. Build Knowledge Graph:
   ```
   !!-BUILD-KG-!!
   ```

## Usage

### Launch Dashboard
```bash
python launch-dashboard.py
```
Access at http://localhost:5000

### Core Commands
- `!!-INIT-.ENGINE-!!` - Initialize new project
- `!!-ADD-.ENGINE-!!` - Add to existing project
- `!!-INSTALL-MCP-!!` - Install MCP servers
- `!!-BUILD-KG-!!` - Build Knowledge Graph
- `!!-LAUNCH-DASHBOARD-!!` - Launch analytics
- `!!-ANALYZE-PROJECT-!!` - Run analysis
- `!!-VIEW-DASHBOARD-!!` - Open dashboard
- `!!-HEALTH-CHECK-!!` - Quick health check

## Directory Structure

```
.cursor/
  CORE/
    RULE-ENGINE/           # Rule engine components
      rule_generator.py
      engine_integration.py
      templates/
      config.json
    ANALYTICS/             # Dashboard components
      static/
        css/
          dashboard.css
          kg-visualizer.css
        js/
          dashboard.js
          kg-visualizer.js
      templates/
        dashboard.html
      api/
        kg_routes.py
      services/
        kg_service.py
      config.json
    SSOT/                  # SSOT system files
      .ENGINE
      .INIT
      .HISTORY
      .CONTEXT
      .FACTS
      .MEMORY
      .PROGRESS
    MCP/                   # MCP server files
```

## Configuration

### MCP Configuration
Edit `mcp.json` to configure:
- Server endpoints
- WebSocket settings
- Memory persistence
- Client options

### Rule Engine Configuration
Edit `.cursor/CORE/RULE-ENGINE/config.json` to set:
- Rule templates
- Generation settings
- Integration options
- Language support

### Analytics Configuration
Edit `.cursor/CORE/ANALYTICS/config.json` to configure:
- Dashboard settings
- Visualization options
- Metrics collection
- Update intervals

## Development

### Adding New Rules
1. Create rule template in `.cursor/CORE/RULE-ENGINE/templates/`
2. Update rule configuration
3. Generate rules using interface
4. Test and validate

### Customizing Dashboard
1. Modify templates in `.cursor/CORE/ANALYTICS/templates/`
2. Update styles in `static/css/`
3. Extend functionality in `static/js/`
4. Add new API routes as needed

### Extending Knowledge Graph
1. Add new entity types
2. Define relationships
3. Create visualization styles
4. Implement search/filter options

## Troubleshooting

See `DEPLOY/DEPLOYMENT_VERIFICATION.md` for:
- Common issues
- Verification steps
- Health checks
- Support resources

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Submit pull request

## License

MIT License - see LICENSE file

## Support

- Documentation: `.cursor/CORE/DOCS/`
- Issues: GitHub repository
- Community: Discord server 