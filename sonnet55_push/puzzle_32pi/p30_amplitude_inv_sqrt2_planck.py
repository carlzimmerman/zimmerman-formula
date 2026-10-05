"""p30: tail nu - 1 -> (1/sqrt 2)/y^2 (exponent 2, amplitude 1/sqrt 2) with the Planck cutoff in BIMOND's vacuum (Lambda/a0^2 = I/2, I = int_0^Y 2y(nu-1) dy).
POST-HOC: the amplitude was suggested by p29's SOLVED value A = 0.706; this tests it, it does not predict it.
Three kernels, all with the deep-MOND limit nu -> y^-1/2 and the tail (1/sqrt 2) y^-2 (checked numerically), differing in the transition shape:
 K1 nu = (1+u)^(1/4), u = y^-2 (1 + 2 sqrt2 y)/(1 + y)       K2 nu = (1+u)^(1/4), u = y^-2 (1 + 2 sqrt2 y^2)/(1 + y^2)
 K3 nu^2 = (1 + sqrt(1 + 4 g/y^2))/2, g = (1 + sqrt2 y)/(1 + y)
I = core(0..1e4) + 2A ln(Y/1e4) (+ O(1e-8)); Y = a_P/a0 for both footings.  Look-elsewhere estimate: how often a 'nice' amplitude lands this close given the menu of choices.
Run: python3 p30_amplitude_inv_sqrt2_planck.py  |  MUTATE=1: amplitude 1/2 instead of 1/sqrt 2 in all kernels (check A must fail)
"""
import os, sys, math
from scipy.integrate import quad
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
c, G, hbar = 2.99792458e8, 6.67430e-11, 1.054571817e-34
aP = math.sqrt(c**7 / (hbar * G)); T = 64 * math.pi
A = 0.5 if MUTATE else 1 / math.sqrt(2)
s2 = 2 * A           # = sqrt 2 for A = 1/sqrt 2
K = {
 "K1": lambda y: math.expm1(0.25 * math.log1p(y**-2 * (1 + 2 * s2 * y) / (1 + y))),
 "K2": lambda y: math.expm1(0.25 * math.log1p(y**-2 * (1 + 2 * s2 * y * y) / (1 + y * y))),
 "K3": lambda y: math.sqrt((1 + math.sqrt(1 + 4 * ((1 + s2 * y) / (1 + y)) / y**2)) / 2) - 1 if y < 1e3 else
                 (lambda w: math.expm1(0.5 * math.log1p(w)))((math.sqrt(1 + 4 * ((1 + s2 * y) / (1 + y)) / y**2) - 1) / 2),
}
Y0 = 1e4; segs = ((1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, Y0))
for nm, e in K.items():
    deep = (1 + e(1e-8)) * math.sqrt(1e-8); tail = e(1e6) * 1e12
    print(f"   {nm}: deep nu sqrt(y) at y=1e-8 = {deep:.4f}; tail (nu-1) y^2 at y=1e6 = {tail:.5f} (A = {A:.5f})")
check("K all three kernels have the deep-MOND limit (nu sqrt y -> 1) and the stated tail amplitude", all(abs((1 + e(1e-8)) * 1e-4 - 1) < 2e-2 and abs(e(1e6) * 1e12 - A) < 1e-3 for e in K.values()))
vals = {}
for lab, a0 in (("framework 9.36e-11", 9.3603e-11), ("alt 1.131e-10", 1.1312e-10)):
    Y = aP / a0
    for nm, e in K.items():
        core = sum(quad(lambda y: 2 * y * e(y), s, t, limit=2000, epsabs=1e-12, epsrel=1e-11)[0] for s, t in segs)
        I = core + 2 * A * math.log(Y / Y0)
        vals[(lab, nm)] = I / 2
        print(f"   {lab:20s} {nm}: Lambda/a0^2 = {I/2:8.3f}  vs 32 pi = {32*math.pi:.3f}  ({100*(I/T - 1):+.2f}%)")
dev = [abs(v / (32 * math.pi) - 1) for v in vals.values()]
spread = max(vals.values()) - min(vals.values())
check(f"A amplitude 1/sqrt 2 + Planck cutoff lands within 1% of 32 pi for all kernels and both footings (max deviation {100*max(dev):.2f}%)", max(dev) < 0.01)
check(f"B the transition shape moves the result by {spread:.2f} (= {100*spread/(32*math.pi):.1f}%): the 'exact' match is kernel-dependent at the few-tenths-percent level", spread > 0.05)
# HONEST TEST (added after the first run): 32 pi is the observed Lambda/a0^2 only on the framework footing, where a0 is DEFINED from Lambda. With a measured a0 the
# observed ratio is Lambda/a0_meas^2 = 32 pi (9.3603e-11/a0_meas)^2; its error is 2 x the a0 error. Predicted ratio = A ln(a_P/a0) + c/2 (K2 shape, the closest).
eK2 = K["K2"]; coreK2 = sum(quad(lambda y: 2 * y * eK2(y), s_, t_, limit=2000, epsabs=1e-12, epsrel=1e-11)[0] for s_, t_ in segs)
print("   measured a0 (lane V determinations): predicted vs OBSERVED Lambda/a0^2")
pulls = []
for lab, a0m, fe in (("record SPARC profile 1.0766e-10", 1.0766e-10, 0.0544), ("lane V ensemble 1.097e-10 +-12%", 1.097e-10, 0.122),
                     ("MLS16 1.20e-10 +-20%", 1.20e-10, 0.201), ("MIGHTEE CFG301 1.05e-10", 1.05e-10, 0.12)):
    pred = (coreK2 + 2 * A * math.log(aP / a0m / Y0)) / 2 if False else (coreK2 + 2 * A * math.log((aP / a0m) / Y0)) / 2
    obs = 32 * math.pi * (9.3603e-11 / a0m)**2; err = 2 * fe * obs
    pulls.append((pred - obs) / err)
    print(f"     {lab:34s} predicted {pred:7.2f}  observed {obs:6.2f} +- {err:5.2f}  pull {(pred-obs)/err:+.2f} sigma")
check("D with a MEASURED a0 the prediction (~100) sits above the observed Lambda/a0^2 (~70-85) by about 1-2 sigma: the 0.0% match exists only on the footing that defines a0 from Lambda",
      all(0.5 < p_ < 3.5 for p_ in pulls))
# look-elsewhere: choices made = cutoff (5 scales in p29), BIMOND normalisation (f'(1) = 0 or 1: factor 2), 'nice' amplitudes in [0.2, 1.5]
nice = [0.25, 1/3, 0.5, 1/math.sqrt(3), 2/3, 1/math.sqrt(2), 0.75, math.pi/4, 1, math.sqrt(2), 1/math.pi, 2/math.pi, 1/math.e, math.log(2)]
win = max(dev)
p_one = min(1, len(nice) * 2 * win)           # rough: each nice value covers a relative window +-win around the solved amplitude
n_tries = 5 * 2
p_any = 1 - (1 - p_one)**n_tries
print(f"   look-elsewhere (rough): {len(nice)} nice amplitudes x window +-{100*win:.2f}% -> {100*p_one:.1f}% per (cutoff, normalisation) choice; over {n_tries} choices ~ {100*p_any:.0f}%")
check("C the match is not significant after the choices made (rough look-elsewhere probability > 5%)", p_any > 0.05)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
