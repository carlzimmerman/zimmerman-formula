# CFG74 -- which LCDM-comparator choices drive the ultra-faint gate? (frozen variants on CFG73's sample)

**Question (declared before the first run).** CFG69/CFG73 found the LCDM ultra-faint gate non-discriminating (passes over about 4 decades of halo mass). Does that survive plausible changes to the halo model? DISCRIMINATING = the gate fails (|z| >= 2) at BOTH x0.1 and x10 of every halo mass. Sample 31 resolved + 9 limits; Duffy-full primary, Duffy-relaxed and Dutton-Maccio also reported; 2000 bootstrap resamples, seed 20260928.

**Result: non-discriminating under every variant except an equal-mass cored Burkert halo, whose core radius is assumed (r0 = r_s), not fitted.** Nothing here says the data favour any model.

| variant (Duffy-full, x1) | KM median | total error | z | fails x0.1 / x10 |
|---|---|---|---|---|
| V0 baseline (= CFG73) | +0.080 | 0.133 | +0.60 | no / no |
| V1 SHMR scatter 0.2 dex, 2000 draws | +0.079 | 0.126 | +0.63 | no / no |
| V2b Blumenthal contraction by the stars | +0.080 | 0.130 | +0.62 | no / no |
| V2a contraction, cosmic baryon fraction kept | +0.150 | 0.126 | +1.18 | yes (z 2.10, marginal) / no |
| V3 true floor max(Moster, f), unclamped | +0.080 | 0.089 | +0.90 | yes (+2.25) / no |
| V4b Burkert r0 = r_s (and V4a, r0 rescaled with mass) | +0.764 | 0.080 | +9.55 | yes / yes |
| V4b Burkert r0 = 0.5 r_s | +0.437 | 0.091 | +4.82 | yes / no |
| V4b Burkert r0 = 2 r_s | +0.945 | 0.043 | +21.9 | yes / yes |

- Scatter (V1) and contraction by the stars (V2b) are negligible: the stars are only 0.7% of the dark mass inside r (3.1% at most). V2a's shift is the (1 - f_b) mass loss, not the stars.
- V3: the set-scan error (0.121) is largely the scan overwriting 39 masses with 1e8/3e8; a true floor gives half-range 0.069 and the gate then fails at x0.1 under Duffy-full only (not under Duffy-relaxed or Dutton-Maccio). One-sided.
- V4 (cored): sigma_pred falls 0.69 dex and the x1 gate fails at 9.5 sigma; the pass window is 0.5-0.75 dex around x10-x100. That says the gate rejects an equal-mass cored halo, not that it measures mass; it depends on r0 and the concentration (r0 = 0.5 r_s is not discriminating under Duffy-full but is under Dutton-Maccio). A cored UFD halo is not a standard prediction.
- Combinations of variants were not run.

**Controls.** Passed: C0 (V0 reproduces CFG73), C1, C2b, C3, C4c (Burkert small-x against a 50-digit mpmath reference), C5 (MUTATE: every variant shifts by exactly -0.30103, worst deviation 5.6e-17), C6. **Failed and kept (3, the runner exits 1):** C2 (compared a stars-off contraction case with a stars-on V0; the like-for-like C2b passes), C4 (Burkert small-x tolerance 1e-6 was wrong: the correction is 3x/4 = 7.5e-4 at x = 1e-3, analytically), C4b (x = 1e-5, where double-precision cancellation gives 1.5e-6). Amendments are disclosed in the script docstring; `CFG74_disclosure/` holds the two runs before the amendments.

**Missed pre-declarations (reported):** the V2b effect is 0.001 dex against a declared 0.02-0.10; V1 lowered the total error by about 5% where an increase under 15% was declared. A 25-point fine ladder was added after the first run (reported only; a lone pass at x1e4 is probably the NFW radius clip).

Scope: the ultra-faint row only; supports CFG69/CFG73's reading that this row is weakly diagnostic for a standard NFW halo. Run: `python3 CFG74_lcdm_variants.py` (rc 1 by design), `MUTATE=1 python3 ...` (rc 1). Re-run in place by the orchestrating session; output identical to the agent's.
