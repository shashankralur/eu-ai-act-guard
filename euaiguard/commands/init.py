from pathlib import Path


IGNORED_DIRS = {
    "venv",
    ".venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "euaiguard.egg-info",
    "build"
}

def init():
    current_directory = Path.cwd()
    
    project_files = []
    
    print("Scanning Files...")
    for path in current_directory.rglob("*"):
        if not path.is_file():
            continue
    
        
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        
        project_files.append(path)
    
    for file in project_files:
        print(file)
    
    print(f"Total Files: {len(project_files)}")