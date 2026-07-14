from pathlib import Path
import ast

PROVIDERS = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google.genai": "Google Gemini",
    "google.generativeai": "Google Gemini",
    "ollama": "Ollama",
    "cohere": "Cohere",
    "mistralai": "Mistral AI",
    "groq": "Groq",
    "azure.ai.inference": "Azure AI",
    "azure.ai.openai": "Azure OpenAI",
    "boto3": "Amazon Bedrock",
}


def detect_ai_providers(project_root: Path):
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
                    for pkg, provider in PROVIDERS.items():
                        if module.startswith(pkg):
                            detected[pkg] = provider

        except Exception:
            continue

    return detected