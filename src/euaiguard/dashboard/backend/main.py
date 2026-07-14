from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[4]

ARTICLE_FILE = PROJECT_ROOT / ".euaiguard" / "articles" / "article_02.json"

print("Project Root:", PROJECT_ROOT)
print("Looking for:", ARTICLE_FILE)
print("Exists:", ARTICLE_FILE.exists())


@app.get("/api/article/02")
def get_article():
    if not ARTICLE_FILE.exists():
        return {"error": "Article 02 not found"}

    with open(ARTICLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)