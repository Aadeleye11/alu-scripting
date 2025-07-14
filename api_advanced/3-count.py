#!/usr/bin/python3
"""
3-count
Recursively queries Reddit API for hot posts,
counts keyword occurrences in titles,
and prints sorted counts.
"""

import requests


def count_words(subreddit, word_list, counts=None, after=None):
    """Recursively count occurrences of keywords in subreddit hot post titles."""
    if counts is None:
        counts = {}

    # Normalize words to lowercase once
    normalized_words = [w.lower() for w in word_list]

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
        # Invalid subreddit or auth failure
        if after is None:
            return
        else:
            return counts

    token = token_response.json().get("access_token")
    headers["Authorization"] = "bearer {}".format(token)

    url = "https://oauth.reddit.com/r/{}/hot?limit=100".format(subreddit)
    if after:
        url += "&after={}".format(after)

    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        if after is None:
            # Initial call failure, invalid subreddit
            return
        else:
            return counts

    posts = response.json().get("data", {}).get("children", [])
    for post in posts:
        title = post.get("data", {}).get("title", "").lower()
        # Split title into words, strip punctuation from each word
        title_words = [
            ''.join(ch for ch in w if ch.isalpha()) for w in title.split()
        ]
        for word in normalized_words:
            count = title_words.count(word)
            if count > 0:
                counts[word] = counts.get(word, 0) + count

    after = response.json().get("data", {}).get("after")

    if after:
        # Continue recursion on next page
        return count_words(subreddit, word_list, counts, after)
    else:
        if not counts:
            # No counts found, print nothing
            return

        # Combine duplicates (already handled since normalized_words is used)
        # Sort by count descending, then alphabetically ascending
        sorted_counts = sorted(
            counts.items(),
            key=lambda x: (-x[1], x[0])
        )
        for word, count in sorted_counts:
            if count > 0:
                print("{}: {}".format(word, count))
        return
