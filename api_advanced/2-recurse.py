#!/usr/bin/python3
"""
2-recurse
Queries the Reddit API recursively and returns a list of titles
of all hot articles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """Recursively get titles of all hot posts for a subreddit."""
    if hot_list is None:
        hot_list = []

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
        return None

    token = token_response.json().get("access_token")
    headers["Authorization"] = "bearer {}".format(token)

    url = "https://oauth.reddit.com/r/{}/hot?limit=100".format(subreddit)
    if after:
        url += "&after={}".format(after)

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    children = data.get("children", [])

    for post in children:
        title = post.get("data", {}).get("title")
        if title:
            hot_list.append(title)

    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    else:
        if len(hot_list) == 0:
            return None
        return hot_list
