# X80_core_convergence: frozen verdict UNDECIDED. Reported: the zoom "cores" are NFW cusps seen through the ε cut; without the cut, native η is ×1.22 over the SPARC limit

Criteria: `FROZEN_CRITERIA.md` (62ddc553d0), committed before any script or number. Script `x80_core_convergence.py`
execs X77's `fit()` unchanged (the file's text up to its K2 block). Outputs: `x80.out`, `x80_results.json`, `x80_MUTATE.out`.

## Frozen grade
- **K1** (exact smooth core a = 6 at x_c 0.01 / 0.03 / 0.1 → 5.999) **PASS**. **K2** (X77's a for M1e12_s1_ng64 reproduced exactly) **PASS**.
  **MUTATE** (halve the particles inside 2 r_conv): fitted a falls in 21/21 runs, **PASS**.
- **T1, same seed ng 48 → 64:** median s = +0.03 [68 % −0.13, +0.37]. **UNDECIDED.**
- **T2, analytic cusp:** at ng 64, |a/a_cusp − 1| ≤ 0.2 for **9/9 runs (NFW) and 9/9 (Einasto)**. Over all 21 runs at 1e12 the
  NFW ratio is 0.95–1.06. **"Zoom cores = cusp seen through the resolution cut."**
- **Combined: UNDECIDED** (T1 does not decide).

**T1 is a design error, mine.** X48 redraws the random field at each ng, so "the same seed" at ng 48 and ng 64 is a
different halo. T1's spread (−2.1 to +2.4) is realisation noise, not resolution. It could never have decided. The
verdict stays UNDECIDED as frozen.

## Reported (post-result, not graded): `x80_cusp_curve.py` → `x80_cusp_curve.out`
Every native halo is an NFW cusp of its own concentration. X77's η_native is therefore not a core property. It is a
function of two numbers: the halo's c, and where the fit starts (x_c = r_conv/r_vir). At ng 64, r_conv sits on the
3ε floor in 6/9 runs, with x_c ≈ 0.03 set by ε = 0.01 r_f, a numerical choice.

η of the smooth-core fit to an exact NFW:

| c | x_c 0.1 | 0.05 | 0.03 | 0.01 | 0.003 | 0.001 |
|---|---|---|---|---|---|---|
| 4 | 8.85 | 10.34 | 11.15 | 11.99 | 12.20 | 12.24 |
| 6 | 12.46 | 15.02 | 16.61 | 18.45 | 18.93 | 19.07 |
| **7.75 (ng 64 median)** | 15.74 | 19.28 | **21.69** | 24.80 | 25.74 | **25.94** |
| 9 | 18.19 | 22.43 | 25.46 | 29.59 | 30.97 | 31.33 |

- η converges as the cut is removed. The inner cusp carries little mass, so the fit saturates by x_c ≈ 0.003.
- Each ng 64 halo at its own c with the cut removed: **median η = 25.94 [68 % 23.89, 26.53]. That is ×1.22 over the
  SPARC Υ-floor limit of 21.2.** Only 3/9 halos are under it.
- At the halos' own cuts, the cusp model gives 21.69, close to X77's measured 20.83. X77's knife-edge pass at 1e12 is a
  property of the ε cut.
- Converged-limit equivalent: SPARC's 21.2 corresponds to an NFW c ≈ 6.4. The native median is 7.75.
- **A5 (ng 80) will not settle this.** ε is fixed at 0.01 r_f, so x_c stays pinned near 3ε ≈ 0.03 in most runs, and A5
  measures the same cut.
- **Direction of the remaining bias.** FP2 found several ng 64 halos with Power κ < 2 at r₋₂ (not relaxed). Relaxation
  lowers central density, so the true c, and hence η, is if anything higher.

## Reading
Cold collisionless collapse makes cusps, as expected. Route E's collapse branch, read off native halos at converged
resolution, is ×1.2 too dense for SPARC's Υ floor at 1e12. This supersedes the "native η inside the window" reading of
X77 at 1e12 (X77's measurement stands; only its interpretation at the resolution limit changes). It agrees with the
pre-read and X76 (native c_f fails SPARC) by an independent route that does not use the r₋₂ crossing.

So a core in bright galaxies cannot come from cold collapse alone. It needs a physical scale the collisionless zooms do
not contain, from the cold dark energy floor physics or from the baryons. Within route E as written, the canonical SPARC
pass rests on the external c_f = 4 (η 10.82).

Caveats:
- The Υ-floor limit 21.2 is the pre-read bracket (c_f ≈ 7), not a fresh grader run at the cusp-limit η.
- The smooth-core fit to a cusp is a proxy. The grader's shape is a core, and the native halo is not one.
- This covers 1e12 only. The cluster masses exist only at ng 48 until A4.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating
field component, never a particle.
