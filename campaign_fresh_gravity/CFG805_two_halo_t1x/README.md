# CFG805: the framework's own two-halo term (T1x clustering) on KiDS lensing. NARROWED: +149 → +11

| all radii (to 2.6 Mpc) | Δχ² (derived catchment − no edge) | b_eff per bin |
|---|---|---|
| CFG804, no two-halo term | +148.7 (K1 reproduced) | — |
| **with T1x two-halo term** (ξ excluded inside each catchment edge) | **+11.1. NARROWED** | 0.20 / 0.24 / 0.53 / 0.53 |
| primary R ≤ 0.31 Mpc | −2.1 | — |

**Reading.**
- Neighbours' matter, taken from the framework's own billion-particle run (T1x P_grav at z = 0.256), supplies most of the
  outer lensing signal beyond the galaxy's own catchment.
- The gap shrinks from Δχ² +149 to +11, with an effective bias of 0.2–0.5. That is low, as expected for an
  *isolated* sample, where neighbours are suppressed by construction.
- **Not closed:** Δχ² +11 > 4. The absolute fit is poor for *every* model, including the no-edge reference (χ² ≈ 160 on
  52 dof). The KiDS absolute level remains an open issue (see CFG261 and the D2 record).

**Disclosed.**
- **K2 FAIL:** σ8 recomputed from P_grav is 0.754, against the snapshot's 0.779 (3.2%; tolerance 2%). The likely cause is
  modes below the box fundamental (k < 0.08 h/Mpc), which are absent from my integral. The two-halo amplitude is absorbed
  by the free b, so the Δχ² is unaffected to first order.
- **MUTATE (no exclusion):**
  - b changes by 12–15% in bins 1–2 but only 4–6% in bins 3–4. The test bites partly.
  - Without exclusion, D_der + 2h beats no-edge + 2h by −23.8 (χ² 123). This variant double-counts matter inside the
    catchment edge, so it is a bracket, not a result.
- T1x carries inherited ΛCDM initial conditions; the NC1x native rerun is queued.
- b is a profiled nuisance, 4 per model, with the same freedom for both models.

**Status of the outer-halo problem.**
- CFG801: the settled edge is EXCLUDED.
- CFG803: the record's infall rescues the fit.
- CFG804: the census catchment closes it inside 0.31 Mpc with no free parameter.
- CFG805: the framework's own clustering narrows the outer gap from +149 to +11 (b_eff 0.2–0.5).
- Remaining: the residual +11, and the poor absolute χ² shared by all models.

κ fitted; not theory closed.

## Diagnostic: where the shared absolute χ² comes from (`diag_chi2_breakdown.py`, not a verdict)
- Block χ² for the no-edge law, by mass bin (lightest to heaviest): 17.9 / 43.2 / 45.9 / 60.6. **The heavy bins carry it.**
- The pattern is the same in bins 2–4:
  - the innermost point (35 kpc) is over-predicted (pulls −2.4 / −3.8 / −4.4);
  - 0.2–1.4 Mpc is under-predicted (pulls +2 to +3).
- So heavy lenses have relatively more mass at 0.2–1.4 Mpc than the law allows, once their mass is set by the inner points.
- This is the record's known **early-type / massive-galaxy lensing excess** (CFG585, T-K +0.28 dex), here seen in the
  profile shape. CFG727, the hot-gas reservoir currently running, is the lane aimed at it.
