# CFG365 FROZEN CRITERIA: the supply cap keyed to the ORIGINAL baryon reservoir

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans. Never "theory closed". Owner (2026-10-06, chat "Nobel Prize and neutrinos"):
"run the original baryon reservoir cap test". The orchestrator was told first.

**Question.** CFG364 (5e44cd0d9): a cap on PRESENT baryons, dark = min(M_ph, 5.364 M_b,now), breaks 26-33% of SPARC
galaxies. If the supply belongs to each system's ORIGINAL baryons, M_b,orig = M_b,now/f_ret, the cap becomes
min(M_ph, 5.364 M_b,now/f_ret). How small must the retained fraction f_ret be for the cap not to bind where the law is
measured, and is that compatible with the measured cosmic baryon census?

## Inputs (declared)
- Per-galaxy Q = M_ph(<R_last)/(5.364 M_b,now) and Q_obs, read from CFG364's committed results JSON (both footings, never
  pooled). Required retention f_req = 1/Q (the cap does not bind iff f_ret <= f_req).
- **System edge (whole-system phantom).** Point-mass baryons in an external field g_e: once y < g_e/a0 the enclosed
  phantom freezes at (nu_mono(g_e/a0) - 1) M_b. So f_req,edge = 5.364/(nu_mono(g_e/a0) - 1), galaxy-independent, for
  g_e in {0.01, 0.03} a0.
- **Retention benchmark (the global census, a COSMIC MEAN, not per galaxy):** Shull, Smith & Danforth 2012 (ApJ 759, 23):
  galaxies, groups and clusters hold ~10% of the baryons, and collapsed phases including the CGM hold 18 +- 4%. So
  f_census in [0.07, 0.18], where the lower end is galaxies only and the upper end is all collapsed phases including the CGM.

## Tests
**T0 (controls).** Read CFG364's JSON (175 rows per footing). Reproduce its canonical break count, 46. Reproduce
5.364 = 0.1200/0.02237.

**T1 (R_last).** The fraction of galaxies with f_req < f_census,hi = 0.18. Those galaxies would need to have lost MORE than
the census mean for the cap not to bind. Also the fraction with f_req < 0.07 (they would need to retain less than even the
galaxies-only census mean). By class.

**T2 (edge).** f_req,edge for both g_e, against 0.07 and 0.18.

## Verdict classes (declared)
- **VIABLE (galaxy level):** canonical, no galaxy has f_req < 0.07 at R_last, AND f_req,edge >= 0.07 for both g_e.
  At census-level retention the reservoir supply then covers the phantom everywhere it is measured.
- **STRAINED:** some galaxies have f_req < 0.07, but they are under 10% of the sample and all are dwarfs or intermediates.
- **DEAD:** at least 10% of galaxies, or any massive galaxy, have f_req < 0.07; OR f_req,edge < 0.07 for both g_e.
- Alt reported separately. The observational Q_obs version is reported.
- Scope: GALAXY LEVEL ONLY. A VIABLE result says the reservoir cap does not break galaxies. It says nothing about whether
  the cap fixes the growth/lensing double count, which needs the PM run (the orchestrator's).
- The census is a cosmic mean. Individual galaxies, dwarfs above all, can retain less. A VIABLE result therefore also
  carries the caveat that per-galaxy retention is not predicted by the framework.

**MUTATE.** Cosmic ratio 5.364 -> 0.5364 (supply x 0.1). The verdict must change from the main run's, rc = 1.

Local compute only. No downloads (the census numbers are quoted above).
