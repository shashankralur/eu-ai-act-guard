from importlib.util import find_spec
from pathlib import Path
import ast

PACKAGES = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google.genai": "Google Gemini",
    "google.generativeai": "Google Gemini",
    "ollama": "Ollama",
    "transformers": "Hugging Face",
    "langchain": "LangChain",
    "llama_index": "LlamaIndex",
    "crewai": "CrewAI",
    "autogen": "AutoGen",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
}


def detect_installed_packages():
    """Packages installed in the current Python environment."""
    detected = {}

    for module, name in PACKAGES.items():
        try:
            if find_spec(module) is not None:
                detected[module] = name
        except ModuleNotFoundError:
            continue

    return detected


def detect_used_packages(project_root: Path):
    """Packages actually imported in the project source code."""
    detected = {}

    for py_file in project_root.rglob("*.py"):

        if any(
            part in {"venv", ".venv", "__pycache__", ".git", ".euaiguard"}
            for part in py_file.parts
        ):
            continue

        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))

            for node in ast.walk(tree):

                modules = []

                if isinstance(node, ast.Import):
                    modules = [n.name for n in node.names]

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        modules = [node.module]

                for module in modules:
                    for pkg, name in PACKAGES.items():
                        if module.startswith(pkg):
                            detected[pkg] = name

        except Exception:
            continue

    return detected