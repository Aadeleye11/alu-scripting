#!/usr/bin/python3
"""
This module defines a function that returns the number of subscribers for a subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    If subreddit is invalid or request fails, return 0.
    """
    client_id = "BLDc0NYEGo_wuYewe9CZdw"
    client_secret = "k_A_JrFDOnivsGdAxg0ai6BbefBkRw"
    user_agent = "python:RedditAPIProject:v1.0.0 (by /u/FlowPsychological419)"

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": user_agent}

    token_response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth, data=data, headers=headers
    )

    if token_response.status_code != 200:
        return 0

    token = token_response.json().get("access_token")
    headers["Authorization"] = "bearer {}".format(token)

    url = "https://oauth.reddit.com/r/{}/about".format(subreddit)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("data", {}).get("subscribers", 0)
    else:
        return 0
