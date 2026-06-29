from pathlib import Path
from dataclasses import dataclass


IGNORED_DIRS = {
    "venv",
    ".venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "euaiguard.egg-info",
    "build",
}


@dataclass
class ProjectFile:
    relative_path: Path
    absolute_path: Path
    extension: str
    size: int


def get_all_files(root: Path | None = None) -> list[ProjectFile]:
    if root is None:
        root = Path.cwd()

    project_files: list[ProjectFile] = []

    print("Scanning files...")

    stack = [root]

    while stack:
        current = stack.pop()

        for item in current.iterdir():

            if item.is_dir():
                if item.name in IGNORED_DIRS:
                    continue

                stack.append(item)
                continue

            project_files.append(
                ProjectFile(
                    relative_path=item.relative_to(root),
                    absolute_path=item.resolve(),
                    extension=item.suffix.lower(),
                    size=item.stat().st_size,
                )
            )

    return project_files


files = get_all_files()

print(f"Total Files: {len(files)}")