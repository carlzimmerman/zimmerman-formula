"""p38: can existing high-acceleration data see PAPER42's MOND turn-off at y_t = 94 (71-117, 2 sigma)?
Data in the repository: ATLAS3D early types (Cappellari+13, real_research/data/atlas3d_fj_table.tsv; CFG33's parsing: r_1/2, Salpeter M*, JAM mass, qual >= 1);
SLACS lenses (CFG33: g_N ~ 10 a0 at the Einstein radius). For each ATLAS3D galaxy, y = G (M*/2)/r_1/2^2 / a0 (h9/CFG33 convention) and the turn-off's effect on the
predicted dynamical mass, Delta log M = log10[nu_fix(y)/nu(y)]. Compared with the per-galaxy systematic floor (CFG33: 0.10 dex IMF/population) and the sample's
statistical reach (scatter/sqrt N). a0 = 1.097e-10 (measured, the a0 PAPER42 used).
Run: python3 p38_high_accel_turnoff.py  |  MUTATE=1: turn-off at y_t = 1 (a gross turn-off; check D must flip to 'detectable')
"""
import os, sys, math
import numpy as np
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
G, MSUN, KPC, a0 = 6.674e-11, 1.989e30, 3.0857e19, 1.097e-10
nu = lambda y: np.sqrt(1 + 1 / y)
nufix = lambda y, yt: 1 + (np.sqrt(1 + 1 / y) - 1) / (1 + (y / yt)**2)
rw = [l.rstrip("\n").split("\t") for l in open(os.path.join(R, "real_research", "data", "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
ah = {h: i for i, h in enumerate(rw[0])}
def fl(s):
    try: return float(s)
    except Exception: return float("nan")
ys = []
for d in rw[1:]:
    D, lr12, lL, lml, q = (fl(d[ah[k]]) for k in ("Dist_Mpc", "logr12", "logL", "logML_Salp", "qual"))
    if not all(np.isfinite(v) for v in (D, lr12, lL, lml, q)) or q < 1: continue
    r12 = 10**lr12 / 206264.806 * D * 1e3 * KPC; M = 10**(lml + lL) * MSUN
    ys.append(G * (M / 2) / r12**2 / a0)
ys = np.array(ys)
print(f"   ATLAS3D (qual >= 1): N = {len(ys)}, y = g_N(r_1/2)/a0: median {np.median(ys):.1f}, 90th pct {np.percentile(ys, 90):.1f}, max {ys.max():.1f}")
yts = (1.0,) if MUTATE else (71.3, 94.1, 116.8)
for yt in yts:
    eff = np.log10(nufix(ys, yt) / nu(ys))
    print(f"   y_t = {yt:6.1f}: Delta log M_dyn  median {np.median(eff):+.5f}  max |.| {np.abs(eff).max():.5f} dex;  sample mean {eff.mean():+.5f} vs reach 0.10/sqrt(N) = {0.10/math.sqrt(len(ys)):.4f}")
yt0 = 1.0 if MUTATE else 94.1
eff0 = np.log10(nufix(ys, yt0) / nu(ys))
for ySL in (5, 10, 20):
    print(f"   SLACS-like y = {ySL}: Delta log M = {math.log10(nufix(ySL, yt0) / nu(ySL)):+.5f} dex (CFG33 floor 0.10 dex)")
detect = abs(eff0.mean()) > 3 * 0.10 / math.sqrt(len(ys))
check(f"D existing early-type dynamics and lensing CANNOT see the turn-off: sample-mean shift {eff0.mean():+.5f} dex vs 3x the reach {3*0.10/math.sqrt(len(ys)):.4f}", not detect)
need = abs(eff0.mean())
check(f"P to see it, a sample would need a shared (systematic) calibration of ~{need:.4f} dex -- about {0.10/need if need else float('inf'):.0f}x better than today's 0.10 dex IMF floor", need < 0.01)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
