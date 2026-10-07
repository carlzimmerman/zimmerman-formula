"""CFG385: self-calibrated a0(z~2.5) forecast (CFG240 Fisher model, one common calibration f free). Criteria: FROZEN_CRITERIA.md (0c47e8505).
A forecast: no data scored. Run: python3 cfg385_forecast.py ; MUTATE=1 sets b = 0.5 everywhere (singular F expected; rc 1).
"""
import itertools, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

def b(kernel, y):
    y = np.asarray(y, float)
    if MUTATE:
        return np.full_like(y, 0.5)
    if kernel == "P2":
        return 1.0 / (2 * (1 + y))
    s = np.sqrt(y)
    return s / (2 * np.expm1(s))

def sig_a0(kernel, y, sigma, tau=None):
    bb = b(kernel, y)
    F = np.array([[np.sum((1 - bb) ** 2), np.sum((1 - bb) * bb)], [np.sum((1 - bb) * bb), np.sum(bb**2)]]) / sigma**2
    if tau:
        F[0, 0] += 1 / tau**2
    if abs(np.linalg.det(F)) < 1e-300 or np.linalg.cond(F) > 1e14:
        return float("inf")
    return float(math.sqrt(np.linalg.inv(F)[1, 1]))

design = lambda ymin, ymax, N: np.logspace(math.log10(ymin), math.log10(ymax), N)
say("CFG385 self-calibrated a0(z~2.5) forecast" + ("  (MUTATE: b = 0.5 everywhere)" if MUTATE else ""))
say("=" * 78)
# C1: CFG240 break-even (P2, ymin 1e-3, N 20, sigma 0.1 -> y_max* 5.5 at sigma(log a0) 0.0999)
s_c1 = sig_a0("P2", design(1e-3, 5.5, 20), 0.1)
check("C1 reproduces CFG240's break-even (P2, y 1e-3..5.5, N 20, sigma 0.1 -> 0.0999 dex) to 2%", MUTATE or abs(s_c1 / 0.0999 - 1) < 0.02, f"{s_c1:.4f}")

T_DE, T_FLAT = 0.22, 0.19
grid = []
for kern, ymin, ymax, N, sg in itertools.product(("P2", "expRAR"), (0.05, 0.1, 0.3), (2, 5, 10, 30), (10, 20, 40, 80), (0.05, 0.1, 0.15, 0.2)):
    if ymax <= ymin:
        continue
    y = design(ymin, ymax, N)
    row = dict(kernel=kern, ymin=ymin, ymax=ymax, N=N, sigma=sg, s_free=sig_a0(kern, y, sg), s_tau03=sig_a0(kern, y, sg, 0.3),
               s_tau015=sig_a0(kern, y, sg, 0.15), floor=3 * sg / math.sqrt(N))
    grid.append(row)
c2 = all(r["s_free"] >= r["floor"] * (1 - 1e-9) for r in grid if math.isfinite(r["s_free"]))
check("C2 T4 floor sigma(log a0) >= 3 sigma/sqrt(N) holds on every cell", c2 or MUTATE, f"{len(grid)} cells")

say(f"\nDesigns reaching the DE-law vs rival 3-sigma target (sigma(log a0) <= {T_DE}) with f FREE (no calibration prior):")
for kern in ("P2", "expRAR"):
    ok = [r for r in grid if r["kernel"] == kern and r["s_free"] <= T_DE]
    say(f"  {kern}: {len(ok)} of {sum(1 for r in grid if r['kernel']==kern)} cells")
    for sg in (0.05, 0.1, 0.15, 0.2):
        best = sorted([r for r in ok if r["sigma"] == sg], key=lambda r: (r["N"], -r["ymin"], r["ymax"]))
        if best:
            r = best[0]
            say(f"    sigma {sg}: smallest N = {r['N']} (e.g. y {r['ymin']}-{r['ymax']}, sigma(log a0) {r['s_free']:.3f})")
        else:
            say(f"    sigma {sg}: none in the grid")

say("\nArchetypes (ILLUSTRATIVE; y ranges from the record, N and sigma ASSUMED)")
arch = {
    "KURVS-like (z~1.5): y 0.06-3, N 30 (10 discs x 3), sigma 0.1": (0.06, 3.0, 30, 0.1),
    "RC100-like: y 1.1-4.4 (no deep points), N 100, sigma 0.1": (1.1, 4.4, 100, 0.1),
    "CRISTAL-like: y 1-5, N 40, sigma 0.15": (1.0, 5.0, 40, 0.15),
    "NEEDED z~2.5: y 0.1-5, N 40, sigma 0.1": (0.1, 5.0, 40, 0.1),
}
arch_out = {}
for lab, (ymin, ymax, N, sg) in arch.items():
    vals = {k: sig_a0(k, design(ymin, ymax, N), sg) for k in ("P2", "expRAR")}
    vt = {k: sig_a0(k, design(ymin, ymax, N), sg, 0.3) for k in ("P2", "expRAR")}
    arch_out[lab] = dict(free=vals, tau03=vt)
    verdict = "DECIDES (<= 0.22)" if max(vals.values()) <= T_DE else ("decides only with a 0.3-dex calibration prior" if max(vt.values()) <= T_DE else "does NOT decide")
    say(f"  {lab}: sigma(log a0) P2 {vals['P2']:.3f} / expRAR {vals['expRAR']:.3f}  (with tau 0.3: {vt['P2']:.3f}/{vt['expRAR']:.3f}) -> {verdict}")

# minimum N at sigma 0.1, y 0.1..5
minN = {}
for k in ("P2", "expRAR"):
    for N in range(4, 400):
        if sig_a0(k, design(0.1, 5.0, N), 0.1) <= T_DE:
            minN[k] = N; break
say(f"\nMinimum N (sigma 0.1 dex per point, y 0.1-5, f free) for the DE-vs-rival 3-sigma: P2 {minN.get('P2')}, expRAR {minN.get('expRAR')}")
if MUTATE:
    singular = all(not math.isfinite(r["s_free"]) or r["s_free"] > 10 for r in grid)
    check("MUTATE premise: a deep-only design (b = 0.5) leaves f and a0 degenerate (singular / > 10 dex)", singular, "")
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": ""})
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG385", "mutate": MUTATE, "targets": {"DE_vs_rival": T_DE, "flat_vs_rival": T_FLAT}, "archetypes": arch_out,
           "minN_sigma0.1_y0.1_5": minN, "grid": grid, "checks": checks}, open(os.path.join(HERE, f"cfg385_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg385{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
