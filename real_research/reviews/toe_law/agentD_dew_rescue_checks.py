#!/usr/bin/env python3
"""
Supplements to agentD_dew_quadrupole.py -- hardening the rescue candidates before verdict.
==========================================================================================
The main script found: published DEW f(Z) fails Cassini 2026 robustly (AQUAL +2.8e-26 own
footing, +1.7e-26 framework footing; 14.6/8.8 sigma).  A tuned alpha-window passes via an
accidental sign-cancellation.  The strongest rescue candidate is (alpha=0.25, a0=framework,
Y=0.7): Q2=+3.2e-27 (0.9 sigma pass) with binned-RAR chi2 comparable to the RAR-nu benchmark
under that convention.  Per both-ways discipline (be MOST skeptical of the framework-convenient
"re-close" outcome), this script:
  A. g_ext fragility of the framework-footing window (alpha = 0.15..0.5) -- does any alpha pass
     across the full plausible g_ext range 2.0-2.48e-10?
  B. free-Upsilon RAR fits: each candidate gets its BEST convention (Y_disk scanned 0.3-1.0,
     bins recomputed per Y; binned chi2/bin and unbinned dex scatter reported at best-Y).
     Candidates: RAR-nu, DEW alpha=0 (published 2026), alpha=0.25, alpha=0.6, alpha=1 (published
     2011 ex2), at both a0 footings.
  C. AQUAL solver resolution check on the headline numbers (alpha=0 both footings).
  D. QUMOND q-integral vmax stability spot-check.
numpy/scipy only.
"""
import numpy as np
from importlib import import_module
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
m = import_module("agentD_dew_quadrupole")

A0_DEW, A0_FRAME, GEXT_FIX, GEXT_GRID = m.A0_DEW, m.A0_FRAME, m.GEXT_FIX, m.GEXT_GRID
GM_SUN, Q2_C, Q2_S = m.GM_SUN, m.Q2_C, m.Q2_S
unit = lambda a0: a0**1.5/np.sqrt(GM_SUN)

def main():
    print("#"*100)
    print("# agentD rescue checks: fragility, free-Upsilon, resolution")
    print("#"*100)

    # ---- A: framework-footing fragility
    print("\n" + "="*100)
    print("A  g_ext fragility, FRAMEWORK footing a0=9.36e-11 (AQUAL; entries Q2 [1e-27], * = 2-sigma pass)")
    print("="*100)
    print(f"  {'alpha':>6} " + " ".join(f"{g*1e10:>9.2f}" for g in GEXT_GRID))
    for al in (0.0, 0.15, 0.2, 0.25, 0.3, 0.4):
        vals = []
        for gext in GEXT_GRID:
            Q = m.aqual_Q2(lambda g, _a=al: m.mu_dew(g, _a), gext/A0_FRAME)[0]*unit(A0_FRAME)
            vals.append(f"{Q*1e27:>+8.1f}{'*' if m.passes(Q) else ' '}")
        print(f"  {al:>6.2f} " + " ".join(vals))
    print("  [pass requires Q2 in [-2.0, +5.2]e-27]")

    # ---- B: free-Upsilon RAR fits
    print("\n" + "="*100)
    print("B  free-Upsilon RAR fits (Y_disk in 0.30..1.00, bins recomputed per Y; chi2/bin at best Y)")
    print("="*100)
    Ygrid = np.arange(0.30, 1.001, 0.05)
    cands = [("RAR-nu", m.nu_rar_one),
             ("DEW a=0 (2026)", lambda y: m.nu_dew_one(y, 0.0)),
             ("DEW a=0.25", lambda y: m.nu_dew_one(y, 0.25)),
             ("DEW a=0.6", lambda y: m.nu_dew_one(y, 0.6)),
             ("DEW a=1 (2011ex2)", lambda y: m.nu_dew_one(y, 1.0))]
    # pre-load per-Y data once
    data = {}
    for Y in Ygrid:
        gN, go = m.load_sparc(Yd=Y)
        ic, med, se = m.binned_medians_se(gN, go)
        data[round(Y, 2)] = (gN, go, ic, med, se)
    print(f"  {'candidate':<19}{'a0':>11}{'best Y':>8}{'chi2/bin':>10}{'rms':>8}{'unbinned':>10}")
    print("  " + "-"*68)
    best_rows = {}
    for lab, nu1 in cands:
        for a0, alab in [(A0_DEW, "1.20e-10"), (A0_FRAME, "9.36e-11")]:
            chis = []
            for Y in Ygrid:
                gN, go, ic, med, se = data[round(Y, 2)]
                chis.append(m.rar_chi2(nu1, a0, ic, med, se))
            iY = int(np.argmin(chis)); Yb = Ygrid[iY]
            gN, go, ic, med, se = data[round(Yb, 2)]
            r = m.rar_rms(nu1, a0, ic, med)
            u = m.unbinned_scatter(nu1, a0, gN, go)
            best_rows[(lab, alab)] = (Yb, chis[iY], r, u)
            print(f"  {lab:<19}{alab:>11}{Yb:>8.2f}{chis[iY]:>10.1f}{r:>8.4f}{u:>10.4f}")
    print("  [chi2/bin ~1 = consistent with binned medians; benchmark row sets the achievable floor]")

    # ---- C: AQUAL resolution check
    print("\n" + "="*100)
    print("C  AQUAL resolution check, published f(Z) (alpha=0)")
    print("="*100)
    for a0, lab in [(A0_DEW, "own"), (A0_FRAME, "framework")]:
        et = GEXT_FIX/a0
        Q_lo = m.aqual_Q2(lambda g: m.mu_dew(g, 0.0), et)[0]*unit(a0)
        Q_hi = m.aqual_Q2(lambda g: m.mu_dew(g, 0.0), et, Nr=1100, Nth=96, lmax=12,
                          rmin=1e-3, rmax=150.0)[0]*unit(a0)
        print(f"  a0 {lab:<10}: default grid {Q_lo:+.4e}   high-res {Q_hi:+.4e}   ratio {Q_hi/Q_lo:.4f}")

    # ---- D: QUMOND vmax stability
    print("\n" + "="*100)
    print("D  QUMOND q-integral vmax stability (published f(Z), own a0, g_ext fixed)")
    print("="*100)
    for vmax in (40.0, 80.0, 160.0):
        q, eN = m.q_milgrom(GEXT_FIX/A0_DEW, lambda y: m.nu_dew_one(y, 0.0), vmax=vmax)
        Q2 = -(3.0*A0_DEW**1.5)/(2.0*np.sqrt(GM_SUN))*q
        print(f"  vmax={vmax:>6.0f}: q={q:+.6f}  Q2={Q2:+.4e}")
    print("#"*100)

if __name__ == "__main__":
    main()
