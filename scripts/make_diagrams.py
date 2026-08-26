#!/usr/bin/env python3
"""Generate the README diagrams as GitHub-safe SVG.

No dependencies. Run from the repo root:  python3 scripts/make_diagrams.py
Output: docs/img/*.svg

GitHub sanitises SVG, so everything here uses inline presentation attributes --
no <style> blocks, no scripts, no external references. Each figure paints its own
light surface so it reads on both the light and dark GitHub themes.

The categorical palette was validated for colour-vision deficiency
(root/leaf/flower/fruit, all-pairs, light surface). Do not swap the hues without
re-running a CVD check -- the obvious "earthy" choice (brown/green/violet/terracotta)
fails: brown and terracotta are indistinguishable to a deuteranope.
"""

import math
import os

OUT = os.path.join("docs", "img")

# --- surface + ink ---------------------------------------------------------
SURF = "#fcfcfb"
CARD = "#f4f2ee"
EDGE = "#e2ded6"
INK = "#0b0b0b"
INK2 = "#52514e"
INK3 = "#87847d"
GRID = "#e6e4df"

# --- categorical: Thun organs (CVD-validated, all pairs) -------------------
ROOT = "#eda100"   # earth
LEAF = "#008300"   # water
FLOWER = "#4a3aa7"  # air
FRUIT = "#e34948"  # fire
OPH = "#6f6c66"    # Ophiuchus -- deliberately neutral: not one of Thun's twelve
OUTZ = "#b8b5ad"   # non-zodiacal strays

FONT = "Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def txt(x, y, s, size=13, fill=INK, weight="normal", anchor="start",
        font=FONT, opacity=None, style=None):
    o = f' opacity="{opacity}"' if opacity else ""
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{o}{st}>{esc(s)}</text>')


def rect(x, y, w, h, fill, rx=0, stroke=None, sw=1, opacity=None, dash=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}"{s}{o}{d}/>')


def line(x1, y1, x2, y2, stroke=GRID, sw=1, dash=None, cap="round", opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}{o}/>')


def circle(cx, cy, r, fill="none", stroke=None, sw=1, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{s}{o}/>'


def path(d, fill="none", stroke=None, sw=1, cap="round", join="round", opacity=None,
         dash=None):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}"{s}{o}{da}/>'


def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>'
            + rect(0, 0, w, h, SURF, rx=10, stroke=EDGE, sw=1))


def save(name, parts):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write("".join(parts) + "</svg>\n")
    print("wrote", os.path.join(OUT, name))


def arc_wedge(cx, cy, r0, r1, a0, a1):
    """Annular wedge path. Angles in degrees, 0 = up (12 o'clock), clockwise."""
    def pt(r, a):
        rad = math.radians(a - 90)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)
    x0o, y0o = pt(r1, a0)
    x1o, y1o = pt(r1, a1)
    x1i, y1i = pt(r0, a1)
    x0i, y0i = pt(r0, a0)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f"M{x0o:.2f},{y0o:.2f} A{r1:.2f},{r1:.2f} 0 {large} 1 {x1o:.2f},{y1o:.2f} "
            f"L{x1i:.2f},{y1i:.2f} A{r0:.2f},{r0:.2f} 0 {large} 0 {x0i:.2f},{y0i:.2f} Z")


def polar(cx, cy, r, a):
    rad = math.radians(a - 90)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


# ===========================================================================
# 1. Thun zodiac wheel -- real IAU arcs, computed from the ephemeris
# ===========================================================================
# Fraction of time the Moon actually spends in each constellation,
# 2026-01-01 to 2036-01-01, 30-minute steps, skyfield + de421,
# IAU/Delporte boundaries. Sums to ~100.
WHEEL = [
    # abbrev, name, pct, organ-colour, days per sidereal month
    ("Ari", "Aries",       6.20, FRUIT,  1.70),
    ("Tau", "Taurus",      9.43, ROOT,   2.58),
    ("Ori", "Orion",       1.17, OUTZ,   0.32),
    ("Gem", "Gemini",      6.84, FLOWER, 1.87),
    ("Cnc", "Cancer",      5.88, LEAF,   1.61),
    ("Leo", "Leo",         8.11, FRUIT,  2.21),
    ("Sex", "Sextans",     1.90, OUTZ,   0.52),
    ("Vir", "Virgo",      12.08, ROOT,   3.30),
    ("Lib", "Libra",       6.37, FLOWER, 1.74),
    ("Sco", "Scorpius",    2.49, LEAF,   0.68),
    ("Oph", "Ophiuchus",   4.64, OPH,    1.27),
    ("Sgr", "Sagittarius", 9.56, FRUIT,  2.61),
    ("Cap", "Capricornus", 5.39, ROOT,   1.47),
    ("Aqr", "Aquarius",    7.38, FLOWER, 2.02),
    ("Psc", "Pisces",     12.02, LEAF,   3.29),
    ("Cet", "Cetus",       0.53, OUTZ,   0.14),
]


def fig_wheel():
    W, H = 940, 724
    p = [head(W, H, "The Moon's real path through the constellations, by Thun day-type")]
    p.append(txt(32, 44, "One sidereal month, as the sky actually is", 19, INK, "bold"))
    p.append(txt(32, 68,
                 "Time the Moon spends in each constellation — real IAU boundaries, not equal 30° divisions.",
                 13, INK2))

    cx, cy, r0, r1 = 300, 380, 96, 196
    total = sum(w[2] for w in WHEEL)
    a = 0.0
    GAP = 0.6
    for ab, name, pct, col, days in WHEEL:
        span = pct / total * 360
        a0, a1 = a + GAP / 2, a + span - GAP / 2
        if a1 > a0:
            p.append(path(arc_wedge(cx, cy, r0, r1, a0, a1), fill=col))
        mid = a + span / 2
        # direct label outside the ring -- secondary encoding, so identity is
        # never carried by colour alone
        if pct >= 3.5:
            lx, ly = polar(cx, cy, r1 + 20, mid)
            anchor = "start" if 0 < mid < 180 else "end"
            if abs(mid) < 6 or abs(mid - 180) < 6:
                anchor = "middle"
            p.append(txt(lx, ly - 2, ab, 13, INK, "bold", anchor))
            p.append(txt(lx, ly + 13, f"{days:.2f} d", 11, INK3, "normal", anchor, font=MONO))
        a += span

    p.append(circle(cx, cy, r0 - 8, fill=CARD))
    p.append(txt(cx, cy - 6, "27.32", 30, INK, "bold", "middle"))
    p.append(txt(cx, cy + 16, "days", 13, INK2, "normal", "middle"))
    p.append(txt(cx, cy + 36, "one sidereal month", 11, INK3, "normal", "middle"))

    # -- extremes, stated as a stat row rather than leader lines into a busy ring
    p.append(rect(72, 626, 456, 40, CARD, rx=8))
    p.append(rect(88, 638, 12, 16, ROOT, rx=3))
    p.append(txt(108, 651, "longest — Virgo, 3.30 d", 12, INK, "bold"))
    p.append(rect(292, 638, 12, 16, LEAF, rx=3))
    p.append(txt(312, 651, "shortest — Scorpius, 0.68 d", 12, INK, "bold"))

    # -- legend / explanation column
    lx = 582
    p.append(rect(lx - 18, 96, 360, 176, CARD, rx=8))
    p.append(txt(lx, 122, "Element → plant organ", 14, INK, "bold"))
    rows = [
        (ROOT, "Root", "earth", "Taurus, Virgo, Capricorn", "7.35 d"),
        (LEAF, "Leaf", "water", "Cancer, Scorpio, Pisces", "6.84 d"),
        (FLOWER, "Flower", "air / light", "Gemini, Libra, Aquarius", "5.63 d"),
        (FRUIT, "Fruit", "fire / warmth", "Aries, Leo, Sagittarius", "6.52 d"),
    ]
    y = 146
    for col, organ, elem, cons, dd in rows:
        p.append(rect(lx, y - 9, 12, 12, col, rx=3))
        p.append(txt(lx + 20, y + 1, organ, 12.5, INK, "bold"))
        p.append(txt(lx + 66, y + 1, elem, 11.5, INK2))
        p.append(txt(lx + 342, y + 1, dd, 11, INK2, "normal", "end", font=MONO))
        p.append(txt(lx + 20, y + 15, cons, 11, INK3))
        y += 31

    p.append(rect(lx - 18, 292, 360, 96, CARD, rx=8))
    p.append(rect(lx, 312, 12, 12, OPH, rx=3))
    p.append(txt(lx + 20, 322, "Ophiuchus — 1.27 d/month", 12.5, INK, "bold"))
    p.append(txt(lx, 342, "On the ecliptic, but not in Thun's 12-fold zodiac.", 11.5, INK2))
    p.append(txt(lx, 358, "The printed calendars extend the Scorpio/water", 11.5, INK2))
    p.append(txt(lx, 374, "region across it. Fold it — but flag it.", 11.5, INK2))

    p.append(rect(lx - 18, 406, 360, 96, CARD, rx=8))
    p.append(rect(lx, 426, 12, 12, OUTZ, rx=3))
    p.append(txt(lx + 20, 436, "Orion, Sextans, Cetus — 0.98 d/month", 12.5, INK, "bold"))
    p.append(txt(lx, 456, "The Moon's orbit is inclined ~5.1°, so it strays", 11.5, INK2))
    p.append(txt(lx, 472, "outside the zodiac entirely. Return None and log —", 11.5, INK2))
    p.append(txt(lx, 488, "never crash, never silently default.", 11.5, INK2))

    p.append(line(lx - 18, 522, lx + 342, 522, EDGE, 1))
    p.append(txt(lx - 18, 546,
                 "Computed: skyfield 1.55, de421.bsp, IAU/Delporte", 11, INK3, font=MONO))
    p.append(txt(lx - 18, 562,
                 "boundaries. 2026-2036, 30-minute steps.", 11, INK3, font=MONO))
    p.append(txt(lx - 18, 586,
                 "Reproduce: scripts/make_diagrams.py", 11, INK3, font=MONO))
    p.append(txt(72, 700,
                 "That 4.8× spread is the point: it is why the day types cannot be equally frequent.",
                 12, INK2, style="italic"))
    save("thun-wheel.svg", p)


# ===========================================================================
# 2. Day-type frequency -- why the statistics need weighting
# ===========================================================================
def fig_frequencies():
    W, H = 900, 340
    p = [head(W, H, "Thun day types are not equally frequent")]
    p.append(txt(32, 44, "Day types are not equally frequent", 19, INK, "bold"))
    p.append(txt(32, 68, "Calendar days in 2027, assigned by which constellation the Moon occupies for most of the day.",
                 13, INK2))

    data = [("Root", 107, ROOT, ""),
            ("Fruit", 97, FRUIT, ""),
            ("Leaf", 94, LEAF, "82 + 12 folded from Ophiuchus"),
            ("Flower", 67, FLOWER, "")]
    x0, y0, bw, gap = 150, 104, 560, 44
    mx = 120
    for i, (name, v, col, note) in enumerate(data):
        y = y0 + i * gap
        p.append(txt(x0 - 14, y + 15, name, 13, INK, "bold", "end"))
        p.append(rect(x0, y, bw * v / mx, 22, col, rx=4))
        p.append(txt(x0 + bw * v / mx + 10, y + 16, f"{v} days", 12.5, INK, "bold"))
        if note:
            p.append(txt(x0 + bw * v / mx + 74, y + 16, note, 11, INK3))

    p.append(line(x0, y0 - 8, x0, y0 + 3 * gap + 30, GRID, 1))

    p.append(rect(32, 292, W - 64, 0.0001, SURF))
    p.append(line(32, 286, W - 32, 286, EDGE, 1))
    p.append(txt(32, 312,
                 "Root days outnumber flower days by 60%. Any test of the calendar must weight for this, or "
                 "\"root days work better\"", 12, INK2))
    p.append(txt(32, 328, "is indistinguishable from \"root days are more numerous\".", 12, INK2))
    save("thun-frequencies.svg", p)


# ===========================================================================
# 3. Sidereal vs tropical -- the two-day error
# ===========================================================================
def fig_sidereal():
    W, H = 900, 330
    p = [head(W, H, "Sidereal constellations versus tropical signs")]
    p.append(txt(32, 44, "Sidereal, not tropical", 19, INK, "bold"))
    p.append(txt(32, 68, "The zodiac signs used by astrology drifted off the constellations they were named for. "
                         "They no longer line up.", 13, INK2))

    x0, w = 60, 780
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo"]
    seg = w / 6
    # tropical band: equal 30-degree signs
    p.append(txt(32, 116, "Tropical signs — equal 30° each", 12, INK2, "bold"))
    for i, s in enumerate(signs):
        p.append(rect(x0 + i * seg + 1, 128, seg - 2, 34, CARD, rx=4, stroke=EDGE))
        p.append(txt(x0 + i * seg + seg / 2, 150, s, 12, INK2, "normal", "middle"))

    # sidereal band: the real constellations sit ~24 degrees EARLIER than the
    # signs named after them, so on this axis they are pushed to the right.
    p.append(txt(32, 200, "Real constellations — unequal widths, ~24° behind", 12, INK, "bold"))
    shift = seg * 24 / 30
    cons = [("Pisces", None, LEAF), ("Aries", 24.7, FRUIT), ("Taurus", 36.7, ROOT),
            ("Gemini", 27.9, FLOWER), ("Cancer", 20.1, LEAF), ("Leo", 35.8, FRUIT),
            ("Virgo", 44.0, ROOT)]
    scale = w / sum(c[1] for c in cons if c[1])
    x = x0
    for s, wd, col in cons:
        ww = shift if wd is None else wd * scale
        draw = min(ww, x0 + w - x)
        if draw <= 0:
            break
        p.append(rect(x + 1, 212, draw - 2, 34, col, rx=4))
        if draw > 62:
            p.append(txt(x + draw / 2, 234, s, 12, "#ffffff", "bold", "middle"))
        x += ww

    # the probe line -- tropical Gemini, sidereal Taurus
    px = x0 + seg * 2.35
    p.append(line(px, 118, px, 262, INK, 1.5, dash="4 3"))
    p.append(circle(px, 118, 4, fill=INK))
    p.append(txt(px + 10, 112, "the Moon is here", 12, INK, "bold"))
    p.append(txt(px + 10, 178, "tropical sign says Gemini → flower day", 11.5, INK3))
    p.append(txt(px + 10, 268, "the actual sky says Taurus → root day", 11.5, INK, "bold"))

    p.append(line(32, 288, W - 32, 288, EDGE, 1))
    p.append(txt(32, 312, "A tropical implementation is wrong by roughly two days, every day. "
                          "This is the most common bug in hobby versions of this calendar.", 12, INK2))
    save("sidereal-vs-tropical.svg", p)


# ===========================================================================
# 4. Two independent lunar cycles
# ===========================================================================
def fig_cycles():
    W, H = 900, 380
    p = [head(W, H, "Ascending/descending is a different cycle from waxing/waning")]
    p.append(txt(32, 44, "Two cycles that are not the same cycle", 19, INK, "bold"))
    p.append(txt(32, 68, "The biodynamic \"ascending / descending\" Moon is a declination cycle. It has nothing to do "
                         "with phase.", 13, INK2))

    x0, w = 250, 620
    days = 60
    def X(d): return x0 + w * d / days

    for cy, per, col, lab, sub in [
        (170, 27.32, FLOWER, "Ascending / descending", "declination — 27.32 d, the tropical month"),
        (280, 29.53, ROOT, "Waxing / waning", "phase — 29.53 d, the synodic month"),
    ]:
        p.append(line(x0, cy, x0 + w, cy, GRID, 1))
        d = f"M{X(0):.1f},{cy:.1f}"
        for i in range(1, 481):
            dd = days * i / 480
            d += f" L{X(dd):.1f},{cy - 34 * math.sin(2 * math.pi * dd / per):.1f}"
        p.append(path(d, stroke=col, sw=2.5))
        p.append(txt(x0 - 22, cy - 4, lab, 12.5, INK, "bold", "end"))
        p.append(txt(x0 - 22, cy + 13, sub, 11, INK3, "normal", "end"))

    # crest markers -- the gap between them is the whole story
    for k, gap in ((0, "0.5 d apart"), (1, "2.8 d apart")):
        d1 = 27.32 * (0.25 + k)
        d2 = 29.53 * (0.25 + k)
        p.append(circle(X(d1), 170 - 34, 4.5, fill=FLOWER, stroke=SURF, sw=2))
        p.append(circle(X(d2), 280 - 34, 4.5, fill=ROOT, stroke=SURF, sw=2))
        p.append(line(X(d1), 136, X(d1), 320, INK3, 1, dash="3 3"))
        p.append(line(X(d2), 246, X(d2), 320, INK3, 1, dash="3 3"))
        mid = (X(d1) + X(d2)) / 2
        p.append(txt(mid, 332, gap, 11, INK, "bold", "middle"))

    p.append(line(x0, 348, x0 + w, 348, EDGE, 1))
    for d in range(0, days + 1, 10):
        p.append(line(X(d), 344, X(d), 352, INK3, 1))
        p.append(txt(X(d), 368, f"day {d}" if d == 0 else str(d), 11, INK3, "normal", "middle"))

    p.append(txt(32, 116, "Confusing these two is the second most common bug in this calendar.",
                 11.5, INK2, style="italic"))
    save("two-lunar-cycles.svg", p)


# ===========================================================================
# 5. Power budget -- why the node is a Pico
# ===========================================================================
def fig_power():
    W, H = 900, 360
    p = [head(W, H, "Daily energy budget: Pi versus Pico")]
    p.append(txt(32, 44, "Why the field node is a Pico W, not a Pi", 19, INK, "bold"))
    p.append(txt(32, 68, "Energy consumed per day, and the December panel needed to replace it in the Dutch winter.",
                 13, INK2))

    data = [
        ("Pi Zero 2 W, always on", 14.4, "~48 W panel · 100 Wh battery", FRUIT),
        ("Pi Zero 2 W, duty-cycled", 2.4, "~8 W panel · 17 Wh battery", ROOT),
        ("Pico W, duty-cycled", 0.16, "~1 W by arithmetic — buy 5–10 W", LEAF),
    ]
    x0, y0, bw, gap = 230, 108, 420, 60
    mx = 15.0
    for i, (name, v, note, col) in enumerate(data):
        y = y0 + i * gap
        p.append(txt(x0 - 14, y + 15, name, 12.5, INK, "bold", "end"))
        ww = max(bw * v / mx, 3)
        p.append(rect(x0, y, ww, 22, col, rx=4))
        p.append(txt(x0 + ww + 10, y + 16, f"{v} Wh/day", 12.5, INK, "bold", font=MONO))
        p.append(txt(x0, y + 38, note, 11, INK3))
    p.append(line(x0, y0 - 8, x0, y0 + 2 * gap + 30, GRID, 1))

    p.append(line(32, 300, W - 32, 300, EDGE, 1))
    p.append(txt(32, 324, "A factor of ~90 between the top and bottom bar. "
                          "Measure your own dormant current before sizing anything — published Pico figures", 12, INK2))
    p.append(txt(32, 342, "disagree by ~30×, which changes the panel by several times but not the conclusion.",
                 12, INK2))
    save("power-budget.svg", p)


# ===========================================================================
# 6. Dutch winter irradiance -- the constraint behind everything
# ===========================================================================
def fig_irradiance():
    W, H = 900, 300
    p = [head(W, H, "De Bilt irradiance, June versus December")]
    p.append(txt(32, 44, "The constraint behind every hardware decision", 19, INK, "bold"))
    p.append(txt(32, 68, "24-hour mean solar irradiance at De Bilt, 1991–2020 normals (KNMI).", 13, INK2))

    for i, (lab, val, col, hh) in enumerate([("June", 200, ROOT, 120), ("December", 20, FLOWER, 12)]):
        x = 90 + i * 220
        p.append(rect(x, 236 - hh, 96, hh, col, rx=4))
        p.append(txt(x + 48, 226 - hh, f"{val}", 26, INK, "bold", "middle"))
        p.append(txt(x + 48, 258, lab, 12.5, INK2, "normal", "middle"))
    p.append(txt(90, 278, "W/m², 24-hour mean", 11, INK3))
    p.append(line(80, 236, 400, 236, EDGE, 1))

    p.append(rect(452, 96, W - 484, 168, CARD, rx=8))
    p.append(txt(474, 126, "A factor of ten — not a factor of two.", 14, INK, "bold"))
    p.append(txt(474, 152, "≈ 4.8 peak-sun-hours in June against ≈ 0.5 in December.", 12, INK2))
    p.append(txt(474, 174, "And that 20 W/m² is a monthly mean. NL routinely delivers", 12, INK2))
    p.append(txt(474, 192, "runs of 5–10 consecutive overcast days at 0.05–0.15 PSH —", 12, INK2))
    p.append(txt(474, 210, "effectively no harvest at all.", 12, INK2))
    p.append(txt(474, 238, "Size the panel for the mean.", 12, INK, "bold"))
    p.append(txt(474, 256, "Size the battery for the dark run.", 12, INK, "bold"))
    save("dutch-irradiance.svg", p)


# ===========================================================================
# 7. Link decision
# ===========================================================================
def fig_link():
    W, H = 900, 360
    p = [head(W, H, "Choosing the field-to-house link by measured distance")]
    p.append(txt(32, 44, "Measure the distance before you choose the radio", 19, INK, "bold"))
    p.append(txt(32, 68, "This is the one architectural choice that is awkward to reverse. Phase 0 decides it.", 13, INK2))

    x0, w, y = 60, 780, 108
    zones = [(0, 20, LEAF, "BLE", "0–20 m, clear line of sight",
              "the simplest thing that works — no extra radios"),
             (20, 50, ROOT, "marginal", "20–50 m, some vegetation",
              "works in July, drops out in a wet November"),
             (50, 120, FRUIT, "LoRa SX1262", "50 m and beyond",
              "20–40 dB of margin you never think about again")]
    for a, b, col, lab, rng, note in zones:
        xa, xb = x0 + w * a / 120, x0 + w * b / 120
        p.append(rect(xa + 1, y, xb - xa - 2, 30, col, rx=4))
        p.append(txt((xa + xb) / 2, y + 20, lab, 12.5, "#ffffff", "bold", "middle"))

    p.append(line(x0, y + 46, x0 + w, y + 46, EDGE, 1))
    for d in (0, 20, 50, 120):
        x = x0 + w * d / 120
        p.append(line(x, y + 42, x, y + 50, INK3, 1))
        p.append(txt(x, y + 68, f"{d} m" + ("+" if d == 120 else ""), 11, INK2, "normal", "middle"))

    ly = 202
    for a, b, col, lab, rng, note in zones:
        p.append(rect(x0, ly - 9, 11, 11, col, rx=3))
        p.append(txt(x0 + 20, ly, rng, 12, INK, "bold"))
        p.append(txt(x0 + 200, ly, note, 12, INK2))
        ly += 24

    p.append(line(32, 292, W - 32, 292, EDGE, 1))
    p.append(txt(32, 316, "BLE's limit here is not throughput — your payload is ~10 bits/second against a "
                          "235 kbps floor. It is that a dropped link", 12, INK2))
    p.append(txt(32, 334, "fails silently, with no retry, during exactly the weather worth observing.", 12, INK2))
    save("link-decision.svg", p)


# ===========================================================================
# 8. Architecture
# ===========================================================================
def fig_arch():
    W, H = 940, 520
    p = [head(W, H, "System architecture")]
    p.append(txt(32, 44, "Sensor to scheduler", 19, INK, "bold"))
    p.append(txt(32, 68, "The store is the seam. Everything upstream writes to it; everything downstream reads from it.",
                 13, INK2))

    # field column
    p.append(rect(32, 96, 300, 386, CARD, rx=10))
    p.append(txt(52, 124, "FIELD", 11.5, INK3, "bold"))
    p.append(txt(52, 146, "Pico 2 W · MicroPython", 14, INK, "bold"))
    items = ["BME280 — air T / RH / pressure",
             "DS18B20 ×2 — soil T, 10 & 30 cm",
             "Capacitive ×2 — soil moisture",
             "BH1750 — lux (not PAR)",
             "Tipping gauge — rain",
             "Anemometer + vane — wind",
             "Battery V / panel V"]
    y = 174
    for it in items:
        p.append(circle(58, y - 4, 2.5, fill=INK3))
        p.append(txt(70, y, it, 11.5, INK2))
        y += 22
    p.append(line(52, 342, 312, 342, EDGE, 1))
    p.append(txt(52, 366, "LiFePO4 26650 → CN3791 MPPT", 11.5, INK2))
    p.append(txt(52, 386, "5–10 W panel @ 65° due south", 11.5, INK2))
    p.append(txt(52, 406, "Ring buffer + ack'd backfill", 11.5, INK, "bold"))
    p.append(txt(52, 426, "IP66 box inside the birdbox", 11.5, INK2))
    p.append(txt(52, 456, "0.08–0.24 Wh/day", 13, LEAF, "bold", font=MONO))

    # link
    p.append(path("M340,250 L392,250", stroke=INK3, sw=2))
    p.append(path("M384,244 L392,250 L384,256", stroke=INK3, sw=2, fill="none"))
    p.append(txt(366, 236, "BLE", 11.5, INK, "bold", "middle"))
    p.append(txt(366, 272, "or LoRa", 10.5, INK3, "normal", "middle"))

    # laptop column
    p.append(rect(400, 96, 508, 386, CARD, rx=10))
    p.append(txt(422, 124, "HOUSE", 11.5, INK3, "bold"))
    p.append(txt(422, 146, "oneacre · Python 3.11+", 14, INK, "bold"))

    boxes = [
        (422, 166, "ingest/", "ble_client · knmi · openmeteo · pvgis", FLOWER),
        (422, 232, "store/", "SQLite — raw stays raw, calibration applies on read", INK3),
        (422, 298, "biodynamic/  ·  solar/", "skyfield day-type  ·  LSTM PV forecast", ROOT),
        (422, 364, "scheduler/", "local LLM proposes → Python constraints dispose", LEAF),
    ]
    for bx, by, t, s, col in boxes:
        p.append(rect(bx, by, 464, 52, SURF, rx=8, stroke=EDGE))
        p.append(rect(bx, by, 4, 52, col, rx=2))
        p.append(txt(bx + 18, by + 22, t, 12.5, INK, "bold", font=MONO))
        p.append(txt(bx + 18, by + 40, s, 11, INK2))
    for by in (218, 284, 350):
        p.append(path(f"M654,{by} L654,{by + 14}", stroke=INK3, sw=1.5))
        p.append(path(f"M648,{by + 8} L654,{by + 14} L660,{by + 8}", stroke=INK3, sw=1.5))

    p.append(txt(422, 440, "→ data/briefs/YYYY-MM-DD.md", 12, INK, "bold", font=MONO))
    p.append(txt(422, 460, "The daily brief. Every number computed in Python; the model selects and explains.",
                 11, INK3))
    save("architecture.svg", p)


# ===========================================================================
# 9. Birdbox build cross-section
# ===========================================================================
def fig_birdbox():
    W, H = 940, 620
    p = [head(W, H, "Field node build - cross-section")]
    p.append(txt(32, 44, "How the node goes together", 19, INK, "bold"))
    p.append(txt(32, 68, "Every detail here exists because leaving it out produces a dead node or "
                         "plausible-looking wrong data.", 13, INK2))

    GROUND = 424
    LW = 512
    p.append(rect(32, 96, LW, GROUND - 96, "#f6f8fa", rx=8))
    p.append(rect(32, GROUND, LW, 154, "#efe9df", rx=8))
    p.append(line(32, GROUND, 32 + LW, GROUND, "#d8cfc0", 2))

    p.append(rect(214, 232, 15, 250, "#b9a68c", rx=3))
    p.append(path("M148,232 L221,186 L294,232 L294,360 L148,360 Z", fill="#e8dcc8",
                  stroke="#cbb89a", sw=2))
    p.append(txt(221, 210, "birdbox shell", 10, "#8a7a5f", "normal", "middle"))

    p.append(rect(166, 256, 110, 86, SURF, rx=6, stroke=INK3, sw=1.5))
    p.append(txt(221, 278, "IP66 box", 11, INK, "bold", "middle"))
    p.append(txt(221, 294, "Pico 2 W", 10, INK2, "normal", "middle"))
    p.append(txt(221, 309, "LiFePO4 + BMS", 10, INK2, "normal", "middle"))
    p.append(txt(221, 329, "conformal coated", 9.5, INK3, "normal", "middle"))

    p.append(circle(190, 342, 4, fill=FLOWER))
    p.append(txt(158, 358, "vent", 9.5, FLOWER, "bold", "end"))
    for gx in (212, 232, 252):
        p.append(circle(gx, 342, 3, fill=INK3))

    p.append(path("M330,172 L410,126 L424,144 L344,190 Z", fill="#3a4a63", stroke="#2b384c", sw=1.5))
    p.append(line(378, 158, 366, 232, "#8a8880", 2))
    p.append(rect(352, 232, 28, 7, "#8a8880", rx=2))
    p.append(txt(378, 116, "panel @ 65°", 10, INK2, "normal", "middle"))

    for i in range(5):
        p.append(path(f"M74,{246 + i * 12} L124,{246 + i * 12} L118,{254 + i * 12} "
                      f"L80,{254 + i * 12} Z", fill="#e9e6df", stroke="#c6c2b8", sw=1))
    p.append(line(124, 284, 166, 294, "#c6c2b8", 1.5))
    p.append(txt(99, 236, "shield + BME280", 10, INK2, "normal", "middle"))

    p.append(rect(466, 192, 7, 232, "#b9a68c", rx=2))
    p.append(path("M446,200 L494,200 L486,232 L454,232 Z", fill="#dfe6ec", stroke="#b9c4ce", sw=1.5))
    for a in (0, 120, 240):
        ex, ey = 470 + 26 * math.cos(math.radians(a)), 168 + 10 * math.sin(math.radians(a))
        p.append(line(470, 168, ex, ey, "#8a8880", 1.5))
        p.append(circle(ex, ey, 4.5, fill="#dfe6ec", stroke="#8a8880", sw=1.2))
    p.append(txt(470, 254, "rain + wind", 10, INK2, "normal", "middle"))

    p.append(line(232, 342, 288, GROUND + 32, INK3, 1.5))
    p.append(line(252, 342, 326, GROUND + 92, INK3, 1.5))
    p.append(circle(288, GROUND + 32, 5, fill=LEAF))
    p.append(circle(326, GROUND + 92, 5, fill=LEAF))
    p.append(line(212, 342, 150, GROUND + 40, INK3, 1.5))
    p.append(rect(144, GROUND + 36, 6, 26, ROOT, rx=2))
    p.append(txt(134, GROUND + 44, "capacitive", 10, INK2, "normal", "end"))
    p.append(txt(134, GROUND + 59, "moisture ×2", 10, INK2, "normal", "end"))
    p.append(txt(300, GROUND + 36, "DS18B20 @ 10 cm", 10, INK2))
    p.append(txt(340, GROUND + 96, "DS18B20 @ 30 cm", 10, INK2))
    p.append(txt(340, GROUND + 111, "the lag between them is real information", 9.5, INK3))

    CX, CW = 570, 338
    calls = [
        (FLOWER, "ePTFE vent + desiccant, underside",
         "A sealed box breathes — warm day out, cold night",
         "in — and pumps itself full of water over weeks."),
        (ROOT, "Radiation shield in ASA or PETG, never PLA",
         "No shield means you are not measuring air",
         "temperature. PLA fails outdoors within 30 days."),
        (FRUIT, "BMS with verified low-temp charge cutoff",
         "Charging LiFePO4 below 0 °C plates lithium.",
         "Irreversible. Freezer-test it before deployment."),
        (LEAF, "Panel at 60–75°, due south",
         "Steeper than the annual optimum: trades summer",
         "surplus for winter, and sheds snow and grime."),
        (INK3, "Drip loops, glands facing down",
         "Water runs down the cable and falls off the loop",
         "instead of tracking into the enclosure."),
    ]
    y = 104
    for col, t, s1, s2 in calls:
        p.append(rect(CX, y, CW, 60, CARD, rx=7))
        p.append(rect(CX, y, 4, 60, col, rx=2))
        p.append(txt(CX + 16, y + 20, t, 11.5, INK, "bold"))
        p.append(txt(CX + 16, y + 36, s1, 10.5, INK2))
        p.append(txt(CX + 16, y + 51, s2, 10.5, INK2))
        y += 68

    p.append(txt(CX, y + 18, "The wooden birdbox is the rain-and-sun shell, not the seal.",
                 11.5, INK, "bold"))
    p.append(txt(CX, y + 36, "Wood is hygroscopic and sits at ambient humidity permanently.", 11, INK2))
    p.append(txt(CX, y + 52, "The air gap between the two boxes buffers thermal swings.", 11, INK2))

    p.append(txt(32, H - 20, "Not to scale. Sensor height: WMO convention is 1.25–2 m for comparability "
                             "with KNMI; lower measures plant microclimate. Record which you chose.",
                 10.5, INK3))
    save("birdbox-build.svg", p)


# ===========================================================================
# 10. Roadmap
# ===========================================================================
def fig_roadmap():
    W, H = 940, 530
    p = [head(W, H, "Phase roadmap")]
    p.append(txt(32, 44, "Roadmap", 19, INK, "bold"))
    p.append(txt(32, 68, "Phases 0–3 are sequential. Phase 5 needs no hardware — start it on the first rainy evening.",
                 13, INK2))

    # legend -- colour groups the kind of work, and follows the phase, not its order
    legend = [(FLOWER, "hardware"), (LEAF, "data, no hardware needed"),
              (ROOT, "models"), (FRUIT, "integration"), (INK3, "setup / later")]
    lx = 32
    for col, lab in legend:
        p.append(rect(lx, 88, 11, 11, col, rx=3))
        p.append(txt(lx + 18, 98, lab, 11, INK2))
        lx += 26 + len(lab) * 6.0

    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    x0, w, ytop = 300, 600, 148
    mw = w / len(months)
    for i, m in enumerate(months):
        p.append(line(x0 + i * mw, ytop, x0 + i * mw, 462, GRID, 1))
        p.append(txt(x0 + i * mw + mw / 2, ytop - 10, m, 10.5, INK3, "normal", "middle"))
    p.append(txt(x0, ytop - 28, "2026", 10.5, INK3, "bold"))
    p.append(txt(x0 + 4 * mw, ytop - 28, "2027", 10.5, INK3, "bold"))

    bars = [
        ("0 · Repo, site survey, ADRs", 0, 0.5, INK3),
        ("1 · Bench node", 0.3, 1.2, FLOWER),
        ("2 · The link", 1.2, 2.2, FLOWER),
        ("3 · Power + deployment", 2.0, 3.2, FLOWER),
        ("4 · Calibration", 3.2, 5.5, FLOWER),
        ("5 · Weather + history", 0.2, 5.0, LEAF),
        ("6 · Biodynamic engine", 1.0, 3.0, LEAF),
        ("7 · Solar LSTM", 4.0, 6.5, ROOT),
        ("8 · LLM scheduler", 6.0, 8.5, FRUIT),
        ("9 · Vision + anomalies", 8.5, 12.5, INK3),
    ]
    y = ytop + 16
    for name, a, b, col in bars:
        p.append(txt(x0 - 18, y + 14, name, 12, INK, "normal", "end"))
        p.append(rect(x0 + a * mw, y, max((b - a) * mw, 8), 20, col, rx=4))
        y += 32

    p.append(line(32, 478, W - 32, 478, EDGE, 1))
    p.append(txt(32, 502, "Deploy before the weather turns — the first Dutch winter is the hard test, and it is the "
                          "whole point of the exercise.", 12, INK2))
    save("roadmap.svg", p)


if __name__ == "__main__":
    fig_wheel()
    fig_frequencies()
    fig_sidereal()
    fig_cycles()
    fig_power()
    fig_irradiance()
    fig_link()
    fig_arch()
    fig_birdbox()
    fig_roadmap()
    print("done")
