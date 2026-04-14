import json
import pandas as pd

INPUT_FILE = "dataset.json"
OUTPUT_FILE = "ml_dataset.csv"

# language encoding
lang_map = {
    "Python": 1,
    "Java": 2,
    "C++": 3,
    "JavaScript": 4,
    "Other": 0
}

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

rows = []

for user in data:
    skills = user.get("skills", [])
    languages = user.get("languages", [])
    strongest = user.get("strongest_language", "Other")

    # CLEAN LANGUAGES
    clean_langs = []
    for l in languages:
        if l in ["Jupyter Notebook", "Python3"]:
            l = "Python"
        if l and l not in ["None", "unknown", ""]:
            clean_langs.append(l)

    clean_langs = list(set(clean_langs))

    # CLEAN SKILLS
    clean_skills = list(set([s for s in skills if s and s != "unknown"]))

    row = {
        "total_problems_solved": int(user.get("total_problems", 0)),
        "codeforces_rating": int(user.get("codeforces_rating", 0)),
        "project_count": int(user.get("projects_count", 0)),
        "skills_count": len(clean_skills),
        "strongest_language": lang_map.get(strongest, 0),
        "final_score": int(user.get("final_score", 0))
    }

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print("✅ ML dataset saved as ml_dataset.csv")