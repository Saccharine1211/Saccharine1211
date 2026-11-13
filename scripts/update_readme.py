#!/usr/bin/env python3
"""Rewrite the three Recently columns of the README (merged PRs, reviews, repositories).

simonw/simonw style: only the text between marker comments changes.
Public repositories only (is:public / privacy:PUBLIC), so private company repo names never leak.
Run: GITHUB_TOKEN=... python3 scripts/update_readme.py
"""
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

LOGIN = os.environ.get("PROFILE_LOGIN", "Saccharine1211")
README = Path(__file__).resolve().parent.parent / "README.md"
N = 5
# Front-end repos are outside the profile focus (backend + infra), so Recently skips them.
SKIP_REPO = re.compile(r"frontend|-web$|\.github\.io$", re.I)


def api(url: str, body: dict | None = None) -> dict:
    token = os.environ.get("GITHUB_TOKEN") or os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        url, data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"bearer {token}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json", "User-Agent": LOGIN},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if isinstance(data, dict) and data.get("errors"):
        raise SystemExit(data["errors"])
    return data


def search_prs(q: str) -> list[dict]:
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "sort": "updated", "order": "desc", "per_page": 50})
    return api(url)["items"]


def clean(title: str, limit: int = 58) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
    return title if len(title) <= limit else title[: limit - 1] + "…"


def pr_lines(items: list[dict], date_key: str, per_repo: int = 2) -> list[str]:
    """Newest first, at most per_repo items per repository so one repo cannot fill the column."""
    out, seen, count = [], set(), {}
    for it in items:
        repo = it["repository_url"].rsplit("/", 1)[-1]
        if SKIP_REPO.search(repo) or it["html_url"] in seen or count.get(repo, 0) >= per_repo:
            continue
        seen.add(it["html_url"])
        count[repo] = count.get(repo, 0) + 1
        date = (it.get(date_key) or it["updated_at"])[:10]
        out.append(f'- [{clean(it["title"])}]({it["html_url"]})<br><sub>{repo} · {date}</sub>')
        if len(out) == N:
            break
    return out


def repo_lines() -> list[str]:
    q = """query($login:String!){ user(login:$login){
      repositoriesContributedTo(first:100, privacy:PUBLIC, includeUserRepositories:true,
        contributionTypes:[COMMIT,PULL_REQUEST,REPOSITORY]){
        nodes{ nameWithOwner url description pushedAt isArchived isFork } } } }"""
    nodes = api("https://api.github.com/graphql", {"query": q, "variables": {"login": LOGIN}})[
        "data"]["user"]["repositoriesContributedTo"]["nodes"]
    nodes.sort(key=lambda n: n["pushedAt"] or "", reverse=True)  # the API order is unreliable, so sort here
    out = []
    for n in nodes:
        if n["isFork"] or SKIP_REPO.search(n["nameWithOwner"]) or n["nameWithOwner"].lower() == f"{LOGIN}/{LOGIN}".lower():
            continue
        desc = f'<br><sub>{clean(n["description"], 46)}</sub>' if n["description"] else ""
        owner, name = n["nameWithOwner"].split("/", 1)
        owner = "personal" if owner.lower() == LOGIN.lower() else owner
        out.append(f'- [{name}]({n["url"]}){desc}<br><sub>{owner} · {n["pushedAt"][:10]}</sub>')
        if len(out) == N:
            break
    return out


def replace(text: str, marker: str, lines: list[str]) -> str:
    block = "\n".join(lines) if lines else "- nothing yet"
    pat = re.compile(rf"(<!-- {marker} starts -->)(.*?)(<!-- {marker} ends -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"marker {marker} not found")
    return pat.sub(lambda m: f"{m.group(1)}\n{block}\n{m.group(3)}", text)


def main() -> None:
    text = README.read_text(encoding="utf-8")
    merged = search_prs(f"author:{LOGIN} is:pr is:merged is:public")
    reviewed = search_prs(f"reviewed-by:{LOGIN} -author:{LOGIN} is:pr is:public")
    text = replace(text, "recent_prs", pr_lines(merged, "closed_at"))
    text = replace(text, "recent_reviews", pr_lines(reviewed, "updated_at"))
    text = replace(text, "recent_repos", repo_lines())
    README.write_text(text, encoding="utf-8")
    print("README updated")


if __name__ == "__main__":
    main()
