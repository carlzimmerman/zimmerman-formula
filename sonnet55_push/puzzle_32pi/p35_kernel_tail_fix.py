"""p35: fix the framework kernel's strong-field tail.  nu_fix(y) = 1 + (sqrt(1 + 1/y) - 1) / (1 + (y/y_t)^k)   (k = 2 default; also k = 3, 4).
Below y_t it IS the framework law (deep limit, landmark triplet, SPARC range untouched); above it nu - 1 ~ y^-(1+k).
Tests: (S) SPARC chi2 vs the exact law (lane V machinery, both Upsilon treatments); (P) planetary anomalies dg = (nu - 1) g_N against the record's bounds
(real_research/reviews/mi_alpha1_solar_system_2026.out, bare, no EFE credit: Mercury 7.52e-13, Venus 3.23e-11, Earth 3.66e-14, Mars 3.72e-14 m/s^2);
(V) the QUMOND/BIMOND vacuum integral I = int 2y (nu - 1) dy is finite; Lambda/a0^2 = I/2 (p21/p25) and the y_t that would make it 32 pi (IF the a0 sector's vacuum
is the dark energy -- lane K's offset reading, an INPUT).  a0 = 9.3603e-11 (framework footing).
Run: python3 p35_kernel_tail_fix.py  |  MUTATE=1: k = 0 (no suppression = the exact law): checks P and V must fail
"""
import os, sys, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
a0 = 9.3603e-11
def nm1(y, yt, k):                       # nu - 1, cancellation-free
    base = math.expm1(0.5 * math.log1p(1 / y))
    return base if (MUTATE or k == 0) else base / (1 + (y / yt)**k)
def IF_fix(yt, k):
    def f(gb, a):
        y = gb / a
        base = np.sqrt(1 + 1 / y) - 1
        sup = 1.0 if (MUTATE or k == 0) else 1 / (1 + (y / yt)**k)
        return gb * (1 + base * sup)
    return f
# (S) SPARC
gals = V.load_sparc()
A = np.exp(np.linspace(math.log(0.5e-10), math.log(2.5e-10), 61))
print("   (S) SPARC chi2: exact law vs tail-fixed (k = 2), lane V machinery")
dmax = 0.0
for lab, sel, kw, sint in (("fixed Upsilon 0.5, MLS16 cuts", [g for g in gals if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30], dict(ufixed=0.5), 0.11),
                           ("Upsilon free, all", gals, {}, 0.0808)):
    base = V.Profile(sel, V.IF_alpha1, **kw).scan(A, sint)
    line = f"     {lab:30s} exact law chi2_min {base.min():8.1f}"
    for yt in (100.0, 128.0, 1e3):
        ch = V.Profile(sel, IF_fix(yt, 2), **kw).scan(A, sint)
        d = ch.min() - base.min(); dmax = max(dmax, abs(d))
        line += f" | y_t = {yt:5.0f}: {d:+.2f}"
    print(line)
check(f"S SPARC cannot tell the tail-fixed kernel from the exact law for y_t >= 100 (|Delta chi2| <= {dmax:.2f}, < 2 on ~3000 points)", dmax < 2.0)
# (P) planets
planets = {"Mercury": (4.228e8, 7.52e-13), "Venus": (1.211e8, 3.23e-11), "Earth": (6.336e7, 3.66e-14), "Mars": (2.729e7, 3.72e-14)}
ymax = {}
for nm, (y, b) in planets.items():
    try:
        ymax[nm] = brentq(lambda lyt: nm1(y, 10**lyt, 2) * y * a0 - b, 0, 9) if nm1(y, 1e9, 2) * y * a0 > b else 9.0
    except ValueError:
        ymax[nm] = 0.0          # no y_t in [1, 1e9] passes (MUTATE: no suppression)
yt_hi = min(ymax.values())
print("   (P) largest y_t each planet allows (k = 2): " + ", ".join(f"{k} {10**v if v < 9 else v:.2e}" for k, v in ymax.items()))
for yt in (128.0, 1e3, 1e5):
    worst = max(nm1(y, yt, 2) * y * a0 / b for y, b in planets.values())
    print(f"     y_t = {yt:8.0f}: worst planet anomaly / bound = {worst:.2e}")
worst128 = max(nm1(y, 128.0, 2) * y * a0 / b for y, b in planets.values())
check(f"P every planet passes for y_t up to {10**yt_hi:.1e} (Mars binds); at y_t = 128 the worst planet sits at {worst128:.1e} of its bound", worst128 < 1)
# (V) vacuum integral
Y0 = 1e4
def I(yt, k):
    segs = [(1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, 1e5), (1e5, 1e7)]
    tot = sum(quad(lambda y: 2 * y * nm1(y, yt, k), s, e, limit=4000, epsabs=1e-10, epsrel=1e-10)[0] for s, e in segs)
    return tot + (0 if (MUTATE or k == 0) else 0.0)      # tail beyond 1e7 ~ yt^k * 1e7^(1-k) -> negligible for k >= 2 and yt << 1e7
print("   (V) vacuum integral I(y_t) and Lambda/a0^2 = I/2")
for k in (2, 3, 4):
    vals = [I(yt, k) / 2 for yt in (100.0, 128.0, 1e3)]
    try:
        ysol = brentq(lambda yt: I(yt, k) - 64 * math.pi, 10, 1e4)
    except ValueError:
        ysol = float('nan')
    print(f"     k = {k}: Lambda/a0^2 at y_t = 100, 128, 1000: {vals[0]:.2f}, {vals[1]:.2f}, {vals[2]:.1f};  32 pi needs y_t = {ysol:.1f} (= {ysol*a0:.2e} m/s^2)")
    if k == 2: y2 = ysol
check(f"V the vacuum integral is FINITE (k = 2, y_t = 128: Lambda/a0^2 = {I(128.0, 2)/2:.2f}); the exact law's diverges (MUTATE)", I(128.0, 2) < 1e3 and I(1e3, 2) < 1e4)
check(f"W if the a0 sector's vacuum IS the dark energy, k = 2 needs y_t = {y2:.1f} -- inside both the SPARC (>= 100) and planetary (<= {10**yt_hi:.0e}) windows; k = 3, 4 give other values (shape-dependent)",
      (y2 == y2) and 100 <= y2 <= 10**yt_hi)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
