#!/usr/bin/env python3
"""Generates the README preview images.

These are illustrative mockups drawn from the visual identity described in
context/format-production.md and the numbers in context/success-metrics.md.
They are not captures of a published account -- nothing has shipped yet.

Usage:  python3 docs/make_screens.py     (run from the repo root)
Output: docs/screens/*.svg
"""

import os

BG      = "#0D1117"
PANEL   = "#161B22"
LINE    = "#30363D"
TEXT    = "#E6EDF3"
MUTED   = "#8B949E"
ACCENT  = "#F0A202"   # hook / emphasis
ACCENT2 = "#2F81F7"   # structure / diagram
GOOD    = "#3FB950"

FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote", os.path.relpath(path))


def phone(x, y, w, h, hooks, sub, diagram):
    """A 9:16 reel frame: hook lines, a small diagram, and a caption bar."""
    cx = x + w / 2
    lines = "".join(
        f'<text x="{cx}" y="{y + 40 + i*26}" font-family="{FONT}" font-size="18" '
        f'font-weight="700" fill="{ACCENT}" text-anchor="middle">{t}</text>'
        for i, t in enumerate(hooks))
    sy = y + 40 + len(hooks) * 26
    return f"""
  <g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
    {lines}
    <text x="{cx}" y="{sy}" font-family="{MONO}" font-size="11" fill="{MUTED}" text-anchor="middle">{sub}</text>
    {diagram}
    <rect x="{x + 14}" y="{y + h - 42}" width="{w - 28}" height="26" rx="6" fill="#0B0F14"/>
    <text x="{cx}" y="{y + h - 24}" font-family="{MONO}" font-size="10.5"
          fill="{MUTED}" text-anchor="middle">save this &#183; send to a friend</text>
  </g>"""


def row3(x, ry, labels, note="", note_color=None):
    """Three-stage diagram inside a phone frame at origin x, centred on ry."""
    a, b, c = labels
    s = ""
    s += box(x + 14, ry - 13, 58, 26, a, ACCENT2, 10)
    s += box(x + 96, ry - 13, 58, 26, b, ACCENT, 10)
    if c == "fan":
        for dy in (-34, 0, 34):
            s += box(x + 178, ry - 12 + dy, 52, 24, "srv", ACCENT2, 10)
            s += arrow(x + 156, ry, x + 176, ry + dy)
    else:
        s += box(x + 178, ry - 13, 58, 26, c, ACCENT2, 10)
        s += arrow(x + 156, ry, x + 176, ry)
    s += arrow(x + 74, ry, x + 94, ry)
    if note:
        s += (f'<text x="{x + 125}" y="{ry + 56}" font-family="{MONO}" font-size="10" '
              f'fill="{note_color or MUTED}" text-anchor="middle">{note}</text>')
    return s


def box(x, y, w, h, label, color=ACCENT2, size=11):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{color}" stroke-width="1.6"/>'
            f'<text x="{x + w/2}" y="{y + h/2 + 4}" font-family="{MONO}" font-size="{size}" '
            f'fill="{TEXT}" text-anchor="middle">{label}</text>')


def arrow(x1, y1, x2, y2, color=MUTED):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="1.4" marker-end="url(#a)"/>')


DEFS = f"""
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/>
    </marker>
  </defs>"""


# ---------------------------------------------------------------- hero banner
def hero():
    fy, fh, fw = 152, 248, 250
    xs = [56, 330, 604]
    frames = (
        phone(xs[0], fy, fw, fh, ["Why Netflix", "never crashes"], "load balancing",
              row3(xs[0], fy + 132, ("you", "host", "fan"))) +
        phone(xs[1], fy, fw, fh, ["Your app", "remembers"], "caching",
              row3(xs[1], fy + 132, ("app", "cache", "db"), "hit: 0.4ms", GOOD)) +
        phone(xs[2], fy, fw, fh, ["The order", "never gets lost"], "message queues",
              row3(xs[2], fy + 132, ("order", "queue", "worker"), "retry safe"))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 470" width="1200" height="470" role="img" aria-label="System design explained like you're 5">
  <rect width="1200" height="470" fill="{BG}"/>{DEFS}
  <text x="56" y="70" font-family="{FONT}" font-size="34" font-weight="800" fill="{TEXT}">System design, explained like you&#8217;re 5.</text>
  <text x="56" y="104" font-family="{FONT}" font-size="16" fill="{MUTED}">Four reels a week. Nine months. 50,000 followers, or an honest post-mortem.</text>
  <line x1="56" y1="128" x2="1144" y2="128" stroke="{LINE}"/>
  {frames}
  <g>
    <text x="898" y="196" font-family="{FONT}" font-size="15" font-weight="700" fill="{TEXT}">The gap this fills</text>
    <text x="898" y="226" font-family="{FONT}" font-size="14" fill="{MUTED}">ByteByteGo owns rigorous.</text>
    <text x="898" y="250" font-family="{FONT}" font-size="14" fill="{MUTED}">Meme accounts own funny.</text>
    <text x="898" y="274" font-family="{FONT}" font-size="14" fill="{ACCENT}">Nobody owns simple and correct.</text>
    <text x="898" y="320" font-family="{FONT}" font-size="15" font-weight="700" fill="{TEXT}">The constraints</text>
    <text x="898" y="348" font-family="{MONO}" font-size="12" fill="{MUTED}">faceless &#183; AI voiceover</text>
    <text x="898" y="370" font-family="{MONO}" font-size="12" fill="{MUTED}">$0 budget &#183; ~6 hrs/week</text>
    <text x="898" y="392" font-family="{MONO}" font-size="12" fill="{MUTED}">starting from zero</text>
  </g>
  <text x="56" y="440" font-family="{MONO}" font-size="11" fill="{LINE}">illustrative mockup &#8212; generated by docs/make_screens.py, not a screenshot of a live account</text>
</svg>
"""


# ------------------------------------------------------------ reel anatomy
def reel_template():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1000" height="560" role="img" aria-label="Anatomy of one reel">
  <rect width="1000" height="560" fill="{BG}"/>{DEFS}
  <text x="48" y="56" font-family="{FONT}" font-size="24" font-weight="800" fill="{TEXT}">Anatomy of one reel</text>
  <text x="48" y="82" font-family="{FONT}" font-size="14" fill="{MUTED}">Every reel uses the same frame so the account is recognisable mid-scroll.</text>

  <rect x="48" y="112" width="270" height="400" rx="16" fill="{PANEL}" stroke="{LINE}"/>
  <text x="183" y="168" font-family="{FONT}" font-size="22" font-weight="800" fill="{ACCENT}" text-anchor="middle">Why Netflix</text>
  <text x="183" y="196" font-family="{FONT}" font-size="22" font-weight="800" fill="{ACCENT}" text-anchor="middle">never crashes</text>
  {box(70, 250, 60, 28, "you")}
  {box(160, 250, 66, 28, "host", ACCENT)}
  {box(252, 218, 52, 24, "srv")}
  {box(252, 252, 52, 24, "srv")}
  {box(252, 286, 52, 24, "srv")}
  {arrow(132, 264, 158, 264)}
  {arrow(228, 264, 250, 231)}
  {arrow(228, 264, 250, 265)}
  {arrow(228, 264, 250, 297)}
  <text x="183" y="352" font-family="{FONT}" font-size="13" fill="{TEXT}" text-anchor="middle">A restaurant host seating</text>
  <text x="183" y="372" font-family="{FONT}" font-size="13" fill="{TEXT}" text-anchor="middle">guests at empty tables.</text>
  <rect x="66" y="462" width="234" height="30" rx="7" fill="#0B0F14"/>
  <text x="183" y="482" font-family="{MONO}" font-size="12" fill="{MUTED}" text-anchor="middle">send this to your prep buddy</text>

  <g font-family="{FONT}">
    <line x1="330" y1="150" x2="392" y2="150" stroke="{ACCENT}" stroke-width="1.4"/>
    <text x="404" y="146" font-size="15" font-weight="700" fill="{TEXT}">Hook &#8212; 8 words, frame one</text>
    <text x="404" y="168" font-size="13" fill="{MUTED}">Half of viewers leave in three seconds. No intro, ever.</text>

    <line x1="330" y1="264" x2="392" y2="264" stroke="{ACCENT2}" stroke-width="1.4"/>
    <text x="404" y="260" font-size="15" font-weight="700" fill="{TEXT}">Diagram builds piece by piece</text>
    <text x="404" y="282" font-size="13" fill="{MUTED}">Something new appears every 1&#8211;2 seconds so nothing sits still.</text>

    <line x1="330" y1="362" x2="392" y2="362" stroke="{GOOD}" stroke-width="1.4"/>
    <text x="404" y="358" font-size="15" font-weight="700" fill="{TEXT}">One everyday analogy</text>
    <text x="404" y="380" font-size="13" fill="{MUTED}">Then one line on why an interviewer cares. One idea per reel.</text>

    <line x1="330" y1="477" x2="392" y2="477" stroke="{MUTED}" stroke-width="1.4"/>
    <text x="404" y="473" font-size="15" font-weight="700" fill="{TEXT}">Sends, not likes</text>
    <text x="404" y="495" font-size="13" fill="{MUTED}">Instagram weights a DM share far above a like. Ask for the share.</text>
  </g>
  <text x="48" y="540" font-family="{MONO}" font-size="11" fill="{LINE}">illustrative mockup &#8212; generated by docs/make_screens.py</text>
</svg>
"""


# ------------------------------------------------------------- growth curve
def growth():
    pts = [(1, 650), (3, 3000), (5, 9000), (7, 20000), (9, 50000)]
    x0, y0, w, h = 90, 90, 700, 330

    def px(m):
        return x0 + (m - 1) / 8 * w

    def py(v):
        import math
        lo, hi = math.log10(300), math.log10(60000)
        return y0 + h - (math.log10(v) - lo) / (hi - lo) * h

    poly = " ".join(f"{px(m):.1f},{py(v):.1f}" for m, v in pts)
    dots = "".join(
        f'<circle cx="{px(m):.1f}" cy="{py(v):.1f}" r="5" fill="{ACCENT}"/>'
        f'<text x="{px(m):.1f}" y="{py(v)-16:.1f}" font-family="{MONO}" font-size="12" '
        f'fill="{TEXT}" text-anchor="middle">{v:,}</text>' for m, v in pts)
    xlab = "".join(
        f'<text x="{px(m):.1f}" y="{y0+h+26}" font-family="{MONO}" font-size="12" '
        f'fill="{MUTED}" text-anchor="middle">month {m}</text>' for m, _ in pts)
    grid = "".join(
        f'<line x1="{x0}" y1="{py(v):.1f}" x2="{x0+w}" y2="{py(v):.1f}" stroke="{LINE}" stroke-dasharray="3 5"/>'
        for v in (1000, 10000, 50000))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 520" width="880" height="520" role="img" aria-label="Follower milestone curve">
  <rect width="880" height="520" fill="{BG}"/>
  <text x="48" y="52" font-family="{FONT}" font-size="24" font-weight="800" fill="{TEXT}">What on-track looks like</text>
  <text x="48" y="76" font-family="{FONT}" font-size="14" fill="{MUTED}">Log scale. Growth is back-loaded &#8212; month 3 feels like failure and isn&#8217;t.</text>
  {grid}
  <polyline points="{poly}" fill="none" stroke="{ACCENT}" stroke-width="2.5"/>
  {dots}{xlab}
  <line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="{LINE}"/>
  <text x="{x0}" y="{y0+h+58}" font-family="{FONT}" font-size="13" fill="{MUTED}">Below the month&#8209;3 mark for two weeks running, the format changes. The niche doesn&#8217;t.</text>
  <text x="48" y="500" font-family="{MONO}" font-size="11" fill="{LINE}">targets from context/success-metrics.md &#8212; generated by docs/make_screens.py</text>
</svg>
"""


# ------------------------------------------------------------------ pillars
def pillars():
    rows = [
        ("How X actually works", 50, ACCENT,
         "Netflix, Uber, WhatsApp. The reach engine &#8212; everyone already uses these."),
        ("Core concepts by analogy", 35, ACCENT2,
         "Caching, sharding, queues. One building block, one everyday analogy."),
        ("Interview tactics", 15, GOOD,
         "Frameworks, estimation, what actually gets graded. The reason to follow."),
    ]
    x0, w = 48, 784
    bar, body, cx = "", "", x0
    for name, pct, color, desc in rows:
        seg = w * pct / 100
        bar += (f'<rect x="{cx}" y="104" width="{seg-4}" height="34" rx="6" fill="{color}" opacity="0.85"/>'
                f'<text x="{cx + seg/2 - 2}" y="127" font-family="{MONO}" font-size="13" '
                f'fill="{BG}" font-weight="700" text-anchor="middle">{pct}%</text>')
        cx += seg
    y = 190
    for name, pct, color, desc in rows:
        body += (f'<rect x="{x0}" y="{y-18}" width="4" height="46" rx="2" fill="{color}"/>'
                 f'<text x="{x0+18}" y="{y}" font-family="{FONT}" font-size="16" font-weight="700" fill="{TEXT}">{name}</text>'
                 f'<text x="{x0+18}" y="{y+22}" font-family="{FONT}" font-size="13" fill="{MUTED}">{desc}</text>')
        y += 76
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 460" width="880" height="460" role="img" aria-label="Three content pillars">
  <rect width="880" height="460" fill="{BG}"/>
  <text x="48" y="52" font-family="{FONT}" font-size="24" font-weight="800" fill="{TEXT}">Three pillars, ~40 topics</text>
  <text x="48" y="78" font-family="{FONT}" font-size="14" fill="{MUTED}">Instagram needs consistent categories to know who to show the account to.</text>
  {bar}{body}
  <text x="48" y="436" font-family="{MONO}" font-size="11" fill="{LINE}">from context/content-pillars.md &#8212; generated by docs/make_screens.py</text>
</svg>
"""


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("hero.svg", hero())
    write("reel-anatomy.svg", reel_template())
    write("growth-curve.svg", growth())
    write("content-pillars.svg", pillars())
