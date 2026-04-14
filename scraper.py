import requests
import json
import re

# ------------------ GITHUB ------------------
def scrape_github(username):
    try:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, timeout=10)

        repos = []
        if response.status_code == 200:
            for repo in response.json():
                repos.append({
                    "name": repo["name"],
                    "description": repo["description"] or "",
                    "language": repo["language"]
                })

        return {"repos": repos}

    except Exception as e:
        return {"repos": []}


# ------------------ CODEFORCES ------------------
def scrape_codeforces(username):
    try:
        url = f"https://codeforces.com/api/user.info?handles={username}"
        res = requests.get(url, timeout=10).json()

        if res.get("status") == "OK":
            user = res["result"][0]
            return {
                "rating": user.get("rating", 0) or 0,
                "max_rating": user.get("maxRating", 0) or 0,
                "rank": user.get("rank", "")
            }
    except:
        pass

    return {}


# ------------------ LEETCODE FIXED ------------------
def scrape_leetcode(username):
    try:
        url = "https://leetcode.com/graphql"

        query = {
            "query": """
            query getUserProfile($username: String!) {
              matchedUser(username: $username) {
                submitStats {
                  acSubmissionNum {
                    difficulty
                    count
                  }
                }
              }
            }
            """,
            "variables": {"username": username}
        }

        headers = {
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/{username}/"
        }

        res = requests.post(url, json=query, headers=headers, timeout=10)

        if res.status_code == 200:
            data = res.json()

            stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
            solved = {i["difficulty"]: i["count"] for i in stats}

            total = sum(solved.values())

            return {
                "total_solved": total,
                "easy": solved.get("Easy", 0),
                "medium": solved.get("Medium", 0),
                "hard": solved.get("Hard", 0),
            }

    except:
        pass

    return {}


# ------------------ CODECHEF FIXED ------------------
def scrape_codechef(username):
    try:
        url = f"https://www.codechef.com/users/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)

        data = {}

        if res.status_code == 200:
            text = res.text

            rating = re.search(r'(\d+)\s*\(Div', text)
            solved = re.search(r'Total Problems Solved:\s*(\d+)', text)

            if rating:
                data["rating"] = int(rating.group(1))

            if solved:
                data["problems_solved"] = int(solved.group(1))

        return data

    except:
        return {}


# ------------------ KAGGLE ------------------
def scrape_kaggle(username):
    try:
        url = f"https://www.kaggle.com/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code == 200:
            return {"status": "Profile fetched (limited data)"}

    except:
        pass

    return {}


# ------------------ MAIN ------------------
def scrape_selected(platforms):
    result = {}

    for platform, username in platforms.items():
        print(f"🔍 Scraping {platform}...")

        if platform == "github":
            result["github"] = scrape_github(username)

        elif platform == "leetcode":
            result["leetcode"] = scrape_leetcode(username)

        elif platform == "codeforces":
            result["codeforces"] = scrape_codeforces(username)

        elif platform == "codechef":
            result["codechef"] = scrape_codechef(username)

        elif platform == "kaggle":
            result["kaggle"] = scrape_kaggle(username)

    return result


# ------------------ INPUT ------------------
def get_user_input():
    platforms = {}

    print("\nSelect platforms (yes/no):")

    if input("GitHub? ").lower() == "yes":
        platforms["github"] = input("GitHub username: ")

    if input("LeetCode? ").lower() == "yes":
        platforms["leetcode"] = input("LeetCode username: ")

    if input("Codeforces? ").lower() == "yes":
        platforms["codeforces"] = input("Codeforces username: ")

    if input("CodeChef? ").lower() == "yes":
        platforms["codechef"] = input("CodeChef username: ")

    if input("Kaggle? ").lower() == "yes":
        platforms["kaggle"] = input("Kaggle username: ")

    return platforms


# ------------------ SAVE ------------------
def save_data(data):
    with open("clean_data.json", "w") as f:
        json.dump(data, f, indent=4)


# ------------------ RUN ------------------
if __name__ == "__main__":
    user_platforms = get_user_input()
    data = scrape_selected(user_platforms)
    save_data(data)

    print("\n✅ clean_data.json created successfully")