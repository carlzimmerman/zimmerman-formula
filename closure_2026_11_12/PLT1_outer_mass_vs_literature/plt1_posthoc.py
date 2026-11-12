#!/usr/bin/env python3
"""PLT1 POST HOC (not in the frozen criteria, written after the graded run): the external-field strength at which
the class median pull of the rows at r >= 150 kpc reaches -2, per class and footing. Reads plt1_results.json.
Uses M_sph = M_b beyond 150 kpc (the ported model gives 0.999 there). Writes plt1_posthoc.out."""
import json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
MB = 6.6814e10 * MSUN
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
MU = np.linspace(-1, 1, 4001)
def nu(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
def line(r, a0, e):
    gb = G * MB / (r * KPC) ** 2 / a0
    if e == 0: return float(nu(gb)) * MB / MSUN / 1e11
    gm = np.sqrt(gb * gb + e * e + 2 * gb * e * MU); y = nu(gm) * (gb + e * MU)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(MU)) / 2) / 2 / gb * MB / MSUN / 1e11
def pull(Ml, r):
    s = math.log10(1.2); side = math.log10(r["M"] / (r["M"] - r["lo"])) if Ml < r["M"] else math.log10((r["M"] + r["hi"]) / r["M"])
    return (math.log10(Ml) - math.log10(r["M"])) / math.hypot(side, s)
D = json.load(open(os.path.join(HERE, "plt1_results.json")))
out = open(os.path.join(HERE, "plt1_posthoc.out"), "w")
def say(s): print(s); out.write(s + "\n")
say("PLT1 POST HOC (not graded; not in the frozen criteria). Rows at r >= 150 kpc only; 20 per cent floor.")
for c in ("H", "S"):
    far = [r for r in D["rows"][c] if r["r"] >= 150.0]
    for f, a0 in A0.items():
        med = lambda e: float(np.median([pull(line(r["r"], a0, e), r) for r in far]))
        lo, hi = 0.0, 0.05
        if med(0.0) < -2: say(f"class {c} {f}: fails low even with no field"); continue
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if med(mid) > -2: lo = mid
            else: hi = mid
        say(f"class {c} {f:9s}: n = {len(far)}; median pull {med(0.0):+.2f} at e_N = 0, {med(0.008):+.2f} at 0.008, {med(0.01273):+.2f} at 0.01273; "
            f"reaches -2 at e_N = {lo:.4f} (plateau {line(2000.0, a0, lo):.2f} e11)")
