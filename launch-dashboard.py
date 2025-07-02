#!/usr/bin/env python3
"""
Quick Launch Script for SSOT-RULE-ENGINE Analytics Dashboard
Place in project root for easy access
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🚀 Launching SSOT-RULE-ENGINE Analytics Dashboard...")
    
    # Check if analytics directory exists
    analytics_dir = Path('.cursor/CORE/ANALYTICS')
    if not analytics_dir.exists():
        print("❌ Analytics system not found. Please run !!-INIT-.ENGINE-!! or !!-ADD-.ENGINE-!! first.")
        return
    
    startup_script = analytics_dir / 'startup.py'
    if not startup_script.exists():
        print("❌ Startup script not found. Please ensure analytics system is properly installed.")
        return
    
    try:
        # Launch dashboard using startup script
        print("📊 Starting dashboard server...")
        subprocess.run([sys.executable, str(startup_script)], cwd=Path.cwd())
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

if __name__ == "__main__":
    main() 