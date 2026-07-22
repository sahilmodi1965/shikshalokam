#!/usr/bin/env python3
"""Shikshagraha Partnership Architecture — cover v2.

Motif: the dandelion. Nine seeds leave the head, one per partnership role.
The real wordmark is embedded from Shikshagraha Logo Final.pdf, never re-typed.
"""
import math

D = "/private/tmp/claude-501/-Users-mantraforchange-shikshalokam/c56c3250-6a8d-4ec8-8baf-0684a0052474/scratchpad/"
W, H = 1600, 2263
BG = "#FFFFFF"

PURPLE  = "#572D90"
ORCHID  = "#994499"
MAGENTA = "#ED1D88"
CRIMSON = "#D21E44"
REDORG  = "#EE4432"
ORANGE  = "#F8981C"
WHEEL = [PURPLE, ORCHID, MAGENTA, CRIMSON, REDORG, ORANGE]


def lerp(a, b, t):
    a = tuple(int(a[i:i+2], 16) for i in (1, 3, 5))
    b = tuple(int(b[i:i+2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))


def wheel_at(t):
    """Continuous walk through the brand wheel. t in [0,1]."""
    t = min(max(t, 0.0), 1.0)
    x = t * (len(WHEEL) - 1)
    i = min(int(x), len(WHEEL) - 2)
    return lerp(WHEEL[i], WHEEL[i+1], x - i)


def seed(cx, cy, ang, r0, r1, spread, colour, wdt, op=1.0):
    """One dandelion seed: a narrow V, vertex inward, arms opening outward."""
    def pt(r, a):
        return (cx + r*math.cos(a), cy + r*math.sin(a))
    tip = pt(r0, ang)
    a_, b_ = pt(r1, ang - spread), pt(r1, ang + spread)
    return (f'<polyline points="{a_[0]:.1f},{a_[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} '
            f'{b_[0]:.1f},{b_[1]:.1f}" fill="none" stroke="{colour}" stroke-width="{wdt:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op:.2f}"/>')


o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{BG}"/>']

# ------------------------------------------------------------- the head
CX, CY, R = 1420, 585, 470
GAP_A, GAP_B = math.radians(183), math.radians(250)   # where the nine left from

angles = []
N = 60
for i in range(N):
    a = (i / N) * 2*math.pi
    if GAP_A < a < GAP_B:
        continue
    angles.append(a)
# order the drawn seeds so colour runs continuously from one gap edge to the other
angles.sort(key=lambda a: (a - GAP_B) % (2*math.pi))

for k, a in enumerate(angles):
    t = k / (len(angles) - 1)
    r1 = R * (0.90 + 0.10*math.sin(k*2.1))
    o.append(seed(CX, CY, a, R*0.045, r1, 0.050, wheel_at(t), 11))
    if k % 2 == 0:                       # inner layer, for density
        o.append(seed(CX, CY, a + 0.052, R*0.045, R*0.55, 0.050, wheel_at(t), 7, 0.5))


# --------------------------------------------- nine seeds, one per role
# They leave the gap and carry the movement across the page.
drift = [(1105, 300), (947, 232), (800, 300), (663, 224),
         (533, 300), (413, 230), (305, 312), (208, 244), (122, 330)]
for i, (x, y) in enumerate(drift):
    sc = 1.0 - i*0.055
    ang = math.radians(196 + (8 if i % 2 else -8))
    o.append(seed(x, y, ang, 16*sc, 104*sc, 0.070,
                  wheel_at(0.06 + i*0.052), 11*sc, 0.95 - i*0.05))

# ------------------------------------------------------------------ type
F = "Poppins, Quicksand, Helvetica, Arial, sans-serif"

# the real wordmark, embedded. 677x101 native.
b64 = open(D + "sg_wordmark.b64").read()
ww = 560
o.append(f'<image x="150" y="1330" width="{ww}" height="{ww*101/677:.0f}" '
         f'xlink:href="data:image/png;base64,{b64}" '
         f'xmlns:xlink="http://www.w3.org/1999/xlink"/>')

o.append(f'<text x="150" y="1600" font-family="{F}" font-size="104" font-weight="500" '
         f'fill="{CRIMSON}">Partnership Architecture</text>')

for k, col in enumerate([PURPLE, ORCHID, MAGENTA, CRIMSON, REDORG, ORANGE]):
    o.append(f'<rect x="{150 + k*58}" y="1668" width="52" height="7" fill="{col}"/>')

o.append(f'<text x="150" y="1836" font-family="{F}" font-size="44" fill="#4A4358">'
         f'The roles through which people and institutions</text>')
o.append(f'<text x="150" y="1898" font-family="{F}" font-size="44" fill="#4A4358">'
         f'join the movement</text>')

roles = ["Co-Builders", "Strategic Partners", "Anchor Partners", "Collaborators",
         "Momentum Partners", "Founding Partners", "Ambassadors", "Advisors", "Mentors"]
o.append(f'<text x="150" y="2062" font-family="{F}" font-size="29" fill="{PURPLE}" '
         f'opacity="0.70">{"  ·  ".join(roles[:5])}</text>')
o.append(f'<text x="150" y="2108" font-family="{F}" font-size="29" fill="{PURPLE}" '
         f'opacity="0.70">{"  ·  ".join(roles[5:])}</text>')
o.append(f'<text x="150" y="2196" font-family="{F}" font-size="31" fill="{PURPLE}" '
         f'opacity="0.5">ShikshaLokam  ·  2026</text>')

o.append('</svg>')
open(D + "cover_sg2.svg", "w").write("\n".join(o))
print("wrote cover_sg2.svg")
