#!/usr/bin/python3
"""
This module contains a function to query Reddit API
and return number of subscribers for a subreddit.
"""

import requests


def number_of_subscribers(subreddit):
    """Returns number of subscribers for a given subreddit"""
    client_id = "BLDc0NYEGo_wuYewe9CZdw"
    client_secret = "k_A_JrFDOnivsGdAxg0ai6BbefBkRw"
    user_agent = (
        "python:RedditAPIProject:v1.0.0 "
        "(by /u/FlowPsychological419)"
    )

    # Get access token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": user_agent}

    token_response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers
    )

    if token_response.status_code != 200:
        return 0

    token = token_response.json().get("access_token")
    headers["Authorization"] = "bearer {}".format(token)

    # Request subreddit info
    url = "https://oauth.reddit.com/r/{}/about".format(subreddit)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("data", {}).get("subscribers", 0)

    return 0
