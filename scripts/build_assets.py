#!/usr/bin/env python3
"""Build the profile README and its animated SVG cards.

Edit the CONTENT section, then run:
    python scripts/build_assets.py

Every card is generated twice (assets/light, assets/dark). The README shows
the one that matches the visitor's GitHub theme using GitHub's
`#gh-light-mode-only` / `#gh-dark-mode-only` link fragments, so switching the
GitHub theme switches the whole profile. SVGs use only SMIL animation and
system fonts, which is what GitHub's image proxy allows.
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape as e

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ================================================================ CONTENT
USER = "Faheem-Musthafa"
PROFILE = f"https://github.com/{USER}"
NAME = "Faheem Musthafa"
ROLE = "Full-stack engineer · AI builder"
TYPED = "building RateCheck — AI pricing for freelancers"
META = ["Available for freelance", "Kerala, India", "Lincole Group"]

FEATURED = dict(
    title="RateCheck",
    desc="Paste a project brief, get a structured cost and scope report. "
         "AI pricing intelligence for freelancers who are tired of guessing.",
    tech="Next.js · Supabase · OpenRouter · Redis · Resend · Vercel",
    url="https://rate-check.vercel.app",
)

PROJECTS = [
    dict(slug="kerala-ai-checker", title="Kerala AI Checker", live=True,
         url=f"{PROFILE}/kerala-digital-trust-or-whatsapp-fact-checker",
         desc="Checks WhatsApp and SMS messages for scams in Malayalam and "
              "Manglish, built for elderly and non-technical users.",
         tech="Next.js · Gemini · Tailwind · Cloud Run"),
    dict(slug="routereport-live", title="RouteReport Live", live=False,
         url=f"{PROFILE}/Route-Report-system",
         desc="Crowd-sourced road conditions with live reports, maps, "
              "location detection, filters and analytics.",
         tech="React · TypeScript · Supabase · Leaflet"),
    dict(slug="dadarch", title="DadArch", live=False,
         url=f"{PROFILE}/DadArch",
         desc="An architecture portfolio built around project storytelling, "
              "responsive layouts and a premium feel.",
         tech="Responsive UI · Vercel · DNS"),
    dict(slug="iedc-mcas", title="IEDC MCAS Website", live=False,
         url=f"{PROFILE}/IEDC-MCAS-website",
         desc="Home for a college innovation community: programmes, events "
              "and student initiatives in one place.",
         tech="Web · Responsive · Events"),
    dict(slug="lms-backend", title="LMS Backend", live=False,
         url=f"{PROFILE}/lms-backend",
         desc="The backend for learning platforms: authentication, data "
              "models and course workflows.",
         tech="APIs · Auth · Data modelling"),
    dict(slug="self-hosted-guide", title="Self-Hosted Guide", live=False,
         url=f"{PROFILE}/self-hosted-guide",
         desc="Field notes for running real services on your own hardware, "
              "from containers to tunnels.",
         tech="Linux · Docker · Nginx · Cloudflare"),
]

STACK = [
    ("Languages", "TypeScript · Python · JavaScript · Bash · C++"),
    ("Frontend", "React · Next.js · Vite · Tailwind CSS · Flutter"),
    ("Backend", "FastAPI · Node.js · Express · Django"),
    ("Data", "PostgreSQL · Supabase · Redis · Firebase"),
    ("Cloud", "GCP · Vercel · Cloudflare · Docker · Terraform · Nginx"),
    ("Exploring", "Agentic AI · DevSecOps · Multi-tenant SaaS"),
]

EXPERIENCE = [  # (when, role, where, current)
    ("Jul 2026 — now", "Full-Stack Engineer", "Lincole Group", True),
    ("Ongoing", "Freelance Developer", "Web apps, AI tools and automation", False),
    ("Apr 2026", "Full-Stack Engineering Intern", "Lincole Group", False),
    ("Earlier", "Cyber-Security Intern", "Prodigy InfoTech", False),
]

CONTACT_TITLE = "Let’s build something useful."
CONTACT_TEXT = "Open to full-stack apps, AI tools, SaaS MVPs, internal systems and automation."
BUTTONS = [  # (slug, label, href, primary)
    ("email", "Email me", "mailto:faheemcp241@gmail.com", True),
    ("linkedin", "LinkedIn", "https://linkedin.com/in/faheem-musthafa-cp", False),
    ("instagram", "Instagram", "https://instagram.com/faheem_cp", False),
]
MOTTO = "build useful things · learn fast · ship consistently"

# ================================================================ THEME
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
THEMES = {  # GitHub Primer colours, so the cards look native in each theme
    "light": dict(bg="#ffffff", surface="#f6f8fa", border="#d1d9e0", text="#1f2328",
                  muted="#59636e", subtle="#818b98", accent="#0969da", green="#1a7f37",
                  cell="#eff2f5"),
    "dark": dict(bg="#0d1117", surface="#151b23", border="#3d444d", text="#f0f6fc",
                 muted="#9198a1", subtle="#656c76", accent="#4493f8", green="#3fb950",
                 cell="#151b23"),
}
MONO_W, SANS_W = 0.6, 0.56  # rough advance per font-size unit
W = 840


# ================================================================ helpers
def svg(w, h, body, label, t=None):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{e(label)}" fill="none"><title>{e(label)}</title>{body}</svg>\n')


def appear(begin, dy=8, dur=0.6):
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" '
            f'begin="{begin:.2f}s" dur="{dur}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="0.2 0.8 0.2 1"/>')


def g_in(begin, inner, dy=8):
    return f'<g opacity="0">{appear(begin, dy)}{inner}</g>'


def text(x, y, s, size, fill, font=SANS, weight=400, anchor="start", ls=0, extra=""):
    ls_attr = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls_attr}{extra}>{e(s)}</text>')


def pulse(cx, cy, color, r=3.5):
    return (f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{color}" opacity="0.4">'
            f'<animate attributeName="r" values="{r};{r * 2.8};{r}" dur="2.2s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.4;0;0.4" dur="2.2s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{color}"/>')


def frame(w, h, c, rx=12):
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{c["bg"]}" stroke="{c["border"]}"/>'


def typed(x, y, s, begin, c, size=14, cps=0.045, uid="ty"):
    cw = size * MONO_W
    vals = ";".join(f"{i * cw:.1f}" for i in range(len(s) + 1))
    dur = len(s) * cps
    return (f'<clipPath id="{uid}"><rect x="{x}" y="{y - size}" height="{size * 1.6}" width="0">'
            f'<animate attributeName="width" values="{vals}" calcMode="discrete" begin="{begin:.2f}s" '
            f'dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
            + text(x, y, s, size, c["text"], MONO, extra=f' clip-path="url(#{uid})"')), begin + dur


def sun_moon(x, y, c, theme):
    if theme == "light":
        rays = "".join(
            f'<line x1="{x}" y1="{y - 9}" x2="{x}" y2="{y - 7}" stroke="{c["muted"]}" stroke-width="1.5" '
            f'stroke-linecap="round" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 45))
        icon = f'<circle cx="{x}" cy="{y}" r="4" stroke="{c["muted"]}" stroke-width="1.5"/>{rays}'
    else:
        icon = (f'<path d="M{x + 3} {y - 6.5}a7 7 0 1 0 4 9.5a5.5 5.5 0 0 1 -4 -9.5z" '
                f'stroke="{c["muted"]}" stroke-width="1.5" stroke-linejoin="round"/>')
    return icon + text(x + 14, y + 4, f"{theme} theme", 11, c["subtle"], MONO, anchor="start")


# ================================================================ cards
def hero(c, theme):
    H = 320
    b = [frame(W, H, c, 14)]
    b.append(g_in(0.05, text(36, 46, f"{USER.lower()} / README.md", 12, c["subtle"], MONO), 0))
    b.append(g_in(0.05, sun_moon(W - 120, 42, c, theme), 0))
    b.append(f'<line x1="0.5" y1="70" x2="{W - 0.5}" y2="70" stroke="{c["border"]}"/>')
    b.append(g_in(0.2, text(34, 134, NAME, 50, c["text"], weight=700, ls=-1.5)
             + f'<circle cx="{34 + len(NAME) * 50 * 0.535:.1f}" cy="128" r="5" fill="{c["accent"]}"/>', 12))
    b.append(g_in(0.4, text(36, 170, ROLE, 18, c["muted"])))
    t0 = 0.9
    b.append(g_in(0.6, text(36, 214, "$", 14, c["accent"], MONO, 600)))
    s, t1 = typed(54, 214, TYPED, t0, c)
    b.append(s)
    # cursor: an invisible copy of the line sets the exact offset in whatever font renders
    b.append(f'<text x="54" y="214" font-family="{MONO}" font-size="14"><tspan fill-opacity="0">{e(TYPED)} </tspan>'
             f'<tspan fill="{c["accent"]}" opacity="0">█<set attributeName="opacity" to="1" begin="{t1:.2f}s"/>'
             f'<animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.1s" begin="{t1:.2f}s" '
             f'repeatCount="indefinite"/></tspan></text>')
    # meta row
    x, parts = 36, []
    for i, m in enumerate(META):
        if i == 0:
            parts.append(pulse(x + 4, 263, c["green"]))
            x += 16
        parts.append(text(x, 267, m, 12.5, c["muted"], MONO))
        x += len(m) * 12.5 * MONO_W + 16
        if i < len(META) - 1:
            parts.append(f'<circle cx="{x - 8:.1f}" cy="263" r="1.5" fill="{c["subtle"]}"/>')
    b.append(g_in(0.7, "".join(parts)))
    # contribution-style dot grid with a diagonal wave
    cols, rows, step, size = 9, 7, 22, 15
    gx, gy = W - 36 - cols * step + (step - size), 96
    levels = [0.0, 0.25, 0.45, 0.7, 1.0]
    cells = []
    for r in range(rows):
        for col in range(cols):
            lv = levels[(col * 7 + r * 13 + col * r) % 5] if (col * 3 + r * 5) % 4 else 0
            x0, y0 = gx + col * step, gy + r * step
            cells.append(f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" rx="3.5" fill="{c["cell"]}" stroke="{c["border"]}" stroke-opacity="0.6"/>')
            if lv:
                cells.append(f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" rx="3.5" fill="{c["accent"]}" opacity="{lv * 0.85:.2f}"/>')
            cells.append(f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" rx="3.5" fill="{c["accent"]}" opacity="0">'
                         f'<animate attributeName="opacity" values="0;0.9;0;0" keyTimes="0;0.08;0.25;1" dur="5s" '
                         f'begin="{1 + (col + r) * 0.11:.2f}s" repeatCount="indefinite"/></rect>')
    b.append(g_in(0.3, "".join(cells), 0))
    return svg(W, H, "".join(b), f"{NAME} — {ROLE}. Currently {TYPED}.")


def header(c, num, title, path):
    H = 56
    tw = len(title) * 20 * SANS_W
    x_line = 44 + tw + 18
    end = W - 18 - len(path) * 11 * MONO_W - 14
    b = [g_in(0, text(2, 36, num, 12, c["accent"], MONO, 600), 4),
         g_in(0.08, text(36, 37, title, 20, c["text"], weight=600, ls=-0.3), 4),
         f'<line x1="{x_line:.1f}" y1="31" x2="{end:.1f}" y2="31" stroke="{c["border"]}" pathLength="100" '
         f'stroke-dasharray="100" stroke-dashoffset="100"><animate attributeName="stroke-dashoffset" from="100" '
         f'to="0" begin="0.2s" dur="1s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/></line>',
         g_in(0.5, text(W - 4, 35, path, 11, c["subtle"], MONO, anchor="end"), 0)]
    return svg(W, H, "".join(b), f"{num} {title}")


def featured(c, theme):
    H, f = 236, FEATURED
    b = [frame(W, H, c, 14)]
    left = [text(32, 48, "CURRENT BUILD", 11, c["accent"], MONO, 600, ls=1.5),
            pulse(150, 44, c["green"], 3),
            text(32, 92, f["title"], 30, c["text"], weight=700, ls=-0.8)]
    for i, line in enumerate(wrap(f["desc"], 56)):
        left.append(text(32, 124 + i * 22, line, 14.5, c["muted"]))
    left.append(text(32, 194, f["tech"], 12, c["subtle"], MONO))
    left.append(text(32, 216, f["url"].replace("https://", "") + "  ↗", 12, c["accent"], MONO))
    b.append(g_in(0.1, "".join(left)))
    # brief -> model -> report
    cy = 104
    d, m, r = 520, 660, 760
    parts = [f'<rect x="{d}" y="{cy - 40}" width="60" height="80" rx="8" fill="{c["surface"]}" stroke="{c["border"]}"/>']
    for i, w in enumerate([36, 28, 40, 22, 32]):
        parts.append(f'<rect x="{d + 12}" y="{cy - 26 + i * 12}" width="{w}" height="4" rx="2" fill="{c["subtle"]}" opacity="0.5"/>')
    parts.append(f'<circle cx="{m}" cy="{cy}" r="30" fill="{c["surface"]}" stroke="{c["border"]}"/>'
                 f'<circle cx="{m}" cy="{cy}" r="30" stroke="{c["accent"]}" stroke-width="1.5" pathLength="100" '
                 f'stroke-dasharray="20 80" transform="rotate(-90 {m} {cy})"><animate attributeName="stroke-dashoffset" '
                 f'from="0" to="-100" dur="3s" repeatCount="indefinite"/></circle>'
                 + text(m, cy + 5, "AI", 14, c["text"], MONO, 700, "middle"))
    parts.append(f'<rect x="{r}" y="{cy - 40}" width="60" height="80" rx="8" fill="{c["surface"]}" stroke="{c["border"]}"/>')
    for i, w in enumerate([34, 22, 40]):
        yy = cy - 22 + i * 18
        parts.append(f'<rect x="{r + 12}" y="{yy}" width="36" height="6" rx="3" fill="{c["border"]}"/>'
                     f'<rect x="{r + 12}" y="{yy}" width="0" height="6" rx="3" fill="{c["accent"]}">'
                     f'<animate attributeName="width" values="0;{w};{w};0" keyTimes="0;0.25;0.85;1" dur="5s" '
                     f'begin="{1.2 + i * 0.25:.2f}s" repeatCount="indefinite"/></rect>')
    for i, (x1, x2) in enumerate([(d + 64, m - 34), (m + 34, r - 4)]):
        parts.append(f'<line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="{c["border"]}" stroke-dasharray="3 4"/>'
                     f'<circle r="3" fill="{c["accent"]}"><animateMotion path="M{x1} {cy}H{x2}" dur="1.6s" '
                     f'begin="{0.8 + i * 0.8:.1f}s" repeatCount="indefinite"/></circle>')
    for x, lbl in [(d + 30, "brief"), (m, "model"), (r + 30, "report")]:
        parts.append(text(x, cy + 66, lbl, 11, c["subtle"], MONO, anchor="middle"))
    b.append(g_in(0.3, "".join(parts), 0))
    return svg(W, H, "".join(b), f'{f["title"]}: {f["desc"]}')


def project(c, p, i):
    w, H = 410, 176
    b = [frame(w, H, c)]
    inner = [text(24, 36, f"{i + 1:02d}", 11, c["subtle"], MONO, 600)]
    if p["live"]:
        inner.append(pulse(w - 62, 32, c["green"], 3) + text(w - 52, 36, "live", 11, c["green"], MONO))
    else:
        inner.append(text(w - 24, 37, "↗", 15, c["subtle"], anchor="end"))
    inner.append(text(24, 66, p["title"], 17, c["text"], weight=600, ls=-0.2))
    for j, line in enumerate(wrap(p["desc"], 54)[:3]):
        inner.append(text(24, 92 + j * 19, line, 13, c["muted"]))
    inner.append(text(24, H - 20, p["tech"], 11, c["subtle"], MONO))
    b.append(g_in(0.1 + i * 0.08, "".join(inner), 6))
    return svg(w, H, "".join(b), f'{p["title"]}: {p["desc"]}')


def stack(c):
    step = 38
    H = 30 + step * len(STACK)
    b = [frame(W, H, c)]
    for i, (label, items) in enumerate(STACK):
        y = 44 + i * step
        last = i == len(STACK) - 1
        row = (text(28, y, label.lower(), 12, c["accent"] if last else c["subtle"], MONO)
               + text(170, y, items, 14, c["text"] if not last else c["muted"]))
        if i:
            row = f'<line x1="28" y1="{y - 24}" x2="{W - 28}" y2="{y - 24}" stroke="{c["border"]}" stroke-opacity="0.6"/>' + row
        b.append(g_in(0.08 * i, row, 4))
    return svg(W, H, "".join(b), "Stack: " + "; ".join(f"{a}: {s}" for a, s in STACK))


def experience(c):
    step, top = 64, 44
    H = top + step * (len(EXPERIENCE) - 1) + 52
    lx = 168
    b = [frame(W, H, c),
         f'<line x1="{lx}" y1="{top - 4}" x2="{lx}" y2="{top + step * (len(EXPERIENCE) - 1)}" stroke="{c["border"]}" '
         f'stroke-width="1.5" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
         f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="1.2s" begin="0.1s" fill="freeze"/></line>']
    for i, (when, role, where, cur) in enumerate(EXPERIENCE):
        y = top + i * step
        dot = (pulse(lx, y, c["accent"], 5) if cur else
               f'<circle cx="{lx}" cy="{y}" r="5" fill="{c["bg"]}" stroke="{c["subtle"]}" stroke-width="1.5"/>')
        row = (text(lx - 24, y + 4, when, 12, c["accent"] if cur else c["subtle"], MONO, anchor="end")
               + dot + text(lx + 26, y + 5, role, 15, c["text"], weight=600)
               + text(lx + 26, y + 26, where, 13, c["muted"]))
        b.append(g_in(0.2 + i * 0.25, row, 4))
    return svg(W, H, "".join(b), "Experience: " + "; ".join(f"{r}, {w} ({t})" for t, r, w, _ in EXPERIENCE))


def contact(c):
    H = 128
    b = [frame(W, H, c),
         g_in(0.1, text(32, 58, CONTACT_TITLE, 24, c["text"], weight=700, ls=-0.6)
              + text(32, 88, CONTACT_TEXT, 14.5, c["muted"])),
         f'<circle cx="{W - 60}" cy="64" r="22" stroke="{c["border"]}"/>'
         f'<circle cx="{W - 60}" cy="64" r="22" stroke="{c["accent"]}" stroke-width="1.5" pathLength="100" '
         f'stroke-dasharray="25 75"><animate attributeName="stroke-dashoffset" from="0" to="-100" dur="4s" repeatCount="indefinite"/></circle>'
         + text(W - 60, 70, "→", 17, c["accent"], anchor="middle")]
    return svg(W, H, "".join(b), f"{CONTACT_TITLE} {CONTACT_TEXT}")


def footer(c):
    H = 48
    return svg(W, H, g_in(0.2, text(W / 2, 28, MOTTO, 12, c["subtle"], MONO, anchor="middle"), 0), MOTTO)


def button(label, primary):
    """Theme-neutral button: mid-tone fill with white text reads on light and dark."""
    w, h = len(label) * 14 * SANS_W + 58, 40
    fill = "#0969da" if primary else "#57606a"
    return svg(int(w), h,
               f'<rect width="{w:.1f}" height="{h}" rx="20" fill="{fill}"/>'
               + text(22, 25.5, label, 14, "#ffffff", weight=600)
               + text(w - 22, 25.5, "↗", 14, "#ffffff", anchor="end"), label)


# ================================================================ README
SECTIONS = [("01", "Now", "/now"), ("02", "Selected work", "/work"),
            ("03", "Stack", "/stack"), ("04", "Experience", "/experience"),
            ("05", "Activity", "/activity"), ("06", "Contact", "/contact")]


def themed(name, alt, href=PROFILE, width="100%"):
    return (f'<a href="{href}#gh-dark-mode-only"><img src="assets/dark/{name}.svg" width="{width}" alt="{e(alt)}" /></a>'
            f'<a href="{href}#gh-light-mode-only"><img src="assets/light/{name}.svg" width="{width}" alt="{e(alt)}" /></a>')


def themed_remote(dark, light, alt, href=PROFILE, attrs='width="100%"'):
    return (f'<a href="{href}#gh-dark-mode-only"><img src="{dark}" {attrs} alt="{e(alt)}" /></a>'
            f'<a href="{href}#gh-light-mode-only"><img src="{light}" {attrs} alt="{e(alt)}" /></a>')


def readme():
    cards = "https://github-profile-summary-cards.vercel.app/api/cards"
    snake = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
    hdr = {num: themed(f"header-{num}", f"{num} {t}") for num, t, _ in SECTIONS}
    rows = []
    for a, b in zip(PROJECTS[::2], PROJECTS[1::2]):
        rows.append('<p align="center">\n  '
                    + themed(f"project-{a['slug']}", a["title"], a["url"], "49%") + "\n  "
                    + themed(f"project-{b['slug']}", b["title"], b["url"], "49%") + "\n</p>")
    live = next(p for p in PROJECTS if p["live"])
    stats = "\n".join([
        themed_remote(f"{cards}/profile-details?username={USER}&theme=github_dark",
                      f"{cards}/profile-details?username={USER}&theme=github", "GitHub profile summary"),
        themed_remote(f"{cards}/repos-per-language?username={USER}&theme=github_dark",
                      f"{cards}/repos-per-language?username={USER}&theme=github", "Repositories per language", attrs='height="165"'),
        themed_remote(f"{cards}/stats?username={USER}&theme=github_dark",
                      f"{cards}/stats?username={USER}&theme=github", "GitHub statistics", attrs='height="165"'),
        themed_remote(f"{snake}/github-contribution-grid-snake-dark.svg",
                      f"{snake}/github-contribution-grid-snake.svg", "Contribution snake"),
    ])
    buttons = "\n  ".join(f'<a href="{h}"><img src="assets/button-{s}.svg" height="40" alt="{e(l)}" /></a>'
                          for s, l, h, _ in BUTTONS)
    return f"""<!-- Generated by scripts/build_assets.py. Edit the CONTENT section there, then re-run. -->
<!-- Each image has a light and a dark version; GitHub shows the one matching your theme. -->

{themed("hero", f"{NAME} — {ROLE}")}

<br/>

{hdr["01"]}

{themed("featured", f"{FEATURED['title']}: {FEATURED['desc']}", FEATURED["url"])}

<br/>

{hdr["02"]}

{chr(10).join(rows)}

<p align="center"><sub>Try <a href="{live['url']}">{live['title']}</a> live.</sub></p>

{hdr["03"]}

{themed("stack", "Stack: " + "; ".join(f"{a}: {s}" for a, s in STACK))}

<br/>

{hdr["04"]}

{themed("experience", "Experience")}

<br/>

{hdr["05"]}

<div align="center">

{stats}

</div>

<br/>

{hdr["06"]}

{themed("contact", f"{CONTACT_TITLE} {CONTACT_TEXT}")}

<p align="center">
  {buttons}
</p>

{themed("footer", MOTTO)}
"""


# ================================================================ main
def main():
    for theme, c in THEMES.items():
        out = ASSETS / theme
        out.mkdir(parents=True, exist_ok=True)
        files = {"hero": hero(c, theme), "featured": featured(c, theme), "stack": stack(c),
                 "experience": experience(c), "contact": contact(c), "footer": footer(c)}
        for num, title, path in SECTIONS:
            files[f"header-{num}"] = header(c, num, title, path)
        for i, p in enumerate(PROJECTS):
            files[f"project-{p['slug']}"] = project(c, p, i)
        for name, content in files.items():
            (out / f"{name}.svg").write_text(content, encoding="utf-8", newline="\n")
    for slug, label, _, primary in BUTTONS:
        (ASSETS / f"button-{slug}.svg").write_text(button(label, primary), encoding="utf-8", newline="\n")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8", newline="\n")
    print("built", sum(1 for _ in ASSETS.rglob("*.svg")), "svgs + README.md")


if __name__ == "__main__":
    main()
