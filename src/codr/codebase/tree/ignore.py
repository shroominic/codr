import os
import fnmatch
from pathlib import Path


IGNORED: set[str] = {
    ".context",
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    "poetry.lock",
    "package-lock.json",
    "yarn.lock",
    ".mypy_cache",
    ".pytest_cache",
    ".vscode",
    ".idea",
    ".DS_Store",
    "*.pyc",
    "Cargo.lock",
}


def load_gitignore() -> None:
    """
    Loads the patterns from .gitignore and updates the global IGNORED set.
    """
    gitignore_files = [file for file in Path(".").rglob(".gitignore")]
    for gitignore_file in gitignore_files:
        with open(gitignore_file, "r") as f:
            for line in f.readlines():
                pattern = line.strip().split("#")[0]
                if pattern and pattern != "*":
                    pattern = pattern.removesuffix("/")
                    IGNORED.add(pattern)

load_gitignore()


def is_ignored_by_gitignore(file_path: str) -> bool:
    """
    Checks if a file is ignored by .gitignore
    """
    return any(
        fnmatch.fnmatch(file_path, pattern)
        or fnmatch.fnmatch(os.path.basename(file_path), pattern)
        for pattern in IGNORED
    )