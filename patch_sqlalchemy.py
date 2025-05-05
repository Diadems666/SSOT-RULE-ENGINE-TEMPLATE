"""
SQLAlchemy Python 3.13 Compatibility Patch

This script patches SQLAlchemy 2.0.x to work with Python 3.13 by modifying
the TypingOnly class check in sqlalchemy.util.langhelpers to ignore the
__firstlineno__ and __static_attributes__ attributes that Python 3.13 adds.

Usage:
    python patch_sqlalchemy.py

Note: This is a temporary workaround until SQLAlchemy releases a version
that is fully compatible with Python 3.13.
"""

import os
import re
import sys


def patch_sqlalchemy():
    """Patch SQLAlchemy's langhelpers.py file to work with Python 3.13."""
    try:
        import sqlalchemy
        sa_path = os.path.dirname(sqlalchemy.__file__)
        langhelpers_path = os.path.join(sa_path, 'util', 'langhelpers.py')
        
        print(f"SQLAlchemy version: {sqlalchemy.__version__}")
        print(f"Attempting to patch: {langhelpers_path}")
        
        if not os.path.exists(langhelpers_path):
            print(f"Error: Could not find {langhelpers_path}")
            return False
        
        # Create a backup of the original file
        backup_path = langhelpers_path + '.bak'
        if not os.path.exists(backup_path):
            print(f"Creating backup at {backup_path}")
            with open(langhelpers_path, 'r') as src:
                with open(backup_path, 'w') as dst:
                    dst.write(src.read())
        
        # Read the file content
        with open(langhelpers_path, 'r') as f:
            content = f.read()
        
        # The pattern to look for (the TypingOnly class and its __init_subclass__ method)
        init_subclass_pattern = r'class TypingOnly\(metaclass=_TypingOnlyMeta\):\s+"""A mixin class that disallows any attributes.*?\s+@classmethod\s+def __init_subclass__\(cls, \*args, \*\*kwargs\):\s+.*?additional attributes (.*?)\s+\)(?=\s+super\()'
        
        # Find the pattern
        match = re.search(init_subclass_pattern, content, re.DOTALL)
        if not match:
            print("Error: Could not find the TypingOnly.__init_subclass__ method to patch")
            return False
        
        # Modified check that excludes Python 3.13's special attributes
        patched_content = content.replace(
            'cls_vars = set(cls.__dict__) - set(TypingOnly.__dict__)',
            'cls_vars = set(cls.__dict__) - set(TypingOnly.__dict__) - {"__firstlineno__", "__static_attributes__"}'
        )
        
        if patched_content == content:
            print("Error: Patch content was not replaced. Manual intervention required.")
            return False
        
        # Write the patched content back
        with open(langhelpers_path, 'w') as f:
            f.write(patched_content)
        
        print("SQLAlchemy successfully patched for Python 3.13 compatibility")
        return True
        
    except ImportError:
        print("Error: SQLAlchemy not installed or not found in Python path")
        return False
    except Exception as e:
        print(f"Error patching SQLAlchemy: {e}")
        return False


if __name__ == "__main__":
    print("SQLAlchemy Python 3.13 Compatibility Patch")
    print("------------------------------------------")
    
    if sys.version_info < (3, 13):
        print(f"Warning: This patch is intended for Python 3.13+. You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        proceed = input("Do you want to proceed anyway? (y/n): ")
        if proceed.lower() != 'y':
            sys.exit(0)
    
    if patch_sqlalchemy():
        print("\nPatch applied successfully. You may now run your application.")
    else:
        print("\nFailed to apply patch. Please try manual intervention.") 