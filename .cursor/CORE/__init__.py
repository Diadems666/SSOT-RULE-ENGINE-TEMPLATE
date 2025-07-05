"""
SSOT Rule Engine Core Package
"""

from pathlib import Path

# Define core paths
CORE_DIR = Path(__file__).parent
ANALYTICS_DIR = CORE_DIR / 'ANALYTICS'
MEMORY_DIR = CORE_DIR / 'MEMORY'
RULE_ENGINE_DIR = CORE_DIR / 'RULE-ENGINE'

# Ensure directories exist
MEMORY_DIR.mkdir(exist_ok=True)
RULE_ENGINE_DIR.mkdir(exist_ok=True)

# Initialize memory file
MEMORY_FILE = MEMORY_DIR / 'memory.jsonl'
if not MEMORY_FILE.exists():
    MEMORY_FILE.touch() 