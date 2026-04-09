import requests
import json

# ------------------ GITHUB ------------------

def scrape_github(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    repos = []
    if response.status_code == 200:
        for repo in response.json():
            repos.append({
                "name": repo["name"],
                "description": repo["description"] or "",
                "language": repo["language"]
            })

    return {"repos": repos}


# ------------------ CODEFORCES (API ✅) ------------------

def scrape_codeforces(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    res = requests.get(url).json()

    if res["status"] == "OK":
        user = res["result"][0]
        return {
            "rating": user.get("rating"),
            "max_rating": user.get("maxRating"),
            "rank": user.get("rank")
        }

    return {}


# ------------------ LEETCODE (GraphQL ✅) ------------------

def scrape_leetcode(username):
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
            profile {
              ranking
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

    res = requests.post(url, json=query, headers=headers)

    if res.status_code == 200:
        data = res.json()

        try:
            stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
            ranking = data["data"]["matchedUser"]["profile"]["ranking"]

            solved = {item["difficulty"]: item["count"] for item in stats}

            return {
                "total_solved": solved.get("All", 0),
                "easy": solved.get("Easy", 0),
                "medium": solved.get("Medium", 0),
                "hard": solved.get("Hard", 0),
                "ranking": ranking
            }
        except:
            return {}

    return {}


# ------------------ CODECHEF (LIGHT SCRAPING ⚠️) ------------------

def scrape_codechef(username):
    url = f"https://www.codechef.com/users/{username}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    data = {}

    if res.status_code == 200:
        text = res.text

        # Simple extraction (basic but works)
        import re

        rating = re.search(r'(\d+)\s*\(Div', text)
        solved = re.search(r'Total Problems Solved:\s*(\d+)', text)
        rank = re.search(r'Global Rank:\s*(\d+)', text)

        if rating:
            data["rating"] = rating.group(1)
        if solved:
            data["problems_solved"] = solved.group(1)
        if rank:
            data["global_rank"] = rank.group(1)

    return data


# ------------------ KAGGLE (LIMITED ⚠️) ------------------

def scrape_kaggle(username):
    url = f"https://www.kaggle.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return {"status": "Profile fetched (limited data due to anti-scraping)"}

    return {}


# ------------------ MAIN LOGIC ------------------

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


# ------------------ USER INPUT ------------------

def get_user_input():
    platforms = {}

    print("\nSelect platforms (type yes/no):")

    if input("GitHub? ").lower() == "yes":
        platforms["github"] = input("Enter GitHub username: ")

    if input("LeetCode? ").lower() == "yes":
        platforms["leetcode"] = input("Enter LeetCode username: ")

    if input("Codeforces? ").lower() == "yes":
        platforms["codeforces"] = input("Enter Codeforces username: ")

    if input("CodeChef? ").lower() == "yes":
        platforms["codechef"] = input("Enter CodeChef username: ")

    if input("Kaggle? ").lower() == "yes":
        platforms["kaggle"] = input("Enter Kaggle username: ")

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

    print("\n✅ Clean data saved to clean_data.json")