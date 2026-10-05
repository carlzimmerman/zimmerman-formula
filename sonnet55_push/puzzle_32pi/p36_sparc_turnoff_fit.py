"""p36: fit the turn-off y_t of nu_fix = 1 + (sqrt(1+1/y) - 1)/(1 + (y/y_t)^2) on SPARC (lane V machinery), a profiled at each y_t.
Question: do galaxies show the offset reading's turn-off at y_t ~ 94-103 (measured a0) or 128.9 (framework footing)? Or can SPARC only bound y_t from below?
Delta chi2(y_t) = chi2_min(y_t) - chi2_min(no turn-off). Independent-point chi2; lane V's crude clustering deflation is ~x18 (quoted).
Samples: all (Upsilon free, sigma_int 0.0808), MLS16 cuts (Upsilon 0.5, 0.11 dex), and the bulge-bearing galaxies (any V_bul > 0; Upsilon free), where y is largest.
Also: the expected size of the effect -- the change in log10 g at y = 10, 30, 100 for y_t = 100.
Run: python3 p36_sparc_turnoff_fit.py  |  MUTATE=1: turn-off applied to the DEEP regime instead (suppression 1/(1+(y_t/y)^2)): the lower bound must change (check C fails)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def IF(yt):
    def f(gb, a):
        y = gb / a; base = np.sqrt(1 + 1 / y) - 1
        sup = 1 / (1 + (yt / y)**2) if MUTATE else 1 / (1 + (y / yt)**2)
        return gb * (1 + base * sup)
    return f
for y in (10, 30, 100):
    b = math.sqrt(1 + 1 / y) - 1
    print(f"   effect of y_t = 100 at y = {y}: log10 g changes by {math.log10((1 + b / (1 + (y/100)**2)) / (1 + b)):+.4f} dex (SPARC scatter ~0.1 dex)")
gals = V.load_sparc()
A = np.exp(np.linspace(math.log(0.5e-10), math.log(2.5e-10), 49))
YT = [1, 2, 3, 5, 10, 20, 50, 94, 100, 128, 300, 1e3, 1e4]
samples = {"all, Upsilon free": (gals, {}, 0.0808),
           "MLS16 cuts, Upsilon 0.5": ([g for g in gals if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30], dict(ufixed=0.5), 0.11),
           "bulge-bearing, Upsilon free": ([g for g in gals if np.any(g["Vbul"] > 0)], {}, 0.0808)}
lower = {}; dvals = {}
for lab, (sel, kw, sint) in samples.items():
    base = V.Profile(sel, V.IF_alpha1, **kw).scan(A, sint).min()
    d = {yt: V.Profile(sel, IF(yt), **kw).scan(A, sint).min() - base for yt in YT}
    best = min(d, key=d.get)
    lb = min([yt for yt in YT if d[yt] < 4.0], default=None)          # smallest y_t with Delta chi2 < 4 (independent points)
    lower[lab] = lb; dvals[lab] = d
    print(f"   {lab:28s} ({len(sel)} gal): " + "  ".join(f"{yt:g}:{d[yt]:+.1f}" for yt in YT))
    print(f"      best y_t = {best:g} (Delta chi2 {d[best]:+.2f}); Delta chi2 < 4 for y_t >= {lb if lb is not None else "none"}; offset-reading values: 94 -> {d[94]:+.2f}, 128 -> {d[128]:+.2f}")
check("A SPARC can only bound y_t from below: every y_t >= 50 is within Delta chi2 = 4 of no turn-off in all three samples", all(lb is not None and lb <= 50 for lb in lower.values()))
check("B the offset reading's y_t = 94 and 128 are ALLOWED but NOT DETECTED: |Delta chi2| < 4 in every sample (its signature is <= 0.002 dex at y <= 100)",
      all(abs(d[94]) < 4 and abs(d[128]) < 4 for d in dvals.values()))
check("C the lower bound sits at y_t of a few (the strong-field turn-off cannot be pushed into the galaxy range y <~ 10)", all(lb is not None and lb >= 2 for lb in lower.values()))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
