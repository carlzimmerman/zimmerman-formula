#!/usr/bin/env python3
"""CFG376 controls (frozen 2f4c18600), algebraic on the 256^3 k-range, at a = 1, 0.5, 0.1, 0.02:
C1a weights sum to 1; C1b W(0) = 1; C1c T_halo -> 0 reproduces CFG374 MIX-A exactly; MUTATE (CFG376_MUTATE=1): f_sc = 1 gives W = 1
to 1e-6 and differs from HALO-A at k = 1, z = 0 by > 0.3.  Also: the f_sc bracket [0.07, 0.09] effect on W (analytic, not run)."""
import os, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUTATE = os.environ.get("CFG376_MUTATE", "0") == "1"
SLUG = "cfg376_checks" + ("_MUTATE" if MUTATE else ""); LOG, CH = [], []
def P(s=""): print(s); LOG.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
Om = (0.02237 + 0.1200) / 0.6736**2
kJ = lambda T, a=1.0: math.sqrt(1.5 * Om * a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
MIXES = {"HALOA": (0.28, 0.54, 0.10, 0.08, 10 ** 6.5), "HALOB": (0.28, 0.54, 0.10, 0.08, 1e6), "MIXALIM": (0.28, 0.54, 0.10, 0.08, 0.0),
         "SC1": (0.0, 0.0, 0.0, 1.0, 10 ** 6.5)}
k = np.linspace(0, 2 * math.pi / (200 / 256) * math.sqrt(3) / 2, 5000)
def W(m, a=1.0, fsc=None):
    fc, fh, fha, fs, Th = MIXES[m]
    if fsc is not None: fha, fs = 0.18 - fsc, fsc
    wh = fha / (1 + (k / kJ(Th, a))**2) if Th > 0 else fha
    return fc / (1 + (k / kJ(1e4, a))**2) + fh / (1 + (k / kJ(1e6, a))**2) + wh + fs
W374 = lambda a=1.0: 0.28 / (1 + (k / kJ(1e4, a))**2) + 0.54 / (1 + (k / kJ(1e6, a))**2) + 0.18     # CFG374 MIX-A, verbatim form
AS = (1.0, 0.5, 0.1, 0.02)
if not MUTATE:
    check("C1a weights sum to 1", all(abs(sum(v[:4]) - 1) < 1e-12 for v in MIXES.values()))
    check("C1b W(0) = 1 for HALOA, HALOB (all a)", all(abs(W(m, a)[0] - 1) < 1e-12 for m in ("HALOA", "HALOB") for a in AS))
    d = max(float(np.max(np.abs(W("MIXALIM", a) - W374(a)))) for a in AS)
    check("C1c T_halo -> 0 reproduces CFG374 MIX-A (max diff, all a)", d < 1e-12, f"{d:.1e}")
    for T in (1e4, 1e6, 10**6.5): P(f"  k_J(z=0, T={T:.3g} K) = {kJ(T):.3f} h/Mpc")
    for m in ("HALOA", "HALOB", "MIXALIM"):
        P(f"  {m}: W at k = 0.3 / 1 / 3 h/Mpc (z = 0) = " + " / ".join(f"{float(np.interp(x, k, W(m))):.3f}" for x in (0.3, 1.0, 3.0)))
    for fsc in (0.07, 0.09):
        P(f"  bracket f_sc = {fsc}: HALOA W(k=1, z=0) = {float(np.interp(1.0, k, W('HALOA', 1.0, fsc))):.3f} (central {float(np.interp(1.0, k, W('HALOA'))):.3f})")
else:
    w1 = W("SC1"); dd = abs(float(np.interp(1.0, k, w1)) - float(np.interp(1.0, k, W("HALOA"))))
    check("MUTATE: f_sc = 1 gives W = 1 everywhere (to 1e-6)", float(np.max(np.abs(w1 - 1))) < 1e-6)
    check("MUTATE: differs from HALO-A at k = 1, z = 0 by > 0.3", dd > 0.3, f"({dd:.3f})")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
raise SystemExit(0 if all(CH) else 1)
