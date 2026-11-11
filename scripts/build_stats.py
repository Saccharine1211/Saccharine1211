#!/usr/bin/env python3
"""기여 달력으로 '모니터링 패널' 모양 통계 SVG를 만든다 (dark/light).

공개 프로필에 비공개 기여 수도 보이게 설정돼 있어서 GITHUB_TOKEN 만으로 같은 숫자가 나온다.
실행: GITHUB_TOKEN=... python3 scripts/build_stats.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

from build_assets import ASSETS, MONO, SANS, THEMES

LOGIN = os.environ.get("PROFILE_LOGIN", "Saccharine1211")
KST = dt.timezone(dt.timedelta(hours=9))
QUERY = """
query($login:String!){ user(login:$login){
  contributionsCollection{ contributionCalendar{ totalContributions
    weeks{ contributionDays{ date contributionCount weekday } } } } } }
"""


def fetch() -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]


def summarize(weeks: list[dict]) -> dict:
    days = [d for w in weeks for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    today = dt.datetime.now(KST).date().isoformat()
    days = [d for d in days if d["date"] <= today]
    counts = [d["contributionCount"] for d in days]

    longest = cur = 0
    for c in counts:
        cur = cur + 1 if c else 0
        longest = max(longest, cur)
    current = 0
    for c in reversed(counts[:-1] if counts and counts[-1] == 0 else counts):  # 오늘 0이면 어제부터
        if not c:
            break
        current += 1

    weekday_tot = [0] * 7
    for d in days:
        weekday_tot[d["weekday"]] += d["contributionCount"]
    names = ["일", "월", "화", "수", "목", "금", "토"]

    weekly = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks][-52:]
    return dict(
        total=sum(counts), active=sum(1 for c in counts if c), days=len(counts),
        longest=longest, current=current, busiest=names[weekday_tot.index(max(weekday_tot))] + "요일",
        weekly=weekly, peak=max(weekly) if weekly else 0,
        updated=dt.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),
    )


def stats_svg(s: dict, t: dict) -> str:
    w, h = 900, 250
    stat = [("지난 1년 기여", f'{s["total"]:,}', t["text"]),
            ("활동한 날", f'{s["active"]}/{s["days"]}일', t["text"]),
            ("최장 연속", f'{s["longest"]}일', t["green"]),
            ("현재 연속", f'{s["current"]}일', t["green"]),
            ("가장 바쁜 요일", s["busiest"], t["purple"])]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="GitHub 기여 통계">',
           f'<style>.m{{font:11px {MONO}}}.s{{font-family:{SANS}}}'
           f'.bar{{transform-origin:bottom;transform-box:fill-box;animation:up .8s ease-out both}}'
           f'@keyframes up{{from{{transform:scaleY(0)}}}}'
           f'@media (prefers-reduced-motion:reduce){{.bar{{animation:none}}}}</style>',
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>',
           f'<circle cx="24" cy="25" r="5" fill="{t["green"]}"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>',
           f'<text x="38" y="30" class="s" font-size="14" font-weight="600" fill="{t["text"]}">github_contributions_total</text>',
           f'<text x="{w-24}" y="30" text-anchor="end" class="m" fill="{t["muted"]}">user="{LOGIN}" · updated {s["updated"]}</text>']
    colw = (w - 48) / len(stat)
    for i, (label, val, color) in enumerate(stat):
        x = 24 + i * colw
        out.append(f'<rect x="{x}" y="46" width="{colw-10}" height="58" rx="8" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        out.append(f'<text x="{x+12}" y="66" class="s" font-size="11" fill="{t["muted"]}">{label}</text>')
        out.append(f'<text x="{x+12}" y="92" class="s" font-size="20" font-weight="700" fill="{color}">{val}</text>')
    # 주간 막대 52개
    top, bottom = 124, 222
    weekly, peak = s["weekly"], max(s["peak"], 1)
    bw = (w - 48) / max(len(weekly), 1)
    out.append(f'<line x1="24" y1="{bottom}" x2="{w-24}" y2="{bottom}" stroke="{t["border"]}"/>')
    out.append(f'<line x1="24" y1="{top}" x2="{w-24}" y2="{top}" stroke="{t["border"]}" stroke-dasharray="3 5"/>')
    out.append(f'<text x="{w-24}" y="{top-4}" text-anchor="end" class="m" fill="{t["muted"]}">peak {peak}/wk · √scale</text>')
    for i, v in enumerate(weekly):
        bh = max((bottom - top - 6) * (v / peak) ** 0.5, 1.5 if v else 0)  # 제곱근 눈금: 몰린 주가 나머지를 뭉개지 않게
        if not bh:
            continue
        x = 24 + i * bw + 1.5
        op = 0.45 + 0.55 * (v / peak) ** 0.5
        out.append(f'<rect class="bar" style="animation-delay:{i*0.012:.3f}s" x="{x:.1f}" y="{bottom-bh:.1f}" '
                   f'width="{bw-3:.1f}" height="{bh:.1f}" rx="2" fill="{t["green"]}" fill-opacity="{op:.2f}"/>')
    out.append(f'<text x="24" y="{bottom+18}" class="m" fill="{t["muted"]}">52주 전</text>')
    out.append(f'<text x="{w-24}" y="{bottom+18}" text-anchor="end" class="m" fill="{t["muted"]}">이번 주</text>')
    out.append("</svg>\n")
    return "\n".join(out)


def main() -> None:
    s = summarize(fetch())
    for name, t in THEMES.items():
        (ASSETS / f"stats-{name}.svg").write_text(stats_svg(s, t), encoding="utf-8")
    print(json.dumps({k: v for k, v in s.items() if k != "weekly"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
