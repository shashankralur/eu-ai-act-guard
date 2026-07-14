from pathlib import Path
import json
from euaiguard.discovery.packages import (
    detect_installed_packages,
    detect_used_packages,
)

from euaiguard.discovery.provider import detect_ai_providers
# packages = detect_packages()
    

ARTICLE_NAME = "article_02"

# User project directory (where 'euai init' is executed)
PROJECT_ROOT = Path.cwd()

# EUAI project structure
EUAI_DIR = PROJECT_ROOT / ".euaiguard"
ARTICLES_DIR = EUAI_DIR / "articles"
REPORTS_DIR = EUAI_DIR / "reports"
LOGS_DIR = EUAI_DIR / "logs"

def create_project_structure():
    """Create the .euaiguard project structure if it doesn't exist."""
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

questions = [
    {
        "key": "is_ai_system",
        "question": "Is this an AI system?",
        "type": "confirm",
        "answer": None,
    },
    {
        "key": "serves_eu_users",
        "question": "Can this AI system be used by people or organizations in the EU?",
        "type": "confirm",
        "answer": None,
    },
    {
        "key": "business_role",
        "question": "What is your role with respect to this AI system?",
        "type": "choice",
        "choices": [
            "Provider",
            "Deployer",
            "Importer",
            "Distributor",
            "Authorized Representative",
        ],
        "answer": None,
    },
    {
        "key": "research_only",
        "question": "Is this AI system used exclusively for research and development?",
        "type": "confirm",
        "answer": None,
    },
    {
        "key": "military_use",
        "question": "Is this AI system intended exclusively for military, defence, or national security purposes?",
        "type": "confirm",
        "answer": None,
    },
]


def save_article(article_name: str, questions: list):
    """Save article answers."""

    create_project_structure()

    data = {
        "article": article_name,
        "completed": all(q["answer"] is not None for q in questions),
        "answers": {
            q["key"]: q["answer"] for q in questions
        },
        "auto_detected": {
            "packages": {
                "installed": detect_installed_packages(),
                "used": detect_used_packages(PROJECT_ROOT)
            },
            "ai_providers": detect_ai_providers(PROJECT_ROOT)
        }
    }

    file = ARTICLES_DIR / f"{article_name}.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        

def load_article(article_name: str):
    """Load saved answers if present."""
    file = ARTICLES_DIR / f"{article_name}.json"

    if not file.exists():
        return {}

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("answers", {})


def ask_questions(questions):
    print(f"\n=== {ARTICLE_NAME.upper()} : Scope Assessment ===\n")

    saved_answers = load_article(ARTICLE_NAME)

    # Restore previous answers
    for q in questions:
        if q["key"] in saved_answers:
            q["answer"] = saved_answers[q["key"]]

    for q in questions:

        # Skip already answered questions
        if q["answer"] is not None:
            print(f"✓ {q['question']} -> {q['answer']}")
            continue

        if q["type"] == "confirm":

            while True:
                ans = input(f"{q['question']} (y/n): ").strip().lower()

                if ans in ("y", "yes"):
                    q["answer"] = True
                    break

                elif ans in ("n", "no"):
                    q["answer"] = False
                    break

                print("Please enter y or n.")

        elif q["type"] == "choice":

            print(f"\n{q['question']}")

            for i, choice in enumerate(q["choices"], start=1):
                print(f"{i}. {choice}")

            while True:

                try:
                    idx = int(input("Select option: "))

                    if 1 <= idx <= len(q["choices"]):
                        q["answer"] = q["choices"][idx - 1]
                        break

                except ValueError:
                    pass

                print("Invalid selection.")

        elif q["type"] == "text":
            q["answer"] = input(f"{q['question']}: ").strip()

        # Save immediately after every answer
        save_article(ARTICLE_NAME, questions)

    return questions


def print_summary(results):
    print("\n========== SUMMARY ==========\n")

    for q in results:
        print(f"{q['question']}")
        print(f"Answer : {q['answer']}\n")


def init():
    print("Initializing EU AI Act Scope Assessment...")

    create_project_structure()
    results = ask_questions(questions)
    save_article(ARTICLE_NAME, results)
    print_summary(results)


    print("\n========== AUTO DETECTED ==========\n")
    installed = detect_installed_packages()
    used = detect_used_packages(PROJECT_ROOT)

    print("Installed Packages:")
    for _, name in installed.items():
        print(f"✓ {name}")

    print("\nUsed Packages:")
    for _, name in used.items():
        print(f"✓ {name}")

    print(f"\n✓ Answers saved to: {ARTICLES_DIR / f'{ARTICLE_NAME}.json'}")


if __name__ == "__main__":
    init()