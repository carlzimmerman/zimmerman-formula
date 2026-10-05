"""p39: classical UV completion of the MOND field. Dimensional fact: G, c, a0 admit NO dimensionless combination, so a classical, parameter-free completion can only
fix the vacuum term as a pure number set by its kernel: Lambda c^4/a0^2 = I/2, I = int_0^inf (nu - 1) d(y^2) (p21/p25). Required: I = 2 x 73.19 = 146.4 (measured a0,
lane V ensemble) to 2 x 32 pi = 201.1 (kappa = 1/2 footing).
Catalog of kernels with a published rationale (QUMOND nu form; cancellation-free nu - 1; numeric to 1e7 + analytic tail where the tail is a power law):
  framework / Milgrom 1999 sqrt(1+1/y); simple; standard; RAR exponential (McGaugh); Milgrom nu_n family (n = 2.5, 3, 4, 6); 'Bose' nu = 1/(1 - e^-y)^(1/2)...
Equivalent framework-kernel cut: the y_t (k = 2) at which the framework kernel + turn-off gives the same I.
Run: python3 p39_uv_completion_catalog.py  |  MUTATE=1: the requirement halved (check A must still... -> check R must fail)
"""
import os, sys, math
from scipy.integrate import quad
from scipy.optimize import brentq
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
REQ = (73.19, 100.53) if not MUTATE else (73.19 / 2, 100.53 / 2)
segs = [(1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, 1e5), (1e5, 1e7)]
def I(nm1, tailA=None, tailp=None):
    tot = sum(quad(lambda y: 2 * y * nm1(y), s, e, limit=4000, epsabs=1e-10, epsrel=1e-10)[0] for s, e in segs)
    if tailA is None: return tot
    if tailp <= 2: return float("inf")
    return tot + 2 * tailA * (1e7)**(2 - tailp) / (tailp - 2)
K = {
 "framework / Milgrom 1999  sqrt(1+1/y)": (lambda y: math.expm1(0.5 * math.log1p(1 / y)), 0.5, 1.0),
 "simple  1/2 + sqrt(1/4 + 1/y)":         (lambda y: 0.5 + math.sqrt(0.25 + 1 / y) - 1, 1.0, 1.0),
 "standard  [(1+sqrt(1+4/y^2))/2]^(1/2)": (lambda y: math.expm1(0.5 * math.log1p((math.sqrt(1 + 4 / y**2) - 1) / 2)), 0.5, 2.0),
 "RAR (McGaugh)  1/(1 - e^-sqrt y)":      (lambda y: 1 / (-math.expm1(-math.sqrt(y))) - 1, None, None),
}
for n in (2.5, 3, 4, 6):
    K[f"Milgrom nu_n, n = {n}"] = (lambda y, n=n: math.expm1(math.log1p(2 * y**(-n) / (1 + math.sqrt(1 + 4 * y**(-n)))) / n), 1 / n, float(n))
fw = lambda y, yt: math.expm1(0.5 * math.log1p(1 / y)) / (1 + (y / yt)**2)
def equiv_yt(Ival):
    if not math.isfinite(Ival): return float("inf")
    return brentq(lambda yt: I(lambda y: fw(y, yt)) - Ival, 0.05, 1e5)
print(f"   required I = 2 x Lambda c^4/a0^2 = {2*REQ[0]:.1f} (measured a0) ... {2*REQ[1]:.1f} (kappa = 1/2 footing)")
best = 0.0
for nm, (f, A, p) in K.items():
    v = I(f, A, p) if A is not None else I(f)
    fin = math.isfinite(v)
    if fin: best = max(best, v)
    print(f"   {nm:40s} I = {v if fin else float('inf'):10.3f}   Lambda c^4/a0^2 = {(v/2) if fin else float('inf'):8.3f}   equivalent framework cut y_t = {equiv_yt(v):8.2f}")
check(f"A every principled kernel with a FINITE vacuum term gives I <= {best:.1f}, short of the required {2*REQ[0]:.0f}-{2*REQ[1]:.0f} by x{2*REQ[0]/best:.1f}-{2*REQ[1]/best:.1f}", best < 2 * REQ[0])
yt_req = (equiv_yt(2 * REQ[0]), equiv_yt(2 * REQ[1]))
check(f"R the requirement is equivalent to the framework kernel's 1/(2y) tail persisting to y_t = {yt_req[0]:.0f}-{yt_req[1]:.0f}; RAR's exponential tail ends near y ~ {equiv_yt(I(K['RAR (McGaugh)  1/(1 - e^-sqrt y)'][0])):.0f}",
      90 < yt_req[0] < 100 and 125 < yt_req[1] < 132)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
