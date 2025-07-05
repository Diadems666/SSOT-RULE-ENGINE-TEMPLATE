# SSOT-RULE-ENGINE-TEMPLATE Deployment Verification

Use this checklist to verify successful deployment to a target project.

## ✅ Pre-Deployment Checklist

- [ ] Target project directory exists
- [ ] You have write permissions to the target directory
- [ ] Python 3.8+ is installed and accessible
- [ ] Node.js 18+ is installed and accessible
- [ ] npm is available in PATH

## ✅ Deployment Process Checklist

### Method 1: Using Deployment Scripts
- [ ] Ran `deploy.ps1` (Windows) or `deploy.sh` (Unix/Linux/macOS)
- [ ] No errors during file copying
- [ ] All template files copied successfully

### Method 2: Manual Deployment
- [ ] Copied `.cursor/` directory to target project root
- [ ] Copied `launch-dashboard.py` to target project root
- [ ] Copied `.gitignore` to target project root (if not existing)

## ✅ Post-Deployment Verification

### Core Structure
- [ ] `.cursor/CORE/SSOT/.ENGINE` exists and is readable
- [ ] `.cursor/CORE/MCP/` contains three server directories
- [ ] `.cursor/CORE/ANALYTICS/` contains analytics files
- [ ] `.cursor/mcp.json` exists and is properly formatted
- [ ] `launch-dashboard.py` exists in project root

### MCP Server Structure
- [ ] `knowledge-graph/` directory exists with source files
- [ ] `sequentialthinking/` directory exists with source files
- [ ] `filesystem/` directory exists with source files
- [ ] No `node_modules/` directories in template
- [ ] No `dist/` directories in template
- [ ] No `package-lock.json` files in template

### Analytics System
- [ ] `analytics_engine.py` exists and is readable
- [ ] `dashboard.py` exists and is readable
- [ ] `startup.py` exists and is readable
- [ ] `cli.py` exists and is readable
- [ ] `USER-RULES-TEMPLATE.md` exists

## ✅ System Initialization

### Trigger Execution
- [ ] Navigate to target project directory
- [ ] Run `!!-ADD-.ENGINE-!!` in Cursor AI
- [ ] System acknowledges trigger and begins analysis
- [ ] SSOT files are populated automatically
- [ ] Analytics dashboard launches

### Expected Outcomes
- [ ] Analytics dashboard accessible at `http://localhost:8080`
- [ ] SSOT files populated in `.cursor/CORE/SSOT/`
- [ ] Project health score generated
- [ ] MCP servers ready for installation
- [ ] Knowledge Graph ready for building

## ✅ Full System Validation

### MCP Installation
- [ ] Run `!!-INSTALL-MCP-!!` trigger
- [ ] npm install completes for all three servers
- [ ] No installation errors reported
- [ ] Server dependencies installed successfully

### Knowledge Graph Building
- [ ] Run `!!-BUILD-KG-!!` trigger
- [ ] Knowledge Graph populated with project entities
- [ ] Relationships established between components
- [ ] Graph accessible via API

### Dashboard Functionality
- [ ] Dashboard loads without errors
- [ ] Project health score displays correctly
- [ ] Analytics data populates
- [ ] Rule Engine interface accessible
- [ ] SSOT system status visible

## ✅ Troubleshooting Common Issues

### Dashboard Not Loading
- [ ] Check Python installation and version
- [ ] Verify port 8080 is available
- [ ] Run `python launch-dashboard.py` manually
- [ ] Check for Unicode encoding issues on Windows

### MCP Installation Failures
- [ ] Verify Node.js version (18+)
- [ ] Check npm is in PATH
- [ ] Verify file permissions
- [ ] Check network connectivity for npm packages

### SSOT System Issues
- [ ] Verify `.ENGINE` file is readable
- [ ] Check directory permissions
- [ ] Ensure all required directories exist
- [ ] Validate JSON configuration files

## ✅ Success Indicators

A successful deployment should show:
- ✅ Analytics dashboard running on http://localhost:8080
- ✅ Project health score > 60
- ✅ All SSOT files populated
- ✅ MCP servers installed and configured
- ✅ Knowledge Graph contains project entities
- ✅ Rule Engine interface functional

## 📝 Deployment Notes

**Date:** ___________
**Target Project:** ___________
**Deployment Method:** ___________
**Issues Encountered:** ___________
**Resolution:** ___________
**Final Status:** ___________

## 🚀 Next Steps After Successful Deployment

1. **Explore the Dashboard**: Visit http://localhost:8080
2. **Review SSOT State**: Check `.cursor/CORE/SSOT/` files
3. **Test Knowledge Graph**: Search for project entities
4. **Create Custom Rules**: Use the Rule Engine interface
5. **Monitor Health**: Set up regular health checks
6. **Customize Analytics**: Modify analytics engine as needed

---

**Template Version:** 1.0.0  
**Last Updated:** 2025-01-27  
**Compatibility:** Cursor AI IDE with MCP support 