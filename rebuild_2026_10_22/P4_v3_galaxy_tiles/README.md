# P4_v3_galaxy_tiles: the five galaxy tiles recomputed for v3

## Verdict: CRISP FINDING. Under v3, two galaxy tiles turn red, one goes conditional, two hold

v3 here means its static weak-field limit on baryons only:
- AQUAL with μ = x/(1+x) exactly;
- the external field solved as a boundary condition;
- screening at L★ = 24 and 90 pc (D10's stiffened form);
- no settling, supply, catchment, edge or round rules;
- both footings, never pooled.

κ = ½ is FITTED. This is not "theory closed", and nothing here says the data favour the framework.

| tile | old | v3 | class |
|---|---|---|---|
| Rotation curves (SPARC RAR) | PASS: 0.101 / 0.099 dex, one global Υ (CFG695) | rms **0.054 / 0.054 dex**, one Υ per galaxy; median Υ **0.52 / 0.44** | **COND**: canonical passes, alt misses the frozen Υ window (0.44 < 0.50). The χ² line FAILS on both footings |
| Local a₀ from MeerKAT | PASS: 1.05e-10 (OBS) / 1.31e-10 (REST) | **1.31e-10** (REST; 95 % 1.23–1.65e-10) against SPARC's same recipe, 1.21e-10: **+0.033 dex** | **PASS** (ROBUST) |
| Galaxy groups (BFJR) | PASS: "consistent supply closes" (CFG543) | law on baryons, isolated: **+0.010 / −0.010 dex**, Z ±0.31 | **PASS** as frozen (isolated). Sensitive to the external field: ABOVE LAW at g_e = 0.03 a₀ |
| MW vertical force | PASS: round rule beats the phantom disc 32/32 (CFG516) | AQUAL disc: K_z,1.1(R₀) **92.3 / 96.9** against 66.4 ± 2.2; χ² **178 / 251** against a line of 67.5 | **FAIL** (ROBUST) |
| Tidal dwarfs, DF2/DF4 | COND: Newtonian if they captured no cold energy (CFG936) | with the host field solved, the data sit **−0.59 / −0.62 dex** (TDGs) and **−1.66 / −1.74 ln** (DF2/DF4) below v3 | **FAIL** (ROBUST) |

Values are canonical / alt at L★ = 24 pc; 90 pc is the same to within the digits shown unless noted. Every number below is
in `p4_v3_galaxy_tiles_results.json`.

## Why each tile moved

**T1. Rotation curves (PASS → COND).**
- The law's shape is unchanged: CFG695 already used g_N = g²/(g + a₀) algebraically, and that is exact AQUAL for a sphere.
- Fitting one Υ per galaxy lowers the rms from 0.101 / 0.099 to 0.054 / 0.054 dex.
- On the alt footing, the higher a₀ makes the per-galaxy fits prefer lighter discs. The median Υ is 0.44 (16–84 %: 0.30–0.93),
  below the frozen window of 0.50–0.80.
- The external field and screening barely matter:
  - Chae's environments give g_e = 0.034–0.060 a₀ (10–90 %, canonical);
  - solving it changes the rms by < 0.001 dex;
  - the maxclu / noclu brackets give 0.0538 / 0.0540;
  - L★ = 90 pc changes it by < 0.0002.
- **χ² line (frozen from SPARC's eV, distance and inclination errors): FAIL on both footings.**
  - Only 63–64 % of galaxies have p ≥ 0.001; the line asks for ≥ 90 %. χ²/dof is 4.93 / 4.77.
  - The record's kernel ν_mono, given the same freedom, does the same: 64 % / 63 %, χ²/dof 4.83 / 4.70.
  - So the failure is the error budget, or non-circular motions, against any law of this family. It is not specific to v3.
- **Reading disclosed.** The criteria say Υ is "chosen by minimising the galaxy's χ²", and the χ² bullet then says "Υ refit
  by this χ²". The script reads this as follows:
  - the rms fit uses the eV-only χ² (the CFG4 weights);
  - the χ² line refits with the covariance.

  The other reading takes Υ from the covariance χ². It gives rms 0.168 / 0.148 with median Υ 0.55 / 0.50, so the rms line
  FAILS. That rms ignores the distance and inclination offsets that chose Υ, so it is not a meaningful scatter.
- The Chae lognormal Υ prior gives 0.0540 / 0.0535 at median Υ 0.52 / 0.46, so the class is unchanged. Q ≤ 2 gives
  0.053 / 0.052 at 0.54 / 0.46.
- "No rotator has an excess" still holds. At the old global Υ, SPARC small and large galaxies sit at −0.046 ± 0.027 and
  −0.047 ± 0.015 dex (canonical), slightly below v3.
- **Geometry (D1, no class weight).** A thin-disc AQUAL solve against the spherical approximation, for exponential discs:
  - the median in-plane shift is −0.002 to −0.006 dex;
  - at R = 0.5 R_d it reaches −0.10 dex for the lowest surface densities (Σ₀ = 0.3 Σ_M).

  An AQUAL disc solve of every SPARC galaxy (batch R3) has not been done.

**T2. MeerKAT a₀ (PASS → PASS).**
- All 47 survivors are deep, so ν₁ and ν_mono differ by −0.001 dex in a₀.
- Under v3 the REST-frame a₀ is 1.308e-10; the SPARC same-recipe value is 1.214e-10. Δ = +0.033 dex, against a line of 0.15.
- Offsets from the footings are +0.145 dex (canonical) and +0.063 dex (alt).
- The OBS frame gives 1.043e-10 (−0.066 dex), which also passes.
- Screening changes g at R by ≤ 5e-5.
- There is no environment estimate on disk for these galaxies, so they are treated as isolated.

**T3. Groups (PASS → PASS, isolated).**
- The old pass needed CFG543's consistent-supply edge. v3 has no edge, and the law on the catalogue baryons alone already sits
  on the groups: +0.010 / −0.010 dex, Z +0.31 / −0.31.
- This equals CFG540's no-edge row. The groups are deep and are scored with a whole-system aperture, so ν₁ and ν_mono agree to
  1e-5 dex.
- Variants (aperture R < Re; Re/k for k = 1.13–2.77) all stay CONSISTENT. Screening changes σ by < 1e-6.
- **Caveat: v3 has an external-field effect, and the groups' field is not on disk.**
  - Solved at g_e = 0.01 a₀, the groups sit at +0.063 / +0.047 dex (Z 1.94 / 1.46, still CONSISTENT).
  - At g_e = 0.03 a₀ they sit at +0.151 / +0.143 dex (Z 4.7 / 4.5, ABOVE LAW).
  - SPARC galaxies' environments correspond to 0.03–0.06 a₀.
  - So the pass holds only if the groups' external field is ≲ 0.01 a₀.

**T4. MW vertical force (PASS → FAIL).**
- The old pass came from the round enclosed-mass rule, which v3 does not contain.
- v3's AQUAL phantom is disc-like, like the QUMOND phantom disc (CFG516's PD: 90.0 / 94.8, χ² 145 / 210).
- On McMillan17, F0 gives K_z,1.1(R₀) = 92.3 / 96.9 M☉/pc² against 66.4 ± 2.2. χ² over the 43 MAPs is 178.4 / 250.7, against
  the line χ²₀.₉₉(43) = 67.5. The K_z scale length is 3.84 / 3.90 kpc, against the data's 2.72.
- v_c(R₀) is low at 215 / 220 km/s. Fitting the amplitude to Eilers (FA: A = 1.19 / 1.10) raises K_z to 105 / 104, χ² 446 / 398.
- Every baryon model fails, F0 and FA:
  - B2: χ² 148 / 213;
  - B2b: 431 / 560;
  - B3: 333 / 435, with FA 216 / 186.
- Screening (≤ 0.2 in χ²) and a 0.03 a₀ external field along the axis (≤ 0.4) change nothing.
- This lane's NFW comparator (Newtonian B1 + NFW fitted to Eilers) has χ² 43.6 and K_z(R₀) 76.7. It is a comparator only, not a
  verdict input.

**T5. Tidal dwarfs and DF2/DF4 (COND → FAIL).**
- v3 has no capture rule, so the law acts on all baryons, and the only way below it is the host's field.
- Solved in AQUAL, that field removes little of the deficit:
  - **TDGs**: r̄ = −0.587 ± 0.110 dex (p 1.6e-6) canonical and −0.623 ± 0.110 alt. The isolated law gives −0.691 / −0.728,
    Newton +0.055;
  - **DF2/DF4**: r̄ = −1.657 ± 0.480 ln (p 0.002) and −1.742. The law gives −1.940 / −2.028. The predicted σ is 17.0 / 16.5 km/s
    against the observed 8.5 and 6.3.
- Host fields are g_e = 0.16–0.28 a₀ (TDGs) and 0.17 / 0.16 a₀ (DF2 / DF4).
- Every frozen variant FAILS: Plummer profile, orientation brackets, host mass ×½ and ×2, scalar-sum field, the host-mass
  corners, and virial σ.
- **Why the record's EFE number differs.** CFG936's EFE contrast (−0.38 dex for the TDGs) used the 1-D formula (FM12 eq. 60).
  In the field-dominated limit that formula gives B = 1/(μ_e(1+L_e)). The solved AQUAL field is 1/μ_e along ê and
  1/(μ_e√(1+L_e)) across it; K2 checks this to 0.7 %. So the 1-D recipe over-suppresses, and v3's solved EFE is weaker.

## What this does not include or show

- **BS24 Eq. 35's μ_K²ψ term** (N0 audit item 2) is not included in any tile. Batch R6 owns it, and it could matter beyond
  about 0.1 Mpc (groups).
- **SPARC is in the spherical approximation.** Disc geometry is diagnosed only (D1). The groups' and MeerKAT galaxies' external
  fields are unknown.
- **The MW baryon models are partly halo-fitted** (McMillan17). B2, B2b and B3 bracket this, and all of them fail.
- **TDG discs have turned less than one orbit** (Lelli), and every estimator here assumes equilibrium.
- The input ledger (RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY) is §3 of
  `FROZEN_CRITERIA.md`.

## Checks: 11/11 PASS (exit 0, 594 s, one thread, peak RSS 0.76 GB)

| check | result |
|---|---|
| K1 isolated AQUAL vs the exact law | 3.4e-3 |
| K2 linear EFE vs the quasi-Newtonian solution | 7.4e-3 |
| K3 grid convergence | 1.7e-3 dex (SPARC 3.9e-4) |
| K4 vs D10's independent screened solver | 5.4e-4 |
| K5 | CFG695 reproduced exactly; loader bit-for-bit |
| K6 | CFG301 / CFG309 / CC2 exact |
| K7 | CFG540 no-edge means to 1e-9 |
| K8 | MW mass 3.5e-5; Newtonian K_z vs ring quadrature 1.7e-3; far field 1.7e-2; NFW χ² 43.62 vs CFG514's 43.70 |
| K9 | CFG936 / CFG933 exact |
| K10 | 109/109 environments matched |
| K11 | peak RSS 0.76 GB |

`--mutate` swaps μ for x/√(1+x²): K1, K2 and K4 FAIL (0/3, exit 1).

**Amendments A1–A4 (post-result, numerics only; no line, threshold or input changed):**
- **A1:** K8's column clause omits the radial-force term (12 %; CFG514 K3b fails it too) and is replaced by a ring quadrature.
- **A2:** predictions are the exact isolated law × the solver's ratio on one grid.
- **A3:** the solver uses the internal potential with exact external face fluxes, and |g_N| in the Newton start.
- **A4:** a radial face is aligned on the evaluation radius, and T5 runs at 40 cells per decade.

## Run

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py            # ~10 min
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py --mutate   # ~10 s, exit 1
```

**Inputs.** All are read only. Tian+2026 is read from `../_external_data/vizier2026/`, outside git. Nothing was downloaded.

**Criteria and amendments:** 6c5e6161b9 (criteria); 10305328f4 (A1–A3); 294c5b08cc (A4).
