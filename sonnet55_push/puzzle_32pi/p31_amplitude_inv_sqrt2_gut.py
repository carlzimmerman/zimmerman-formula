"""p31: as p30 (amplitude 1/sqrt 2, exponent 2, kernels K1-K3) but cut at the GUT scale, a_cut = E_GUT c/hbar, E_GUT = 2e16 GeV (p29's value). POST-HOC.
Run: python3 p31_amplitude_inv_sqrt2_gut.py  |  MUTATE=1: Planck cutoff instead (check A must fail)
"""
import os, sys, math
from scipy.integrate import quad
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
c, G, hbar, eV = 2.99792458e8, 6.67430e-11, 1.054571817e-34, 1.602176634e-19
acut = math.sqrt(c**7 / (hbar * G)) if MUTATE else 2e25 * eV * c / hbar
A = 1 / math.sqrt(2); s2 = 2 * A; T = 64 * math.pi
K = {"K1": lambda y: math.expm1(0.25 * math.log1p(y**-2 * (1 + 2 * s2 * y) / (1 + y))),
     "K2": lambda y: math.expm1(0.25 * math.log1p(y**-2 * (1 + 2 * s2 * y * y) / (1 + y * y))),
     "K3": lambda y: (lambda w: math.expm1(0.5 * math.log1p(w)))((math.sqrt(1 + 4 * ((1 + s2 * y) / (1 + y)) / y**2) - 1) / 2)}
Y0 = 1e4; segs = ((1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, Y0))
core = {k: sum(quad(lambda y: 2 * y * e(y), s, t, limit=2000, epsabs=1e-12, epsrel=1e-11)[0] for s, t in segs) for k, e in K.items()}
print(f"   cutoff a = {acut:.3e} m/s^2 ({'Planck' if MUTATE else 'GUT 2e16 GeV'})")
fw = {}
for k in K:
    v = (core[k] + 2 * A * math.log(acut / 9.3603e-11 / Y0)) / 2; fw[k] = v
    print(f"   framework footing {k}: Lambda/a0^2 = {v:.2f} vs 32 pi = {32*math.pi:.2f} ({100*(v/(32*math.pi)-1):+.1f}%)")
check("A on the framework footing the GUT cutoff falls 4-5% short of 32 pi (ln(a_GUT/a_P) = -6.4, times 1/sqrt 2 = -4.5)", all(-0.06 < v / (32 * math.pi) - 1 < -0.03 for v in fw.values()))
pulls = []
for lab, a0m, fe in (("record SPARC 1.0766e-10", 1.0766e-10, 0.0544), ("lane V ensemble 1.097e-10", 1.097e-10, 0.122), ("MIGHTEE 1.05e-10", 1.05e-10, 0.12)):
    pred = (core["K2"] + 2 * A * math.log(acut / a0m / Y0)) / 2; obs = 32 * math.pi * (9.3603e-11 / a0m)**2; err = 2 * fe * obs
    pulls.append((pred - obs) / err)
    print(f"   measured a0 {lab:26s}: predicted {pred:6.2f}  observed {obs:6.2f} +- {err:5.2f}  pull {(pred-obs)/err:+.2f} sigma")
check(f"B against measured a0 the GUT version is still high (pulls {min(pulls):+.2f} to {max(pulls):+.2f} sigma, all > 0): closer than Planck, not a match",
      all(0.5 < p_ < 3.0 for p_ in pulls))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
