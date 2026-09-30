#!/usr/bin/env python3
"""CFG213 POST HOC (a reconciliation asked for by the orchestrator, 2026-09-30, after the data chat's z > 3.5 list HIGHZ_INDEPENDENT_BARYON_DISCS_2026-09-30.md counted SIX CRISTAL
discs with an SED M* and a dust-DETECTED gas mass where this lane's README says 'the 9 disks that have both'; written after the frozen numbers were seen; reported only).
Which nine, and what they are: the lane's SED + gas route needs a finite SED M*, a finite f_molgas and a finite fitted M_bary.  Among the CRISTAL disks of the primary set (CRISTAL-09 and
-15 are excluded as frozen) that is 02, 03, 07a, 08, 11, 12, 19, 20 and 23b.  The CRISTAL paper (arXiv:2507.11600, its f_molgas note in the gas-fraction section) says that for CRISTAL-01a,
08, 12, 14, 15, 16, 23b and 23c the measured f_molgas are UPPER LIMITS (the dust continuum is below the S/N threshold).  So six of the nine (02, 03, 07a, 11, 19, 20) are dust
detections and THREE (08, 12, 23b) are upper limits that the lane's route used as values, M_ind = M*/(1 - f_molgas).  This script (i) reproduces the lane's committed n = 9 route
medians (control), (ii) recomputes the route on the six detections alone (and the fit route on the same six), (iii) reports the three upper-limit discs as ONE-SIDED bounds: an upper
limit on f_molgas is an upper limit on M_ind and on g_bar; in this lane D = g_obs / g_bar also depends on g_bar, so delta = log10(D) - log10 nu(g_bar / a0) FALLS as g_bar rises
(d delta / d ln g_bar = -1 - d ln nu / d ln y < 0 because y nu(y) rises), and each delta below is therefore a LOWER bound on that disc's true delta under either law.
Reuses the lane's functions (cfg213_two_sided.py exec'd read-only up to its BINS definition).  MUTATE=1 passes through (D x 1.5): the n = 9 route medians must then shift by
log10(1.5) = +0.1761 against the committed values; outputs are named *_MUTATE.
Run: python3 campaign_fresh_gravity/CFG213_dysmalpy_two_sided/cfg213_route_detected.py
"""
import os, sys, io, json, math, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg213_two_sided.py")
src = open(path).read()
MUT = os.environ.get("MUTATE", "").strip() == "1"
ns = {"__file__": path, "__name__": "cfg213"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("BINS = {")], "cfg213", "exec"), ns)
cr, EXCL, galaxy_rows, deltas, verdict, KER, A0F, E, nu1, K = (ns[k] for k in ("cr", "EXCL", "galaxy_rows", "deltas", "verdict", "KER", "A0F", "E", "nu1", "K"))
out = []


def P(s=""):
    print(s); out.append(s)


P(__doc__.split("Run:")[0].strip())
allok = True
prim = [g for g in cr if g["id"] not in EXCL]
DET = ("02", "03", "07a", "11", "19", "20")
UL = ("08", "12", "23b")
byid = {g["id"]: g for g in prim}
S9 = [g for g in prim if g["id"] in DET + UL]
S6 = [byid[i] for i in DET]
S3 = [byid[i] for i in UL]
rows9 = galaxy_rows("Z5", prim, alpha=3.36, route=True, mutate=MUT)
assert sorted(r["id"] for r in rows9) == sorted(DET + UL), f"the route sample is not the expected nine: {sorted(r['id'] for r in rows9)}"
P(f"\n  the lane's route sample (finite SED M*, f_molgas and fitted M_bary, primary set): {sorted(r['id'] for r in rows9)} (n = {len(rows9)})")
P(f"  dust DETECTIONS ({len(DET)}): {', '.join(DET)};  dust UPPER LIMITS used as values ({len(UL)}): {', '.join(UL)}  (f_molgas table values: "
  + ", ".join(f"{i} {byid[i]['f_molgas']:.2f}" for i in UL) + ")")
rng = np.random.default_rng(2130)
NB = 10000


def med_ci(d):
    B = rng.integers(0, len(d), size=(NB, len(d)))
    bs = np.median(d[B], axis=1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return float(np.median(d)), float(lo), float(hi)


committed = json.load(open(os.path.join(LANE, "cfg213_two_sided_results.json")))["numbers"]["Z5 (CRISTAL primary)"]
# (i) control: the n = 9 route medians against the committed values
dmax = 0.0
shifts = []
for kname, nu in KER.items():
    for foot in A0F:
        for law in ("flat", "rival"):
            m = float(np.median(deltas(rows9, law, foot, nu)))
            c = committed[f"3.36|route|{kname}|{foot}|{law}"]["med"]
            dmax = max(dmax, abs(m - c)); shifts.append(m - c)
if not MUT:
    ok = dmax < 1e-9
    P(f"\n  {'PASS' if ok else 'FAIL'}  control: the n = 9 route medians (2 kernels x 2 footings x 2 laws) equal the committed values: max |difference| {dmax:.1e}")
else:
    ok = all(abs(s - math.log10(1.5)) < 1e-9 for s in shifts)
    P(f"\n  {'PASS' if ok else 'FAIL'}  MUTATE: every n = 9 route median shifts by log10(1.5) = {math.log10(1.5):+.4f} (measured {min(shifts):+.4f} to {max(shifts):+.4f})")
allok &= ok
# (ii) the route on the six detections, and the fit route on the same six
def cell_table(label, gals, route):
    rows = galaxy_rows("Z5", gals, alpha=3.36, route=route, mutate=MUT)
    P(f"\n  {label} (n = {len(rows)}); median delta [95% CI, 10,000 resamples] -> verdict; alpha = 3.36")
    res = {}
    for law in ("flat", "rival"):
        for kname, nu in KER.items():
            for foot in A0F:
                m, lo, hi = med_ci(deltas(rows, law, foot, nu))
                res[(law, kname, foot)] = (m, lo, hi, verdict(lo, hi))
                P(f"    {law:5s} {kname:7s} {foot:9s} {m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi)}")
    return res


r9 = cell_table("SED + gas route, the lane's nine (3 of them dust upper limits used as values)", S9, True)
r6 = cell_table("SED + gas route, the six dust DETECTIONS only", S6, True)
r6f = cell_table("fit route (the authors' M_bary), the same six", S6, False)
# (iii) the three upper-limit discs as one-sided bounds
P("\n  the three upper-limit discs, per disc (nu_mono, canonical, alpha = 3.36): delta_route is a LOWER bound on that disc's delta under the law shown")
rows3 = {r["id"]: r for r in galaxy_rows("Z5", S3, alpha=3.36, route=True, mutate=MUT)}
rows3f = {r["id"]: r for r in galaxy_rows("Z5", S3, alpha=3.36, route=False, mutate=MUT)}
n_pos = {"flat": 0, "rival": 0}
for i in UL:
    r, rf = rows3[i], rows3f[i]
    a0 = A0F["canonical"]
    bound = {law: math.log10(r["D"] / nu1(K.nu_mono, r["gbar"] / (a0 * (E(r["z"]) if law == "rival" else 1.0)))) for law in ("flat", "rival")}
    fitv = {law: math.log10(rf["D"] / nu1(K.nu_mono, rf["gbar"] / (a0 * (E(rf["z"]) if law == "rival" else 1.0)))) for law in ("flat", "rival")}
    for law in bound:
        n_pos[law] += bound[law] > 0
    P(f"    CRISTAL-{i:4s} z {r['z']:.3f}  f_molgas <= {byid[i]['f_molgas']:.2f}:  delta_flat >= {bound['flat']:+.3f}, delta_rival >= {bound['rival']:+.3f}   (fit route: {fitv['flat']:+.3f}, {fitv['rival']:+.3f})")
P(f"    -> discs whose lower bound is above 0: flat {n_pos['flat']} of 3, rival {n_pos['rival']} of 3 (a lower bound above 0 means the law UNDER-predicts that disc's mass discrepancy whatever the true, smaller, gas mass)")
P("\n  the lane's 'SED + gas: both laws CONSISTENT for the 9 disks that have both' rests on six detections and three upper limits used as values; the six-detection cells and the one-sided bounds are above")
open(os.path.join(LANE, "cfg213_route_detected" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if allok else 1)
