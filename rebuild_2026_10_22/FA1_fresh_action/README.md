# FA1_fresh_action: no action found. Of ten fresh selector ideas, four were untested as stated; the best one (I1, tidal isotropy of the baryons) is KILLED AT GATE 1 on both footings: 42 % of SPARC's low-acceleration points look as cluster-like as X-COP (line 4.6 %)

Not blind. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
Adopts nothing. The cold sector stays retired. This lane graded a selector on baryon data only, so it did not reopen the
cold sector under the owner's 11-04 lift.

Order on record: `PHASE1_IDEAS.md` (825da66d06), written and committed before any repo file was read;
`PHASE2_RECORD_CHECK.md` (after the record check); `FROZEN_CRITERIA.md` (d7c4be8f4c), committed alone before any number;
then `fa1_zeta.py` → `fa1.out`, `fa1_results.json`, MUTATE twin `fa1_MUTATE.out`, `fa1_results_MUTATE.json`;
post-result diagnostics with no label: `fa1_diag.py` → `fa1_diag.out`, `fa1_diag.json`.

## Every idea
| id | selector | status (Phase 2) | graded here |
|---|---|---|---|
| I1 | tidal isotropy of the baryons, zeta = rho_b / rho_bar_b (Weyl-electric over Ricci) | UNTESTED as a dust selector (neighbours X67, KT30 tested other uses) | **KILLED AT GATE 1**, both footings |
| I2 | mean-flow vorticity | PARTLY TESTED (DR5 40d43dbb8a; uncommitted vorticity_gate) | **KILLED**, both readings, both footings (`I2_vorticity/`): Phase 1's omega_* ~ a0/c is 27-130x below the ICM's shear floor (dust off in clusters); scale-free V/sigma reading fails the ellipticals (13 on, +0.094 vs +0.199, Z -2.15); dSph extra ALLOWED (12 -> 12 of 19) |
| I3 | fixed Jeans length, k^4 dispersion | TESTED, FAIL (X22 a2b532e3c6, X57 M4 436ff03cb9) | no |
| I4 | staticity, AeST dust term | TESTED, FAIL / NO VERDICT (H1 1654b84f78, H2 385f61a14c, AN1 a3ce1814c5) | no |
| I5 | bulk motion against the khronon frame, disformal | UNTESTED; dead on order of magnitude (LG 600 km/s vs clusters 300-1000 km/s) | no |
| I6 | Galileon determinant, source dimensionality | UNTESTED as a dust switch (galileons for planets: M1 836cc3661f) | **KILLED AT THE SPARC NULL**, both footings (`I6_galileon/`): cubic-galileon field solve; 3 of 6 SPARC-like discs stay on (gas-rich dwarfs), spherical f_SP 0.429; Q2 fails on pi's own force at beta = 1 |
| I7 | defect network of the a0 field | UNTESTED; dead on paper (strings, walls are not w = 0) | no |
| I8 | Weyl/Ricci of the full metric | PARTLY TESTED (K1 83d3592c87); reads as gas density in clusters | no |
| I9 | nonlocal curvature history, box^-1 R | TESTED, FAIL (DR4 552b98907e, TM2 c5bae4c406) | no |
| I10 | condensate coherence length set by rho_DE | TESTED, FAIL (X57 M4 436ff03cb9) | no |

Ten ideas: four TESTED, two PARTLY TESTED, four UNTESTED as stated (I1, I5, I6, I7). I1 counts as untested even though X67
and KT30 tested its neighbours.

## Gate 1 on I1: can any non-decreasing weight F(zeta) give X-COP its dust and SPARC none?
zeta_c is the 5th percentile of zeta over X-COP's 35 rows (7 clusters, 0.1 to 0.7 R500). The line, f_SP <= 0.046, comes from
SPARC's room under its rms line: (0.110^2 - 0.069^2) / 0.40^2. Here 0.40 dex is the smallest cluster-level dust (1.5 x the law).

| quantity | canonical | alt |
|---|---|---|
| X-COP zeta: min / zeta_c / median / max | 0.403 / 0.426 / 0.507 / 0.703 | same rows |
| SPARC g_b < a0, Y 0.5: points, galaxies | 2573, 173 | 2662, 173 |
| **f_SP, Y 0.5 / 0.3 / 0.7** | **0.425 / 0.461 / 0.394** | **0.425 / 0.458 / 0.393** |
| galaxies with a hit, Y 0.5 | 0.73 | 0.78 |
| SPARC median zeta, Y 0.5 | 0.337 | 0.338 |
| **G-SEP** | **DOES NOT SEPARATE** | **DOES NOT SEPARATE** |
| Reading B: thin-disc midplane zeta | 0.500, above zeta_c | same |
| G-BUL: zeta at BCG1, BCG3, main gas, bullet gas (point) | 0.856, 0.465, 0.920, 0.819 | same model |
| G-BUL label | WEIGHT ALLOWED AT GALAXIES | same |
| G-Q2: zeta at Saturn | 4.2e-14, INHERITS (Q2 rests on v3s's L*) | same |
| G-KEYS | NOT COMPUTED (gas profiles sit inside X30's drivers) | same |

**Lane label: I1 KILLED AT GATE 1.** Every check passes, so the label is clean.

What it means: X-COP's baryon mass still grows as r^1.2 to r^2.1 out to 0.7 R500. Many SPARC galaxies, gas-rich ones most of
all, have a baryonic curve that is still rising where g_b < a0, so their zeta is just as high. No threshold in zeta can switch the dust
on in clusters and off in those discs. Reading B is worse: a thin disc's own midplane gives zeta = 1/2, the same KT30 lesson
in a new role. The Bullet and Q2 readings pass, but they don't rescue a selector that fails on SPARC.

### Post-result diagnostics, no label (`fa1_diag.out`)
The fail is not noise and not a threshold artefact. These are canonical numbers; alt agrees within 0.003.
- Smoothing V_b^2 (3-point running mean): f_SP 0.432.
- Stricter thresholds: f_SP 0.340 at the X-COP median and 0.150 at the X-COP maximum (0.703). Both are still above 0.046.
- Outer third of each curve only: 0.195 at zeta_c and 0.055 at the X-COP maximum.
- Gas-dominated points are worse (0.49) than star-dominated ones (0.41), as Phase 1 predicted.

## Checks
- K0: with F = 0 the candidate equals the law to 0 relative difference, on both footings.
- K1: the Plummer-Hessian zeta matches the analytic (dlnM/dlnr)/3 to 2e-16. A uniform sphere gives 1, rho ~ r^-2 gives 1/3
  and a far point mass gives 1e-12.
- MUTATE, SPARC zeta x 0.1: f_SP becomes 0.000 and G-SEP reads SEPARATES on both footings, so the gate bites.
- Rerun: `fa1_results.json` is byte-identical across two runs.
- Compute: 58 MB RSS, under 1 s, one thread.

## What is not done
- No action was found, and nothing here is one.
- I1's weight switch on a gravitating component is not a standard field-theory object. Gate 1 tests a necessary condition
  only.
- I2 and I6 were run on 11-04 (owner: "Yes, run both"); see `I2_vorticity/README.md` and `I6_galileon/README.md`. Both
  are killed; neither reopens the cold sector.
- `fa1_results.json` stores X-COP `r_kpc` 1000x too large (R500 is already in kpc). zeta is a log slope, so the I1 result is
  unaffected; found by I6, fixed there.
- The keys were not wired at the selector level.
- The record's bigger walls still stand for any successor: X22's capture of forest-passing dust by galaxies, the mu-pincer
  and Theorem G (X57).

kappa = 1/2 FITTED; not theory closed.
