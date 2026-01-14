import os
import requests
import pandas as pd

os.chdir("/Users/efang/Documents/IAP_UROP/github-compliment")

TOKEN = os.getenv("GITHUB_TOKEN")

if TOKEN is None:
    raise ValueError("GITHUB_TOKEN not set")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

OWNER = "davila7"
REPO = "claude-code-templates"

forks = []
page = 1

while True:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/forks?per_page=100&page={page}"
    response = requests.get(url, headers=HEADERS)

    # print("STATUS CODE:", response.status_code)
    # print("RAW RESPONSE SAMPLE (first 500 chars):")
    # print(response.text)
    batch = response.json()

    # If GitHub did NOT return a list of forks, stop
    # if not isinstance(batch, list):
    #     print("GitHub did not return fork data. Stopping.")
    #     break

    if len(batch) == 0:
        break

    for fork in batch:
        forks.append({
            "fork_owner": fork["owner"]["login"],
            "fork_url": fork["html_url"],
            "owner_type": fork["owner"]["type"],
            "created_at": fork["created_at"],
            "pushed_at": fork["pushed_at"],
            "size": fork["size"],
            "stars": fork["stargazers_count"],
            "forks_of_fork": fork["forks_count"],
            "open_issues": fork["open_issues_count"],
            "has_homepage": fork["homepage"] is not None,
            "is_archived": fork["archived"]
        })
    print(f'Scraped page {page}')
    page +=1


df = pd.DataFrame(forks)
df.to_csv("data/forks.csv", index=False)

print(f"Saved {len(df)} forks")
