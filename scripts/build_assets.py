#!/usr/bin/env python3
"""Generate the animated SVG cards used in README.md.

Edit the content in the DATA section, then run:
    python scripts/build_assets.py

GitHub renders README images as <img>, so the SVGs use only SMIL animation
(no JavaScript, no external fonts or images).
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape as e

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ---------------------------------------------------------------- theme
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Liberation Mono', Menlo, monospace"
BG, PANEL, BORDER = "#0d1117", "#161b22", "#30363d"
TEXT, SOFT, MUTED = "#e6edf3", "#c9d1d9", "#8b949e"
CYAN, VIOLET, GREEN, PINK, AMBER = "#36bcf7", "#a78bfa", "#3fb950", "#f472b6", "#f59e0b"
MONO_W = 0.62  # approx. monospace advance per font-size unit

# ---------------------------------------------------------------- data
NAME = ("Faheem", "Musthafa")
TAGLINE = "Full-Stack Developer · AI Builder"
PITCH = "Turning real business problems into reliable software."
LOCATION = "Kerala, India"

TERMINAL = [  # (command, output)
    ("whoami", "full-stack dev · ai builder"),
    ("cat stack.txt", "next.js · fastapi · supabase · gcp"),
    ("./ship --current", "building RateCheck ... live ✔"),
]

STATUS = [
    (GREEN, "Open to freelance & collaborations", True),
    (AMBER, "Building RateCheck", False),
    (VIOLET, "Exploring agentic AI · DevSecOps", False),
]

FEATURED = {
    "title": "RateCheck",
    "desc": "AI-powered freelance pricing intelligence that converts project "
            "briefs into structured cost and scope reports.",
    "tech": ["Next.js", "Supabase", "OpenRouter", "Redis", "Resend", "Vercel"],
    "link": "rate-check.vercel.app",
}

PROJECTS = [
    dict(slug="kerala-ai-checker", title="Kerala AI Checker", tag="AI · SCAM DETECTION",
         initials="KA", accent=CYAN, live=True,
         desc="A Malayalam and Manglish scam-message analyser that helps elderly "
              "and non-technical users spot suspicious WhatsApp and SMS messages.",
         tech=["Next.js", "Gemini", "Tailwind", "Cloud Run"]),
    dict(slug="routereport-live", title="RouteReport Live", tag="CIVIC TECH · MAPS",
         initials="RR", accent=GREEN, live=False,
         desc="Community-driven road-condition reporting with live reports, maps, "
              "location detection, filters and analytics.",
         tech=["React", "TypeScript", "Supabase", "Leaflet", "PostgreSQL"]),
    dict(slug="dadarch", title="DadArch", tag="PORTFOLIO · DESIGN",
         initials="DA", accent=AMBER, live=False,
         desc="A modern architecture portfolio focused on project presentation, "
              "responsive design and a premium visual experience.",
         tech=["Responsive UI", "Vercel", "DNS"]),
    dict(slug="iedc-mcas", title="IEDC MCAS Website", tag="COMMUNITY · EVENTS",
         initials="IE", accent=PINK, live=False,
         desc="A college innovation-community website showcasing programmes, "
              "events, activities and student initiatives.",
         tech=["Web", "Responsive", "Events"]),
    dict(slug="lms-backend", title="LMS Backend", tag="BACKEND · EDTECH",
         initials="LM", accent=VIOLET, live=False,
         desc="Backend foundation for learning-management workflows, "
              "authentication, data modelling and educational services.",
         tech=["Backend APIs", "Auth", "Data modelling"]),
    dict(slug="self-hosted-guide", title="Self-Hosted Guide", tag="INFRA · GUIDES",
         initials="SH", accent=CYAN, live=False,
         desc="Practical notes and guides for running tools, services and "
              "infrastructure on personal hardware.",
         tech=["Linux", "Docker", "Nginx", "Cloudflare"]),
]

STACK_ROWS = [
    [("Python", CYAN), ("TypeScript", CYAN), ("JavaScript", CYAN), ("Bash", CYAN),
     ("C++", CYAN), ("React", VIOLET), ("Next.js", VIOLET), ("Vite", VIOLET),
     ("Tailwind", VIOLET), ("Flutter", VIOLET), ("Node.js", GREEN), ("FastAPI", GREEN),
     ("Django", GREEN), ("Express", GREEN)],
    [("PostgreSQL", AMBER), ("Redis", AMBER), ("Supabase", AMBER), ("Firebase", AMBER),
     ("GCP", PINK), ("Vercel", PINK), ("Cloudflare", PINK), ("Docker", PINK),
     ("Terraform", PINK), ("Nginx", PINK), ("Linux", PINK), ("Git", PINK)],
]
STACK_LEGEND = [(CYAN, "languages"), (VIOLET, "frontend"), (GREEN, "backend"),
                (AMBER, "data"), (PINK, "cloud & devops")]

JOURNEY = [  # (era, title, sub, accent, current)
    ("ORIGINS", "Cyber-Security", "Prodigy InfoTech · intern", PINK, False),
    ("APR 2026", "Full-Stack Intern", "Lincole Group", AMBER, False),
    ("JUL 2026 → NOW", "Full-Stack Engineer", "Lincole Group", CYAN, True),
    ("ONGOING", "Freelance", "Web · AI · Automation", GREEN, False),
]


# ---------------------------------------------------------------- helpers
def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}">'
            f'<title>{e(title)}</title>{body}</svg>\n')


def fade_in(begin, dy=10, dur=0.7):
    """Children for a <g opacity="0"> that fades and slides up into place."""
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
            f'dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0 {dy}" to="0 0" begin="{begin:.2f}s" dur="{dur}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/>')


def pulse_dot(cx, cy, color, r=4):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.5">'
            f'<animate attributeName="r" values="{r};{r * 2.6};{r}" dur="2s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.5;0;0.5" dur="2s" repeatCount="indefinite"/>'
            f'</circle><circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


def pill(x, y, text, color, size=11, h=22):
    """Mono pill at (x, y) top-left. Returns (svg, width)."""
    w = len(text) * size * MONO_W + 18
    s = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
         f'fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.35"/>'
         f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" '
         f'font-family="{MONO}" font-size="{size}" fill="{color}">{e(text)}</text>')
    return s, w


def pill_row(x, y, items, color, max_w, size=11, gap=6):
    out, cx = [], x
    for t in items:
        w = len(t) * size * MONO_W + 18
        if cx + w > x + max_w:
            break
        s, w = pill(cx, y, t, color, size)
        out.append(s)
        cx += w + gap
    return "".join(out)


def typed(x, y, text, begin, color, size=13, cps=0.05, uid="t"):
    """Text revealed one character at a time. Returns (svg, end_time)."""
    cw = size * MONO_W
    vals = ";".join(f"{i * cw:.1f}" for i in range(len(text) + 1))
    dur = max(len(text) * cps, 0.1)
    s = (f'<clipPath id="{uid}"><rect x="{x}" y="{y - size}" height="{size * 1.6}" width="0">'
         f'<animate attributeName="width" values="{vals}" calcMode="discrete" '
         f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
         f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{color}" '
         f'clip-path="url(#{uid})">{e(text)}</text>')
    return s, begin + dur


def card_bg(w, h, rx=16):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" '
            f'fill="{BG}" stroke="{BORDER}"/>')


# ---------------------------------------------------------------- cards
def hero():
    W, H = 840, 360
    b = [f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity="0.04"/></pattern>
<filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="50"/></filter>
<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="440" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;400 0;0 0" dur="8s" repeatCount="indefinite"/></linearGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<circle cx="140" cy="70" r="110" fill="{CYAN}" opacity="0.22" filter="url(#blur)"><animate attributeName="cx" values="140;300;140" dur="14s" repeatCount="indefinite"/></circle>
<circle cx="720" cy="300" r="130" fill="{VIOLET}" opacity="0.22" filter="url(#blur)"><animate attributeName="cy" values="300;140;300" dur="12s" repeatCount="indefinite"/></circle>
<circle cx="420" cy="380" r="90" fill="{PINK}" opacity="0.14" filter="url(#blur)"><animate attributeName="cx" values="420;560;420" dur="16s" repeatCount="indefinite"/></circle>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>''']

    # left column
    b.append(f'<g opacity="0">{fade_in(0.2)}<text x="44" y="84" font-family="{MONO}" '
             f'font-size="13" letter-spacing="3" fill="{CYAN}">HELLO, WORLD — I’M</text></g>')
    b.append(f'<g opacity="0">{fade_in(0.45, 16)}'
             f'<text x="40" y="146" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#name)">{NAME[0]}</text>'
             f'<text x="40" y="206" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#name)">{NAME[1]}</text></g>')
    b.append(f'<g opacity="0">{fade_in(0.8)}'
             f'<text x="44" y="244" font-family="{SANS}" font-size="17" font-weight="600" fill="{SOFT}">{e(TAGLINE)}</text>'
             f'<text x="44" y="268" font-family="{SANS}" font-size="14" fill="{MUTED}">{e(PITCH)}</text></g>')
    loc_w = len(LOCATION) * 11 * MONO_W + 36
    b.append(f'<g opacity="0">{fade_in(1.1)}'
             f'<rect x="44" y="290" width="{loc_w:.1f}" height="26" rx="13" fill="{PANEL}" stroke="{BORDER}"/>'
             f'{pulse_dot(60, 303, GREEN, 3.5)}'
             f'<text x="72" y="307" font-family="{MONO}" font-size="11" fill="{SOFT}">{e(LOCATION)}</text></g>')

    # terminal
    tx, ty, tw, th = 462, 52, 340, 256
    b.append(f'<g opacity="0">{fade_in(0.5, 14)}'
             f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{BG}" fill-opacity="0.92" stroke="{BORDER}"/>'
             f'<path d="M{tx} {ty + 32}V{ty + 12}a12 12 0 0 1 12-12H{tx + tw - 12}a12 12 0 0 1 12 12V{ty + 32}Z" fill="{PANEL}"/>'
             f'<line x1="{tx}" y1="{ty + 32}" x2="{tx + tw}" y2="{ty + 32}" stroke="{BORDER}"/>'
             f'<circle cx="{tx + 18}" cy="{ty + 16}" r="5" fill="#ff5f56"/>'
             f'<circle cx="{tx + 34}" cy="{ty + 16}" r="5" fill="#ffbd2e"/>'
             f'<circle cx="{tx + 50}" cy="{ty + 16}" r="5" fill="#27c93f"/>'
             f'<text x="{tx + tw / 2}" y="{ty + 20}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">faheem@dev: ~</text></g>')
    t, y, lx = 1.2, ty + 62, tx + 18
    for i, (cmd, out) in enumerate(TERMINAL):
        b.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                 f'<text x="{lx}" y="{y}" font-family="{MONO}" font-size="13" fill="{GREEN}">$</text></g>')
        s, t = typed(lx + 16, y, cmd, t + 0.25, TEXT, uid=f"c{i}")
        b.append(s)
        b.append(f'<g opacity="0">{fade_in(t + 0.2, 4, 0.4)}<text x="{lx}" y="{y + 24}" '
                 f'font-family="{MONO}" font-size="13" fill="{CYAN if i < 2 else GREEN}">{e(out)}</text></g>')
        t += 0.6
        y += 56
    b.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
             f'<text x="{lx}" y="{y}" font-family="{MONO}" font-size="13" fill="{GREEN}">$</text>'
             f'<rect x="{lx + 16}" y="{y - 12}" width="8" height="15" fill="{CYAN}">'
             f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect></g>')
    return svg(W, H, "".join(b), "Faheem Musthafa — Full-Stack Developer and AI Builder")


def status():
    W, H, size = 840, 56, 12
    widths = [len(t) * size * MONO_W + 46 for _, t, _ in STATUS]
    gap = 12
    x = (W - sum(widths) - gap * (len(STATUS) - 1)) / 2
    b = []
    for i, ((color, text, live), w) in enumerate(zip(STATUS, widths)):
        dot = pulse_dot(x + 18, 28, color, 4) if live else \
            f'<rect x="{x + 14:.1f}" y="24" width="8" height="8" rx="2" fill="{color}" transform="rotate(45 {x + 18:.1f} 28)"/>'
        b.append(f'<g opacity="0">{fade_in(0.15 * i, 6, 0.5)}'
                 f'<rect x="{x:.1f}" y="12" width="{w:.1f}" height="32" rx="16" fill="{PANEL}" stroke="{color}" stroke-opacity="0.4"/>'
                 f'{dot}<text x="{x + 32:.1f}" y="32" font-family="{MONO}" font-size="{size}" fill="{SOFT}">{e(text)}</text></g>')
        x += w + gap
    return svg(W, H, "".join(b), "Current status")


def featured():
    W, H = 840, 260
    f = FEATURED
    b = [f'''<defs><linearGradient id="fg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<radialGradient id="glow" cx="0.8" cy="0.5" r="0.6"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.18"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient></defs>
{card_bg(W, H)}<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#glow)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#fg)" stroke-width="2" pathLength="1000" stroke-dasharray="160 840" stroke-linecap="round">
<animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="6s" repeatCount="indefinite"/></rect>''']
    b.append(f'<text x="36" y="48" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{AMBER}">★ CURRENT BUILD</text>'
             f'<text x="34" y="94" font-family="{SANS}" font-size="38" font-weight="800" fill="{TEXT}">{e(f["title"])}</text>')
    for i, line in enumerate(wrap(f["desc"], 50)):
        b.append(f'<text x="36" y="{126 + i * 21}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{e(line)}</text>')
    rows = [f["tech"][:3], f["tech"][3:]]
    for i, row in enumerate(rows):
        b.append(pill_row(36, 186 + i * 28, row, CYAN, 400))

    # brief -> AI -> report flow
    bx, by = 470, 70
    b.append(f'<g font-family="{MONO}" font-size="10" fill="{MUTED}" text-anchor="middle">'
             f'<text x="{bx + 44}" y="{by + 136}">project brief</text>'
             f'<text x="{bx + 170}" y="{by + 136}">AI analysis</text>'
             f'<text x="{bx + 296}" y="{by + 136}">cost &amp; scope</text></g>')
    # brief doc
    b.append(f'<rect x="{bx}" y="{by}" width="88" height="110" rx="10" fill="{PANEL}" stroke="{BORDER}"/>')
    for i, w in enumerate([60, 48, 64, 40, 56]):
        b.append(f'<rect x="{bx + 14}" y="{by + 18 + i * 17}" width="{w}" height="6" rx="3" fill="{MUTED}" fill-opacity="0.35"/>')
    # AI node
    cx, cy = bx + 170, by + 55
    b.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{VIOLET}" stroke-opacity="0.5">'
             f'<animate attributeName="r" values="34;46;34" dur="2.4s" repeatCount="indefinite"/>'
             f'<animate attributeName="stroke-opacity" values="0.5;0;0.5" dur="2.4s" repeatCount="indefinite"/></circle>'
             f'<circle cx="{cx}" cy="{cy}" r="34" fill="{PANEL}" stroke="url(#fg)" stroke-width="2"/>'
             f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{TEXT}">LLM</text>')
    # report
    rx = bx + 252
    b.append(f'<rect x="{rx}" y="{by}" width="88" height="110" rx="10" fill="{PANEL}" stroke="{BORDER}"/>')
    for i, (lbl, w, col) in enumerate([("scope", 54, CYAN), ("cost", 40, VIOLET), ("time", 62, PINK)]):
        yy = by + 22 + i * 30
        b.append(f'<text x="{rx + 12}" y="{yy}" font-family="{MONO}" font-size="9" fill="{MUTED}">{lbl}</text>'
                 f'<rect x="{rx + 12}" y="{yy + 6}" width="0" height="7" rx="3.5" fill="{col}">'
                 f'<animate attributeName="width" values="0;{w};{w};0" keyTimes="0;0.3;0.85;1" dur="4s" begin="{0.6 + i * 0.2:.1f}s" repeatCount="indefinite"/></rect>')
    # connectors with travelling dots
    for i, (x1, x2) in enumerate([(bx + 92, cx - 38), (cx + 38, rx - 4)]):
        b.append(f'<line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="{BORDER}" stroke-width="2" stroke-dasharray="4 4">'
                 f'<animate attributeName="stroke-dashoffset" from="8" to="0" dur="0.6s" repeatCount="indefinite"/></line>'
                 f'<circle r="3.5" fill="{CYAN}"><animateMotion path="M{x1} {cy}H{x2}" dur="2s" begin="{i:.1f}s" repeatCount="indefinite"/></circle>')
    b.append(f'<text x="{W - 30}" y="48" text-anchor="end" font-family="{MONO}" font-size="11" fill="{VIOLET}">{e(f["link"])} ↗</text>')
    return svg(W, H, "".join(b), f'{f["title"]} — {f["desc"]}')


def project_card(p, i):
    W, H, a = 410, 200, p["accent"]
    b = [f'''<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
<stop offset="0.5" stop-color="#fff" stop-opacity="0.07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="top" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient></defs>
{card_bg(W, H, 14)}
<g clip-path="url(#c)"><rect width="{W}" height="3" fill="url(#top)"/>
<rect x="-160" y="-40" width="120" height="{H + 80}" fill="url(#shine)" transform="skewX(-20)">
<animateTransform attributeName="transform" type="translate" values="0 0;720 0;720 0" keyTimes="0;0.3;1" dur="7s" begin="{i * 0.7:.1f}s" repeatCount="indefinite" additive="sum"/></rect></g>''']
    b.append(f'<rect x="22" y="22" width="38" height="38" rx="10" fill="{a}" fill-opacity="0.12" stroke="{a}" stroke-opacity="0.5"/>'
             f'<text x="41" y="46" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{a}">{p["initials"]}</text>'
             f'<text x="72" y="39" font-family="{SANS}" font-size="18" font-weight="700" fill="{TEXT}">{e(p["title"])}</text>'
             f'<text x="72" y="57" font-family="{MONO}" font-size="9.5" letter-spacing="1.2" fill="{a}">{e(p["tag"])}</text>')
    if p["live"]:
        b.append(f'{pulse_dot(W - 62, 36, GREEN, 3.5)}<text x="{W - 52}" y="40" font-family="{MONO}" font-size="10" fill="{GREEN}">LIVE</text>')
    else:
        b.append(f'<text x="{W - 24}" y="42" text-anchor="end" font-family="{SANS}" font-size="16" fill="{MUTED}">↗</text>')
    for j, line in enumerate(wrap(p["desc"], 54)[:3]):
        b.append(f'<text x="24" y="{92 + j * 19}" font-family="{SANS}" font-size="12.5" fill="{MUTED}">{e(line)}</text>')
    b.append(pill_row(24, H - 40, p["tech"], a, W - 48, size=10))
    return svg(W, H, "".join(b), f'{p["title"]} — {p["desc"]}')


def stack():
    W, H, size, gap = 840, 142, 12, 10

    def row(items, y, reverse, dur_per_px=0.035):
        parts, x = [], 0
        for name, col in items:
            w = len(name) * size * MONO_W + 34
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="32" rx="16" fill="{PANEL}" stroke="{col}" stroke-opacity="0.35"/>'
                         f'<circle cx="{x + 15:.1f}" cy="{y + 16}" r="4" fill="{col}"/>'
                         f'<text x="{x + 25:.1f}" y="{y + 20.5}" font-family="{MONO}" font-size="{size}" fill="{SOFT}">{e(name)}</text>')
            x += w + gap
        seq = "".join(parts)
        frm, to = (f"-{x:.1f} 0", "0 0") if reverse else ("0 0", f"-{x:.1f} 0")
        return (f'<g><animateTransform attributeName="transform" type="translate" from="{frm}" to="{to}" '
                f'dur="{x * dur_per_px:.1f}s" repeatCount="indefinite"/>'
                f'{seq}<g transform="translate({x:.1f} 0)">{seq}</g><g transform="translate({2 * x:.1f} 0)">{seq}</g></g>')

    b = [f'''<defs><linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.08" stop-color="#fff"/><stop offset="0.92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>
{card_bg(W, H)}<g mask="url(#m)">{row(STACK_ROWS[0], 20, False)}{row(STACK_ROWS[1], 64, True)}</g>''']
    widths = [len(t) * 10 * MONO_W + 30 for _, t in STACK_LEGEND]
    x = (W - sum(widths)) / 2
    for (col, t), w in zip(STACK_LEGEND, widths):
        b.append(f'<circle cx="{x + 6:.1f}" cy="{H - 24}" r="4" fill="{col}"/>'
                 f'<text x="{x + 16:.1f}" y="{H - 20.5}" font-family="{MONO}" font-size="10" fill="{MUTED}">{e(t)}</text>')
        x += w
    return svg(W, H, "".join(b), "Tech stack")


def journey():
    W, H = 840, 190
    n = len(JOURNEY)
    xs = [110 + i * (W - 220) / (n - 1) for i in range(n)]
    ly = 82
    b = [f'''<defs><linearGradient id="line" gradientUnits="userSpaceOnUse" x1="{xs[0]}" y1="0" x2="{xs[-1]}" y2="0">
<stop offset="0" stop-color="{PINK}"/><stop offset="0.4" stop-color="{AMBER}"/><stop offset="0.7" stop-color="{CYAN}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>
{card_bg(W, H)}
<line x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="{BORDER}" stroke-width="2"/>
<line x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="url(#line)" stroke-width="2.5" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">
<animate attributeName="stroke-dashoffset" from="100" to="0" dur="2s" begin="0.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/></line>''']
    for i, ((era, title, sub, col, current), x) in enumerate(zip(JOURNEY, xs)):
        t = 0.2 + 2 * i / (n - 1)
        ring = (f'<circle cx="{x:.1f}" cy="{ly}" r="9" fill="none" stroke="{col}">'
                f'<animate attributeName="r" values="9;20;9" dur="2s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite"/></circle>') if current else ""
        b.append(f'<g opacity="0">{fade_in(t, 8, 0.6)}'
                 f'<text x="{x:.1f}" y="{ly - 26}" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="1.2" fill="{col}">{e(era)}</text>'
                 f'{ring}<circle cx="{x:.1f}" cy="{ly}" r="9" fill="{BG}" stroke="{col}" stroke-width="2.5"/>'
                 f'<circle cx="{x:.1f}" cy="{ly}" r="4" fill="{col}"/>'
                 f'<text x="{x:.1f}" y="{ly + 42}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">{e(title)}</text>'
                 f'<text x="{x:.1f}" y="{ly + 63}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{e(sub)}</text></g>')
    return svg(W, H, "".join(b), "Journey: " + ", ".join(f"{t} ({s})" for _, t, s, _, _ in JOURNEY))


def main():
    OUT.mkdir(exist_ok=True)
    files = {"hero.svg": hero(), "status.svg": status(), "featured.svg": featured(),
             "stack.svg": stack(), "journey.svg": journey()}
    for i, p in enumerate(PROJECTS):
        files[f"project-{p['slug']}.svg"] = project_card(p, i)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8", newline="\n")
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
