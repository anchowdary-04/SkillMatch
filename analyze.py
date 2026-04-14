import json

# Load data
with open("clean_data.json", "r") as f:
    data = json.load(f)

output = {}

# ------------------ SUMMARY ------------------
leetcode_total = data.get("leetcode", {}).get("total_solved", 0) or 0
codechef_total = data.get("codechef", {}).get("problems_solved", 0) or 0

try:
    codechef_total = int(codechef_total)
except:
    codechef_total = 0

total_problems = leetcode_total + codechef_total

cf_rating = data.get("codeforces", {}).get("rating", 0)
if cf_rating is None:
    cf_rating = 0

cf_rating = int(cf_rating)

if total_problems > 500:
    activity = "High"
elif total_problems > 100:
    activity = "Medium"
else:
    activity = "Low"

output["summary"] = {
    "total_problems_solved": total_problems,
    "codeforces_rating": cf_rating,
    "activity_level": activity
}

# ------------------ PROJECT + SKILLS ------------------
projects = []
languages_count = {}

keyword_map = {
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "web": "Web Development",
    "frontend": "Web Development",
    "backend": "Web Development",
    "api": "Backend Development",
    "data": "Data Analysis"
}

repos = data.get("github", {}).get("repos", [])

for repo in repos:
    name = repo.get("name", "")
    desc = (repo.get("description") or "").lower()
    lang = repo.get("language")

    if lang:
        languages_count[lang] = languages_count.get(lang, 0) + 1

    skills = set()

    if lang:
        skills.add(lang)

    for key, value in keyword_map.items():
        if key in desc:
            skills.add(value)

    projects.append({
        "name": name,
        "description": desc,
        "skills": list(skills)
    })

output["projects"] = projects

# ------------------ LANGUAGE PROFICIENCY ------------------
language_scores = {}

for lang, count in languages_count.items():
    language_scores[lang] = count * 20

for lang in ["Python", "Java", "C++"]:
    language_scores.setdefault(lang, 10)

for lang in language_scores:
    language_scores[lang] += total_problems // 50

# safest strongest language
if language_scores:
    strongest = max(language_scores, key=language_scores.get)
else:
    strongest = "None"

output["languages"] = {
    "scores": language_scores,
    "strongest": strongest
}

# ------------------ SKILLS ------------------
skills = {
    "programming": list(language_scores.keys()),
    "core_cs": ["DSA", "Algorithms"],
    "domain": []
}

for p in projects:
    for s in p["skills"]:
        if s in ["Machine Learning", "Web Development", "Data Analysis", "Artificial Intelligence"]:
            skills["domain"].append(s)

# remove duplicates safely
for key in skills:
    skills[key] = list(set(skills[key]))

output["skills"] = skills

# ------------------ FINAL SCORE ------------------
score = 0

if total_problems > 500:
    score += 40
elif total_problems > 100:
    score += 25
else:
    score += 10

if cf_rating > 1200:
    score += 30
elif cf_rating > 800:
    score += 20
else:
    score += 10

if len(projects) >= 5:
    score += 30
elif len(projects) >= 2:
    score += 20
else:
    score += 10

output["final_score"] = score

# ------------------ SAVE ------------------
print(json.dumps(output, indent=4))

with open("analyzed.json", "w") as f:
    json.dump(output, f, indent=4)

print("✅ Analysis saved to analyzed.json")