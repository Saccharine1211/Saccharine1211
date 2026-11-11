#!/usr/bin/env python3
"""README의 Recently 세 칸(최근 병합 PR · 최근 리뷰 · 최근 작업한 저장소)을 다시 쓴다.

simonw/simonw 방식: 표식 주석 사이만 바꾸고 나머지는 건드리지 않는다.
공개 저장소만 다룬다(비공개 회사 저장소 이름이 새지 않게 is:public / privacy:PUBLIC).
실행: GITHUB_TOKEN=... python3 scripts/update_readme.py
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
# 프로필 방향(백엔드 + 인프라)과 무관한 프런트엔드 레포 활동은 Recently에서 뺀다.
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
    """최근 순서대로 고르되 한 저장소에서 per_repo개까지만(한 레포가 칸을 다 채우지 않게)."""
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
    nodes.sort(key=lambda n: n["pushedAt"] or "", reverse=True)  # API 정렬이 믿을 만하지 않아 직접 정렬
    out = []
    for n in nodes:
        if n["isFork"] or SKIP_REPO.search(n["nameWithOwner"]) or n["nameWithOwner"].lower() == f"{LOGIN}/{LOGIN}".lower():
            continue
        desc = f'<br><sub>{clean(n["description"], 46)}</sub>' if n["description"] else ""
        owner, name = n["nameWithOwner"].split("/", 1)
        owner = "개인" if owner.lower() == LOGIN.lower() else owner
        out.append(f'- [{name}]({n["url"]}){desc}<br><sub>{owner} · {n["pushedAt"][:10]}</sub>')
        if len(out) == N:
            break
    return out


def replace(text: str, marker: str, lines: list[str]) -> str:
    block = "\n".join(lines) if lines else "- 아직 없음"
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
