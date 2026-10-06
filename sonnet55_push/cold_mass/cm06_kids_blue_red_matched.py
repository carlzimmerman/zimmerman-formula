"""cm06: the blue-spiral test at matched stellar mass, from CFG261's committed mass-matched rows (KiDS-1000 isolated lenses, 10.3 <= log M* < 10.9).
s* = implied a0 / 0.936e-10 from the 1-halo lensing amplitude under the law with visible baryons (s* = 1: the law alone; s* > 1: extra mass).
Combined over the two redshift thirds by inverse variance in log s* (jackknife SDs as committed). Hot-halo hypothesis: blue (late) ~ 1, red (early) > 1.
Run: python3 cm06_kids_blue_red_matched.py | MUTATE=1 swaps the class labels (the red-minus-blue difference must flip sign, check D fails)
"""
import os, re, sys, math
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "campaign_fresh_gravity", "CFG261_kids_absolute_a0_zthirds", "cfg261_stageB.out")).read()
rows = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in re.finditer(r"(MM-(?:late|early)-(?:LO|HI))\s+N\s+\d+ z [0-9.]+:\s+s\* = ([0-9.]+) .*?jackknife ([0-9.]+) dex", out)}
for k, v in rows.items(): print(f"   {k:12s} s* = {v[0]:.3f}  (log {math.log10(v[0]):+.3f} +- {v[1]:.3f})")
def comb(cls):
    w = [(1 / rows[f"MM-{cls}-{t}"][1]**2, math.log10(rows[f"MM-{cls}-{t}"][0])) for t in ("LO", "HI")]
    W = sum(a for a, _ in w); return sum(a * b for a, b in w) / W, 1 / math.sqrt(W)
blue, red = comb("late"), comb("early")
if MUTATE: blue, red = red, blue
print(f"   blue/late  (matched mass): log s* = {blue[0]:+.3f} +- {blue[1]:.3f}  -> s* = {10**blue[0]:.2f}, {blue[0]/blue[1]:+.1f} sigma from the law alone")
print(f"   red/early  (matched mass): log s* = {red[0]:+.3f} +- {red[1]:.3f}  -> s* = {10**red[0]:.2f}, {red[0]/red[1]:+.1f} sigma from the law alone")
d = red[0] - blue[0]; e = math.hypot(red[1], blue[1])
print(f"   red - blue at matched mass: {d:+.3f} +- {e:.3f} dex ({d/e:+.1f} sigma)")
print("   caveat: LO and HI thirds of the blue class disagree (CFG261 d = -0.73 +- 0.41 dex); stellar masses are SED-based (LePhare) for both classes")
check("D red lenses carry more extra mass than blue at matched stellar mass (difference > 0) -- MUTATE swaps labels and must fail", d > 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
