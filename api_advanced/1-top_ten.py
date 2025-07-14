#!/usr/bin/python3
"""
1-top_ten
Queries the Reddit API and prints the titles of the first 10 hot posts
listed for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit."""
    client_id = "BLDc0NYEGo_wuYewe9CZdw"
    client_secret = "k_A_JrFDOnivsGdAxg0ai6BbefBkRw"
    user_agent = "python:RedditAPIProject:v1.0.0 (by /u/FlowPsychological419)"

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": user_agent}

    # Get access token
    token_response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth, data=data, headers=headers
    )

    if token_response.status_code != 200:
        print("None")
        return

    token = token_response.json().get("access_token")
    headers["Authorization"] = "bearer {}".format(token)

    url = "https://oauth.reddit.com/r/{}/hot?limit=10".format(subreddit)
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        print("None")
        return

    try:
        posts = response.json().get("data", {}).get("children", [])
        for post in posts:
            title = post.get("data", {}).get("title")
            if title:
                print(title)
    except Exception:
        print("None")
