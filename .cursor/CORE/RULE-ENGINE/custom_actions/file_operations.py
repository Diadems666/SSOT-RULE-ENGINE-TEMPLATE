import os
import shutil
from typing import Dict, Any
from ..action_executor import action

@action("backup_file")
def backup_file(context: Dict[str, Any], source_path: str, backup_dir: str = "backups") -> Dict[str, Any]:
    """Create a backup of a file"""
    if not os.path.exists(source_path):
        raise ValueError(f"Source file does not exist: {source_path}")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    filename = os.path.basename(source_path)
    backup_path = os.path.join(backup_dir, f"{filename}.bak")
    
    shutil.copy2(source_path, backup_path)
    
    return {
        "source_path": source_path,
        "backup_path": backup_path
    }

@action("archive_files")
def archive_files(context: Dict[str, Any], source_dir: str, archive_name: str) -> Dict[str, Any]:
    """Create a zip archive of files"""
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    archive_path = f"{archive_name}.zip"
    shutil.make_archive(archive_name, 'zip', source_dir)
    
    return {
        "source_dir": source_dir,
        "archive_path": archive_path
    }

@action("clean_directory")
def clean_directory(context: Dict[str, Any], target_dir: str, pattern: str = "*") -> Dict[str, Any]:
    """Clean files matching a pattern in a directory"""
    import glob
    
    if not os.path.exists(target_dir):
        raise ValueError(f"Target directory does not exist: {target_dir}")

    files = glob.glob(os.path.join(target_dir, pattern))
    removed_files = []
    
    for file_path in files:
        try:
            os.remove(file_path)
            removed_files.append(file_path)
        except Exception as e:
            context.get("logger", logging.getLogger()).warning(f"Failed to remove {file_path}: {str(e)}")
    
    return {
        "target_dir": target_dir,
        "pattern": pattern,
        "removed_files": removed_files,
        "removed_count": len(removed_files)
    } 