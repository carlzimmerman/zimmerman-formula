"""p32: amplitude 1/sqrt 2, exponent 2 (kernel K2 of p30) with every physical cutoff of p29, against 32 pi (framework footing) and against measured a0. POST-HOC SWEEP.
Because the cutoff was varied until something matched, any single match below is a menu pick; the look-elsewhere note at the end says how easy matching is.
Run: python3 p32_amplitude_inv_sqrt2_all_cutoffs.py  |  MUTATE=1: amplitude 1/2 (check A must fail)
"""
import os, sys, math
from scipy.integrate import quad
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
c, G, hbar, eV = 2.99792458e8, 6.67430e-11, 1.054571817e-34, 1.602176634e-19
A = 0.5 if MUTATE else 1 / math.sqrt(2); s2 = 2 * A
K2 = lambda y: math.expm1(0.25 * math.log1p(y**-2 * (1 + 2 * s2 * y * y) / (1 + y * y)))
Y0 = 1e4; segs = ((1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, Y0))
core = sum(quad(lambda y: 2 * y * K2(y), s, t, limit=2000, epsabs=1e-12, epsrel=1e-11)[0] for s, t in segs)
pred = lambda acut, a0: (core + 2 * A * math.log(acut / a0 / Y0)) / 2
cuts = {"electron": 0.51099895e6 * eV * c / hbar, "proton": 938.272e6 * eV * c / hbar, "electroweak": 246.22e9 * eV * c / hbar,
        "GUT 2e16 GeV": 2e25 * eV * c / hbar, "Planck": math.sqrt(c**7 / (hbar * G))}
meas = (("SPARC record", 1.0766e-10, 0.0544), ("lane V ensemble", 1.097e-10, 0.122), ("MIGHTEE", 1.05e-10, 0.12))
print(f"   {'cutoff':14s} {'fw footing':>10s} {'vs 32pi':>8s}   " + "   ".join(f"{m[0]}: pred/obs(pull)" for m in meas))
table = {}
for nm, ac in cuts.items():
    fw = pred(ac, 9.3603e-11)
    row = []
    for lab, a0m, fe in meas:
        p_, o = pred(ac, a0m), 32 * math.pi * (9.3603e-11 / a0m)**2
        row.append((p_ - o) / (2 * fe * o))
    table[nm] = (fw, row)
    print(f"   {nm:14s} {fw:10.2f} {100*(fw/(32*math.pi)-1):+7.1f}%   " + "   ".join(f"{pred(ac, a0m):6.1f}/{32*math.pi*(9.3603e-11/a0m)**2:5.1f} ({r:+.2f})" for (lab, a0m, fe), r in zip(meas, row)))
fwE, rowE = table["electron"]
check(f"A electron cutoff: framework footing {fwE:.1f} ({100*(fwE/(32*math.pi)-1):+.0f}% vs 32 pi), but within 1.5 sigma of every measured-a0 ratio (pulls {min(rowE):+.2f} to {max(rowE):+.2f})",
      -0.40 < fwE / (32 * math.pi) - 1 < -0.30 and all(abs(r) < 1.5 for r in rowE))
inside = [nm for nm, (fw, row) in table.items() if all(abs(r) < 1.5 for r in row)]
print(f"   cutoffs consistent (|pull| < 1.5) with all three measured a0: {inside}")
check("B several of the five cutoffs are consistent with measured a0 (the data cannot pick a cutoff): a sweep that finds a match is a menu pick", len(inside) >= 2)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
