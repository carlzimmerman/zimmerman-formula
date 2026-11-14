#!/usr/bin/env python3
"""XJ1 build A: identity check of one stage-e part against FWN1's committed parts (closure_2026_11_13/
FWN1_forest_flux_split_f_ceiling/parts), run on the test part before the stage is left unattended (FWN1 section 10's rule).
Checks: (i) base-box R (primary and M1_lin) equals FWN1's pass-1 ("inf") part's base R, P1D to 1e-12 rel and P3D to 1e-6;
same forced-box list; (j1, seeds 0 and 1) B|S5.00 equals FWN1's pass-2 ("fin") B|S5.00 in the base box and every forced box;
(d) every field's mean flux within 1e-4 of the target. Prints only identity and mean-flux numbers (no case statistic).
Usage: python3 -I -B xj1a_check_part.py <z> <seed> <footing>
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FWN1 = os.path.join(REPO, "closure_2026_11_13", "FWN1_forest_flux_split_f_ceiling", "parts")
z, s, ft = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
d = json.load(open(os.path.join(HERE, "parts_a", f"e_z{z:.1f}_s{s}_{ft}.json")))
inf = json.load(open(os.path.join(FWN1, f"inf_z{z:.1f}_s{s}_{ft}.json")))
def maxrel(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); z0 = b == 0
    if np.any(a[z0] != 0): return float("inf")
    return float(np.max(np.abs(a[~z0] / b[~z0] - 1))) if np.any(~z0) else 0.0
ok = True
for sp in ("primary", "M1_lin"):
    A, B = d["base"]["flux"][sp]["R"], inf["base"]["flux"][sp]["R"]
    p = maxrel(A["p"], B["p"]); q = maxrel(A["P3D"], B["P3D"]) if "P3D" in A and "P3D" in B else 0.0
    good = p <= 1e-12 and q <= 1e-6; ok &= good
    print(f"(i) base R {sp}: P1D max rel {p:.2e}, P3D max rel {q:.2e} -> {'PASS' if good else 'FAIL'}")
print(f"(i) forced boxes equal FWN1's: {d['boxes'] == inf['boxes']} ({len(d['boxes'])} boxes)"); ok &= d["boxes"] == inf["boxes"]
if s in (0, 1):
    fin = json.load(open(os.path.join(FWN1, f"fin_z{z:.1f}_s{s}_{ft}.json")))
    mp = mq = 0.0; n = 0
    for bx, A in [("base", d["base"])] + [(str(b), d["forced_boxes"][str(b)]) for b in d["boxes"]]:
        B = fin["base"] if bx == "base" else fin["forced_boxes"][bx]
        a, b = A["flux"]["primary"]["B|S5.00"], B["flux"]["primary"]["B|S5.00"]
        mp = max(mp, maxrel(a["p"], b["p"])); mq = max(mq, maxrel(a["P3D"], b["P3D"])); n += 1
    good = mp <= 1e-12 and mq <= 1e-6; ok &= good
    print(f"(j1) control S5.00 vs FWN1 pass 2 over {n} boxes: P1D max rel {mp:.2e}, P3D max rel {mq:.2e} -> {'PASS' if good else 'FAIL'}")
tau = 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132; dm = 0.0; nf = 0
for A in [d["base"]] + list(d["forced_boxes"].values()):
    for sp, F in A["flux"].items():
        for nm, v in F.items(): dm = max(dm, abs(v["meanF"] - math.exp(-tau))); nf += 1
print(f"(d) mean flux over {nf} fields: max |<F> - target| {dm:.2e} -> {'PASS' if dm <= 1e-4 else 'FAIL'}"); ok &= dm <= 1e-4
print(f"fields in base primary: {sorted(d['base']['flux']['primary'])}; forced box fields: {sorted(next(iter(d['forced_boxes'].values()))['flux']['primary'])}")
print(f"part time {d['time_s']:.0f} s in boxes; ALL {'PASS' if ok else 'FAIL'}")
