# Route cluster_dsunruh_baryons — clusters via the framework's OWN dS-Unruh interpolation + an honest baryon budget

**Date:** 2026-06-14 · **Grade: PARTIAL (leans FAILS for the framework)** · Opus 4.8 work folder
**Code:** `cluster_dsunruh_baryons.py` · **Output:** `cluster_dsunruh_baryons_output.txt`
**Data:** real eRASS1 primary (Bulbul+2024), N=9830 clean clusters, WL-calibrated M500.

## The question
Does the framework's OWN de Sitter–Unruh interpolation
`mu(a)=[sqrt(a^2+(cH)^2)-cH]/a` ⟺ `g_obs = sqrt(g_bar^2 + g_bar a0)` (the "simple" nu family,
`nu(y)=sqrt(1+1/y)`, `y=g_bar/a0`) change the ~2x cluster deficit vs standard MOND nu's, and how
much of the 2x is honest baryon accounting? All at the framework `a0=9.36e-11` (LOWER than regular
MOND `1.2e-10`, so `eta ~ 1/sqrt(a0)` is worse).

## What was COMPUTED (load-bearing)

1. **dS-Unruh nu is the WEAKEST of the three in mild MOND.** At `y=1`: `nu_dSU=1.414` vs
   `nu_simple=1.618` vs `nu_McGaugh=1.582`. The framework's own interpolation gives the *smallest*
   boost → the *largest* core deficit. The brief's hypothesis (dS-Unruh might help) **fails on the merits**.

2. **The brief's "mild MOND at R500" premise is wrong for integrated masses.** At eRASS1 R500 the
   baryonic `g_bar/a0_FRAME = 0.037` (median) — **deep MOND**, not `y~0.5-2`. The mild-MOND `y~0.5-2`
   regime lives in the cluster **core** (r~100-400 kpc, where A&A2024 finds the worst residual
   M_mm/M_bar~1-5). In deep MOND all three nu's converge to `1/sqrt(y)`, so the interpolation choice
   is **moot at R500** — there only the lower a0 hurts.

3. **eRASS1 deficit (dS-Unruh, framework a0):** `eta = M_dyn/M_pred = 2.33` [IQR 2.16–2.74].
   Regular MOND a0: `2.07`. simple/McGaugh at framework a0: `2.15`.

4. **Baryon budget (deep MOND: `eta ~ 1/sqrt(B)`):**
   - Honest non-IGIMF: ICL/BCG undercount ~+5%, missing-baryons-to-R500 ~+18% → B~1.18 → `eta 2.33→2.15`.
   - Doubling only STELLAR mass (gas dominates 5-7x) → total B~1.10-1.30 → `eta 2.33→2.23-2.05`.
   - Contested IGIMF "clusters 2x heavier" (Zhang/Zonoozi/Kroupa 2026, arXiv:2602.06082):
     reaches 88% of M_dyn (`eta~1.14`) **at a0=1.2e-10**. Implied total boost B~3.3x. Applied at the
     framework a0 + dS-Unruh nu → `eta~1.28` — still ~28% over parity.

5. **a0(z) lever at z~0.3:** declining-DE law has a small EARLY bump: `a0(z=0.3)/a0(0)=1.058` →
   deficit helped by `+0.012 dex` but **wrong-signed** (a0 rises → deficit slightly worse). A 2x
   deficit is **0.30 dex** (the brief's "0.66 dex needed" is an error: 0.66 dex = 4.6x). The a0(z)
   lever supplies ~4% of the gap, wrong sign. Confirmed negligible.

## Convention-robust truth (both ways)
- **Exact algebra, nu- and baryon-independent:** `eta_FRAME/eta_MOND = sqrt(a0_MOND/a0_FRAME) =
  sqrt(1.282) = 1.132`. The framework is robustly **~13% worse than regular MOND** on clusters.
- The 2x is NOT a hydrostatic artifact: eRASS1 M500 are WL-calibrated, and lensing (arXiv:2410.02612)
  independently finds ~2x. The deficit survives the bias-free cross-check.
- BUT absolute eta carries ~30-50% baryon-budget systematic (fstar, gas profile, ICL). The DIRECTION
  is exact; the magnitude 2.0-2.3 is uncertain at tens-of-percent.

## Verdict
This route **CLOSES LESS than the AeST route**, as predicted. The framework's own dS-Unruh
interpolation does not rescue clusters — it is the *weakest* nu in mild MOND and converges to the
others (offering no help) in the deep-MOND R500 regime, while the lower a0 deepens the deficit by an
exact 13%. Honest non-IGIMF baryon accounting closes ≤20% of the gap (eta 2.33→~2.1). Only the
contested IGIMF doubling can approach closure, and even then leaves ~1.3x at the framework a0 — i.e.
it closes MOND-at-1.2e-10, not the framework. **A ~1.9-2.1x residual survives.** Clusters remain the
framework's hardest empirical front; this route is a sharp PARTIAL, leaning FAILS for the framework.
