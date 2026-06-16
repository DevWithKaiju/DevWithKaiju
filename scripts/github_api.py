"""
GitHub GraphQL API data fetcher.
Retrieves user stats, repositories, languages, and contribution data.
"""

import os
import json
import requests
from datetime import datetime, timezone


GRAPHQL_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    following { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        stargazerCount
        forkCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name color }
          }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
    }
    pullRequests(first: 1) { totalCount }
    issues(first: 1) { totalCount }
  }
}
"""


def fetch_github_data(username: str, token: str) -> dict:
    """Fetch user data from GitHub GraphQL API.

    Falls back to mock data when no token is available (local dev).
    """
    if not token:
        print("No GITHUB_TOKEN found - using mock data for local preview")
        return _mock_data(username)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        GRAPHQL_URL,
        json={"query": QUERY, "variables": {"login": username}},
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    result = resp.json()

    if "errors" in result:
        print(f"GraphQL errors: {result['errors']}")
        return _mock_data(username)

    user = result["data"]["user"]
    return _parse_user(username, user)


def _parse_user(username: str, user: dict) -> dict:
    """Transform raw GraphQL response into a flat stats dict."""

    # ── Languages ──
    languages: dict[str, dict] = {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            color = edge["node"]["color"] or "#ccc"
            size = edge["size"]
            if name in languages:
                languages[name]["size"] += size
            else:
                languages[name] = {"name": name, "color": color, "size": size}

    total_size = sum(l["size"] for l in languages.values())
    for lang in languages.values():
        lang["percentage"] = round(lang["size"] / total_size * 100, 1) if total_size else 0

    sorted_langs = sorted(languages.values(), key=lambda x: x["size"], reverse=True)

    # ── Account age ──
    created = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    age_years = (datetime.now(timezone.utc) - created).days / 365.25

    # ── Stars / forks ──
    total_stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])
    total_forks = sum(r["forkCount"] for r in user["repositories"]["nodes"])

    contrib = user["contributionsCollection"]

    return {
        "username": username,
        "followers": user["followers"]["totalCount"],
        "following": user["following"]["totalCount"],
        "total_repos": user["repositories"]["totalCount"],
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_commits": (
            contrib["totalCommitContributions"]
            + contrib["restrictedContributionsCount"]
        ),
        "total_prs": user["pullRequests"]["totalCount"],
        "total_issues": user["issues"]["totalCount"],
        "total_reviews": contrib["totalPullRequestReviewContributions"],
        "contributions_this_year": (
            contrib["totalCommitContributions"]
            + contrib["totalPullRequestContributions"]
            + contrib["totalIssueContributions"]
        ),
        "account_age_years": round(age_years, 1),
        "languages": sorted_langs[:10],
    }


def _mock_data(username: str = "DevWithKaiju") -> dict:
    """Return sample data for local testing / preview."""
    return {
        "username": username,
        "followers": 5,
        "following": 10,
        "total_repos": 8,
        "total_stars": 3,
        "total_forks": 1,
        "total_commits": 150,
        "total_prs": 5,
        "total_issues": 2,
        "total_reviews": 3,
        "contributions_this_year": 120,
        "account_age_years": 2.5,
        "languages": [
            {"name": "Python", "color": "#3572A5", "size": 50000, "percentage": 60.0},
            {"name": "Jupyter Notebook", "color": "#DA5B0B", "size": 20000, "percentage": 24.0},
            {"name": "R", "color": "#198CE7", "size": 8000, "percentage": 9.6},
            {"name": "Shell", "color": "#89e051", "size": 3000, "percentage": 3.6},
            {"name": "HTML", "color": "#e34c26", "size": 2000, "percentage": 2.4},
        ],
    }
