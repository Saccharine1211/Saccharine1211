#!/usr/bin/env python3
"""헤더(터미널)와 프로젝트 카드 SVG를 dark/light 두 벌로 만든다.

내용을 바꾸려면 아래 HEADER_ROWS, CARDS 를 고치고 `python3 scripts/build_assets.py`.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", green="#3fb950", blue="#58a6ff", purple="#bc8cff",
                 orange="#d29922", red="#f85149", chip="#21262d"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", green="#1a7f37", blue="#0969da", purple="#8250df",
                  orange="#9a6700", red="#cf222e", chip="#eaeef2"),
}

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = ("-apple-system,BlinkMacSystemFont,'Segoe UI','Apple SD Gothic Neo',"
        "'Noto Sans KR','Malgun Gothic',Helvetica,Arial,sans-serif")

# ── 헤더: kubectl 출력처럼 보이는 자기소개 ─────────────────────────────
HEADER_COLS = [("NAMESPACE", 34), ("NAME", 150), ("READY", 330), ("STATUS", 410), ("WHERE", 560)]
HEADER_ROWS = [
    # (namespace, name, ready, status, status_color, where)
    ("mori", "contentcare-api", "1/1", "Running", "green", "AWS · production"),
    ("echo", "echoport-was", "1/1", "Awarded 🏆", "orange", "AWS EKS · GCP GKE · on-prem k3s"),
    ("iris", "likelion-was", "1/1", "Completed", "blue", "AWS EKS · GKE · Argo CD"),
]


def header_svg(t: dict) -> str:
    w, h = 900, 330
    lines: list[str] = []
    step = 0.35  # 줄마다 나타나는 간격(초)

    def row(y: int, body: str, i: int) -> None:
        lines.append(
            f'<g class="ln" style="animation-delay:{i * step:.2f}s" transform="translate(0,{y})">{body}</g>'
        )

    def prompt(cmd: str) -> str:
        return (f'<text x="34" class="m"><tspan fill="{t["green"]}">jimin@prod</tspan>'
                f'<tspan fill="{t["muted"]}">:</tspan><tspan fill="{t["blue"]}">~</tspan>'
                f'<tspan fill="{t["muted"]}">$ </tspan><tspan fill="{t["text"]}">{escape(cmd)}</tspan></text>')

    i = 0
    row(78, prompt("whoami"), i); i += 1
    row(104, f'<text x="34" class="s b" fill="{t["text"]}">Jimin Kim <tspan fill="{t["muted"]}" class="n">(김지민)</tspan>'
             f'<tspan fill="{t["muted"]}" class="n">  ·  </tspan><tspan fill="{t["purple"]}">Backend &amp; Infra Engineer</tspan></text>', i); i += 1
    row(130, f'<text x="34" class="s" fill="{t["muted"]}">API 서버를 만들고, 그 서버가 멈추지 않는 길을 깝니다 — 멀티 클라우드 · 무중단 이전 · 관측</text>', i); i += 1
    row(170, prompt("kubectl get deploy -A -l owner=jimin"), i); i += 1
    head = "".join(f'<text x="{x}" class="m" fill="{t["muted"]}">{n}</text>' for n, x in HEADER_COLS)
    row(196, head, i); i += 1
    y = 220
    for ns, name, ready, status, color, where in HEADER_ROWS:
        cells = [
            (HEADER_COLS[0][1], ns, t["muted"]),
            (HEADER_COLS[1][1], name, t["text"]),
            (HEADER_COLS[2][1], ready, t["text"]),
            (HEADER_COLS[3][1], status, t[color]),
            (HEADER_COLS[4][1], where, t["muted"]),
        ]
        row(y, "".join(f'<text x="{x}" class="m" fill="{c}">{escape(v)}</text>' for x, v, c in cells), i)
        i += 1
        y += 24
    row(y + 16, prompt("") + f'<rect class="cur" x="166" y="-13" width="9" height="17" fill="{t["text"]}"/>', i)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Jimin Kim — Backend &amp; Infra Engineer">
<style>
.m{{font:14px {MONO};}}
.s{{font:15px {SANS};}}
.b{{font-weight:600;font-size:17px}}
.n{{font-weight:400;font-size:15px}}
.ln{{opacity:0;animation:in .35s ease-out forwards}}
@keyframes in{{to{{opacity:1}}}}
.cur{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.ln{{opacity:1;animation:none}}.cur{{animation:none}}}}
</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>
<path d="M1 13a12 12 0 0 1 12-12h{w-26}a12 12 0 0 1 12 12v27H1z" fill="{t["panel"]}"/>
<line x1="1" y1="40" x2="{w-1}" y2="40" stroke="{t["border"]}"/>
<circle cx="24" cy="21" r="6" fill="#ff5f57"/><circle cx="44" cy="21" r="6" fill="#febc2e"/><circle cx="64" cy="21" r="6" fill="#28c840"/>
<text x="{w/2}" y="26" text-anchor="middle" class="m" fill="{t["muted"]}">jimin@prod: ~ — zsh</text>
{chr(10).join(lines)}
</svg>
'''


# ── 프로젝트 카드 ────────────────────────────────────────────────────
CARDS = [
    dict(slug="echoport", badge="🏆 SoftBank Hackathon 2026 본선 우수상(2위)", badge_color="orange",
         title="EchoPort", subtitle="멀티 클라우드 무중단 이전(BCDR) 플랫폼",
         role="Team Echo · API 서버 · 인프라 · 시연 앱",
         metrics=[("11s", "도쿄 → 서울 긴급 이전"), ("0/149", "판정 요청 중 실패"), ("123", "merged PRs")],
         tags=["FastAPI", "PostgreSQL", "EKS", "GKE", "k3s", "Envoy", "Terraform"]),
    dict(slug="contentcare", badge="주식회사 모리 · 2025.09 ~ 재직 중", badge_color="green",
         title="ContentCare", subtitle="B2B 콘텐츠 보안 서비스",
         role="리드 엔지니어 · 백엔드 · 인프라 · 앱 출시",
         metrics=[("1,186", "merged PRs"), ("7/8", "사내 주요 레포 커밋 1위"), ("14개월", "운영 중")],
         tags=["Node.js", "Python", "AWS", "Docker", "Flutter"]),
    dict(slug="likelion", badge="SoftBank Hackathon 2026 예선 · Team Iris", badge_color="blue",
         title="Likelion", subtitle="코드만 올리면 빌드·배포·AI 진단까지",
         role="API 서버 · 온프레미스 타깃 · CLI",
         metrics=[("133", "merged PRs"), ("+2", "배포 타깃 GKE·온프렘"), ("v0.4", "CLI 릴리스")],
         tags=["FastAPI", "Argo CD", "EKS", "GKE", "Tailscale", "TypeScript CLI"]),
    dict(slug="media-pipeline", badge="Public · 레퍼런스 구현", badge_color="purple",
         title="Event-Driven Media Processing", subtitle="중복 전달·부분 실패에 안전한 비동기 처리",
         role="설계 · 구현 · IaC",
         metrics=[("at-least-once", "멱등 처리"), ("FIFO+DLQ", "재시도 격리"), ("OIDC", "키 없는 배포")],
         tags=["TypeScript", "S3", "SQS", "Lambda", "DynamoDB", "CDK"]),
]


def text_width(s: str, size: float) -> float:
    """대략적인 글자 폭(한글은 넓게)."""
    wide = sum(1 for ch in s if ord(ch) > 0x2E80)
    return (len(s) - wide) * size * 0.6 + wide * size * 1.0


def card_svg(c: dict, t: dict) -> str:
    w, h = 440, 232
    acc = t[c["badge_color"]]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(c["title"])}">',
           f'<style>.m{{font:12px {MONO}}}.s{{font-family:{SANS}}}</style>',
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>',
           f'<rect x="1" y="1" width="5" height="{h-2}" rx="2" fill="{acc}"/>',
           f'<text x="24" y="32" class="s" font-size="12.5" font-weight="600" fill="{acc}">{escape(c["badge"])}</text>',
           f'<text x="24" y="64" class="s" font-size="22" font-weight="700" fill="{t["text"]}">{escape(c["title"])}</text>',
           f'<text x="24" y="88" class="s" font-size="13.5" fill="{t["text"]}">{escape(c["subtitle"])}</text>',
           f'<text x="24" y="108" class="s" font-size="12.5" fill="{t["muted"]}">{escape(c["role"])}</text>']
    # 지표 3칸
    colw = (w - 48) / 3
    for k, (v, label) in enumerate(c["metrics"]):
        x = 24 + k * colw
        out.append(f'<rect x="{x}" y="122" width="{colw-8}" height="54" rx="8" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        vs = min(17.0, 17.0 * (colw - 26) / max(text_width(v, 17) * 0.92, 1))
        ls = min(10.5, 10.5 * (colw - 24) / max(text_width(label, 10.5) * 0.92, 1))
        out.append(f'<text x="{x+10}" y="146" class="s" font-size="{vs:.1f}" font-weight="700" fill="{t["text"]}">{escape(v)}</text>')
        out.append(f'<text x="{x+10}" y="165" class="s" font-size="{ls:.1f}" fill="{t["muted"]}">{escape(label)}</text>')
    # 스택 칩
    x, y = 24, 196
    for tag in c["tags"]:
        tw = text_width(tag, 11.5) + 16
        if x + tw > w - 20:
            break
        out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="22" rx="11" fill="{t["chip"]}"/>')
        out.append(f'<text x="{x+8}" y="{y+15}" class="m" font-size="11.5" fill="{t["muted"]}">{escape(tag)}</text>')
        x += tw + 6
    out.append("</svg>\n")
    return "\n".join(out)


def divider_svg(t: dict) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="16" viewBox="0 0 900 16">'
            f'<line x1="0" y1="8" x2="900" y2="8" stroke="{t["border"]}" stroke-dasharray="4 6"/>'
            f'<circle cx="450" cy="8" r="3.5" fill="{t["green"]}"/></svg>\n')


def main() -> None:
    (ASSETS / "cards").mkdir(parents=True, exist_ok=True)
    for name, t in THEMES.items():
        (ASSETS / f"header-{name}.svg").write_text(header_svg(t), encoding="utf-8")
        (ASSETS / f"divider-{name}.svg").write_text(divider_svg(t), encoding="utf-8")
        for c in CARDS:
            (ASSETS / "cards" / f'{c["slug"]}-{name}.svg').write_text(card_svg(c, t), encoding="utf-8")
    print("assets built:", sorted(p.relative_to(ROOT).as_posix() for p in ASSETS.rglob("*.svg")))


if __name__ == "__main__":
    main()
