#!/usr/bin/python3
"""Fetches and prints the top 10 hot post titles from a subreddit."""

import requests


def top_ten(subreddit):
    """Prints the titles of the top 10 hot posts for a given subreddit."""
    client_id = "BLDc0NYEGo_wuYewe9CZdw"
    client_secret = "k_A_JrFDOnivsGdAxg0ai6BbefBkRw"
    user_agent = "python:RedditAPIProject:v1.0.0 (by /u/FlowPsychological419)"

    # Step 1: Get OAuth2 token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {'grant_type': 'client_credentials'}
    headers = {'User-Agent': user_agent}

    try:
        res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth, data=data, headers=headers, timeout=10
        )
        res.raise_for_status()
        token = res.json().get('access_token')
    except Exception:
        print("None")
        return

    headers['Authorization'] = "bearer {}".format(token)

    # Step 2: Call subreddit hot posts
    url = "https://oauth.reddit.com/r/{}/hot?limit=10".format(subreddit)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("None")
            return

        posts = response.json().get('data', {}).get('children', [])
        for post in posts:
            print(post.get('data', {}).get('title'))
    except Exception:
        print("None")

