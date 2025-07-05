# SSOT Rule Engine Deployment Verification Guide

This guide helps verify that your SSOT Rule Engine deployment is working correctly.

## Prerequisites Check

1. Python Environment
```bash
python --version  # Should be 3.8+
pip --version
```

2. Node.js Environment
```bash
node --version  # Should be 14+
npm --version
```

## Directory Structure Verification

Check that the following directories exist and contain the appropriate files:

```
.cursor/
  CORE/
    RULE-ENGINE/
      rule_generator.py
      engine_integration.py
      templates/
      config.json
    ANALYTICS/
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
    SSOT/
      .ENGINE
      .INIT
      .HISTORY
      .CONTEXT
      .FACTS
      .MEMORY
      .PROGRESS
    MCP/
      [MCP server files]
```

## Configuration Verification

1. Check MCP Configuration
```bash
cat mcp.json  # Should contain valid JSON with MCP settings
```

2. Check Rule Engine Configuration
```bash
cat .cursor/CORE/RULE-ENGINE/config.json  # Should contain valid JSON
```

3. Check Analytics Configuration
```bash
cat .cursor/CORE/ANALYTICS/config.json  # Should contain valid JSON
```

## Functionality Tests

1. Dashboard Access
   - Run `python launch-dashboard.py`
   - Access http://localhost:5000
   - Verify dashboard loads without errors
   - Check all dashboard components are visible

2. Knowledge Graph Visualization
   - Click "Knowledge Graph" tab in dashboard
   - Verify graph visualization loads
   - Test node/edge creation
   - Test search functionality
   - Test filtering options

3. Rule Engine
   - Check rule generation works
   - Verify rule templates are accessible
   - Test rule creation through interface

4. SSOT System
   - Verify .HISTORY shows deployment entry
   - Check .INIT contains valid configuration
   - Test project context tracking

5. MCP Integration
   - Verify MCP servers are running
   - Test Knowledge Graph persistence
   - Check memory operations work

## Common Issues & Solutions

1. Dashboard Not Loading
   - Check Python dependencies are installed
   - Verify port 5000 is available
   - Check Flask server logs

2. Knowledge Graph Issues
   - Verify vis.js is loaded correctly
   - Check browser console for errors
   - Verify MCP connection settings

3. Rule Engine Problems
   - Check Python path includes rule_engine module
   - Verify template directory permissions
   - Check rule generation logs

4. MCP Connection Issues
   - Verify MCP servers are running
   - Check WebSocket connection
   - Verify mcp.json configuration

## Health Check

Run the built-in health check:
```bash
!!-HEALTH-CHECK-!!
```

This will:
- Verify all components are running
- Check system integration
- Report any issues found
- Provide health score (0-100)

## Support

If you encounter issues:
1. Check the logs in `.cursor/CORE/LOGS/`
2. Review error messages in browser console
3. Verify all dependencies are installed
4. Check system requirements are met

For additional help:
- Run `!!-ANALYZE-PROJECT-!!` for detailed diagnostics
- Check documentation in `.cursor/CORE/DOCS/`
- Submit issues to the project repository 