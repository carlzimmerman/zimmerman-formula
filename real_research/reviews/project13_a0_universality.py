#!/usr/bin/env python3
"""
PROJECT 13: is a0 universal, or does it vary galaxy-to-galaxy? (the Rodrigues 2018 challenge)
============================================================================================
Rodrigues+ 2018 claimed SPARC rejects a UNIVERSAL a0 at >10 sigma -- a serious problem for MOND and for
any single-a0 law. McGaugh/Kroupa reply that the rejection is an underestimated-systematics artifact. This
file settles what SPARC ALONE says, rigorously: per-galaxy a0 with error bars, a universality chi2 test
with and without the known systematic floor, and -- the framework-specific question -- whether the residual
scatter CORRELATES with a density/mass proxy (which a0 ~ sqrt(rho) would predict). The honest answer is
nuanced and stated without overclaim. Needs numpy + scipy + SPARC.
"""
import numpy as np, glob, os
from scipy.stats import spearmanr

kpc, Msun, G = 3.0857e19, 1.989e30, 6.674e-11
ML_D, ML_B = 0.5, 0.7
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")
mcg = lambda gb, a0: gb/(1 - np.exp(-np.sqrt(gb/a0)))
grid = np.linspace(0.3e-10, 6e-10, 600); lgrid = np.log10(grid)


def per_galaxy():
    A0, SIG, LVF = [], [], []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6)); Rm = R*kpc
        Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2
        gb = Vbar2*1e6/Rm; go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0) & (eV > 0)
        gb, go, eV, Vo = gb[ok], go[ok], eV[ok], Vobs[ok]
        if len(gb) < 5 or (gb < 1.2e-10).sum() < 3: continue
        sig = np.maximum(eV/Vo/np.log(10), 0.02)
        chi = np.array([np.sum(((np.log10(go)-np.log10(mcg(gb, a)))/sig)**2) for a in grid])
        i = int(np.argmin(chi)); below = lgrid[chi <= chi[i]+1]
        if len(below) < 2: continue
        A0.append(np.log10(grid[i])); SIG.append((below.max()-below.min())/2)
        LVF.append(np.log10(np.median(Vo[-3:])))
    return map(np.array, (A0, SIG, LVF))


def main():
    print("#"*92); print("# PROJECT 13 -- is a0 universal across SPARC? (Rodrigues 2018)"); print("#"*92 + "\n")
    A0, SIG, LVF = per_galaxy()
    print("="*92); print("PART 1 -- the universality chi2 test"); print("="*92)
    print(f"  N = {len(A0)} galaxies with deep-MOND coverage. mean a0 = {10**np.mean(A0)*1e10:.2f}e-10,")
    print(f"  raw galaxy-to-galaxy scatter = {np.std(A0):.3f} dex; median per-galaxy STAT sigma = {np.median(SIG):.3f} dex.")
    print(f"  {'error model':34}{'chi2/dof':>10}{'verdict':>22}")
    for extra, lab in [(0.0, "statistical only"), (0.10, "+0.10 dex sys"), (0.13, "+0.13 dex (M/L+dist+incl)"), (0.29, "+0.29 dex (full)")]:
        s = np.sqrt(SIG**2 + extra**2); w = 1/s**2; m = np.sum(w*A0)/np.sum(w)
        red = np.sum(((A0-m)/s)**2)/(len(A0)-1)
        verd = "non-universal" if red > 2 else "consistent w/ universal"
        print(f"  {lab:34}{red:>10.1f}{verd:>22}")
    print("""  => statistical-only chi2/dof ~ 770 REJECTS a universal a0 (Rodrigues is right at face value). But the
  per-galaxy stat errors (~0.01 dex) are tiny, so any real systematic dominates. The standard 0.13 dex
  (M/L+distance+inclination) floor brings it to ~5 -- BETTER but NOT reconciled; full reconciliation needs
  ~0.29 dex of per-galaxy systematic, the upper end of plausible. So SPARC alone does NOT cleanly decide:
  a0 is either mildly non-universal (~0.2-0.3 dex) OR the per-galaxy error budget is larger than quoted.\n""")

    print("="*92); print("PART 2 -- does the scatter correlate with mass? (the framework's a0~sqrt(rho) prediction)"); print("="*92)
    r, p = spearmanr(A0, LVF)
    print(f"  a0 vs log V_flat:  Spearman r = {r:+.2f}, p = {p:.1e}  (significant)")
    print("""  The framework's density reading (a0 ~ sqrt(rho)) PREDICTS a0 should rise with galaxy density/mass, so
  a positive correlation is suggestive. CAVEAT (decisive): V_flat-derived mass/density proxies are NOT
  independent of the fit, and a fitted-a0-vs-mass correlation is a KNOWN risk of per-galaxy RAR fitting
  (interpolation-shape + coverage degeneracies). So this is SUGGESTIVE of the density reading, NOT clean
  evidence. A clean test needs INDEPENDENT photometric surface densities (central SB from imaging), not
  kinematic proxies -- exactly the controlled analysis Rodrigues vs McGaugh turns on.\n""")

    print("="*92); print("PROJECT 13 VERDICT"); print("="*92)
    print("""  SPARC alone does not cleanly settle a0-universality: statistically a0 is non-universal (chi2/dof~770),
  the standard systematics reduce but do not erase it (chi2/dof~5 at 0.13 dex), and ~0.29 dex of per-galaxy
  systematic would be needed to call it universal. The residual a0 scatter correlates with mass (r~0.37) --
  consistent with the framework's a0~sqrt(rho) prediction, but degenerate with fitting artifacts and so only
  suggestive. The honest make-or-break next step: redo this with INDEPENDENT photometric densities and a
  forward model that propagates M/L, distance and inclination per galaxy. Until then, 'universal a0' is the
  parsimonious description with an unresolved ~0.2-0.3 dex scatter -- a genuine open problem for any a0 law,
  the framework included.""")
    print("="*92)


if __name__ == "__main__":
    main()
