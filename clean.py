import json

# -----------------------------
# LOAD ANALYZED DATA
# -----------------------------
INPUT_FILE = "analyzed.json"   # output from analyze.py
OUTPUT_FILE = "dataset.json"  # final cleaned dataset

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def normalize_languages(lang_dict):
    """
    Convert language scores dict to clean list + strongest language
    """
    if not lang_dict:
        return [], "None"

    languages = list(lang_dict.keys())

    # find strongest language
    strongest = max(lang_dict, key=lang_dict.get)

    return languages, strongest


def clean_skills(skills):
    """
    Merge all skill categories into one list and remove duplicates
    """
    all_skills = []

    for category in skills.values():
        all_skills.extend(category)

    # remove duplicates + empty values
    clean = list(set([s for s in all_skills if s]))

    return clean


def count_projects(projects):
    return len(projects) if projects else 0


# -----------------------------
# MAIN CLEANING FUNCTION
# -----------------------------

def clean_data(data):
    cleaned_dataset = []

    # handle single user OR multiple users
    if isinstance(data, dict):
        data = [data]

    for user in data:
        summary = user.get("summary", {})
        skills = user.get("skills", {})
        languages = user.get("languages", {})
        projects = user.get("projects", [])

        lang_list, strongest_lang = normalize_languages(languages.get("scores", {}))
        skill_list = clean_skills(skills)
        project_count = count_projects(projects)

        clean_user = {
            "total_problems": summary.get("total_problems_solved", 0),
            "codeforces_rating": summary.get("codeforces_rating", 0),
            "activity_level": summary.get("activity_level", "Unknown"),

            "skills": skill_list,
            "languages": lang_list,
            "strongest_language": strongest_lang,

            "projects_count": project_count,
            "final_score": user.get("final_score", 0)
        }

        cleaned_dataset.append(clean_user)

    return cleaned_dataset


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        raw_data = json.load(f)

    cleaned_data = clean_data(raw_data)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(cleaned_data, f, indent=4)

    print("✅ Cleaned dataset saved to dataset.json")