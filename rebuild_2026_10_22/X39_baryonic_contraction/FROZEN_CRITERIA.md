# X39_baryonic_contraction — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X38 (9cc80516df / f72216ad98, reproduced by the coordinator) found that route-E cold dark energy halos,
Burkert-cored at ρ₀r₀ = a₀/(2πG), pass SPARC and the cluster OUTER bands. They fail only the heaviest cluster cores, which
come out too wide and too light at 0.3–1 Mpc. Does **baryonic contraction** (gravity only, no new constant) supply the
missing core mass in massive clusters, while keeping SPARC's pass?

**The hypothesis (SD + AC).**
- The cold dark energy halo is born with X38's a₀-pinned core: Burkert, ρ₀r₀ = Σ_a₀ = 107 (canonical) / 129 (alt) M☉ pc⁻².
- Baryons start distributed like the halo, then settle into their observed profiles.
- The collisionless cold dark energy responds adiabatically.
- Standing rules: κ = ½ FITTED. Footings never pooled. Raw data, framework-native. Cold dark energy is not matter. Not
  "theory closed". Nothing here may say the data favour the framework.

## 1. Contraction models

- **PRIMARY: Blumenthal et al. (1986) adiabatic contraction.** For each initial shell r_i:
  r_f [M_b(r_f) + M_cde,0(r_i)] = r_i M_cde,0(r_i)(1 + F).
  - F = M_b,tot / M_cde,tot (inside r_ta for clusters, inside R200 for galaxies).
  - Solved by fixed-point iteration (100 steps; convergence printed). Shells are not allowed to cross.
- **REPORTED: Gnedin et al. (2004) modified contraction.** The same equation with masses evaluated at
  r̄ = A r_vir (r / r_vir)^w, A = 0.85, w = 0.8.
  - Those constants are calibrated on ΛCDM simulations, so this is EXTERNALLY CALIBRATED and carries no verdict weight.
  - r_vir = R200 for galaxies and r_ta for clusters.

## 2. Inputs

- **Clusters:** X30's machinery executed read-only, as in X38.
  - Baryons = X30's M_b (β-model gas × 1.2), plus a BCG.
  - BCG: Hernquist profile with mass = CFG922 `cfg922_census_A1.json` `bcg_med`, matched per cluster exactly as X21 does
    (CFG687 positions within 5″ and Δz < 1e-3). Clusters with no measured BCG take the median measured BCG of their
    MGAS500 tercile (count reported).
  - Hernquist scale a = 10 kpc (frozen; R_e ≈ 18 kpc). a = 5 and 20 kpc are reported.
  - Disclosed: X30's ×1.2 stellar term already spreads some stars like the gas, so adding the BCG may double-count part
    of it. That favours contraction. The variant without the BCG is reported.
- **SPARC:** EM1's machinery, read-only, as in X38. M200 from EM1's relation (borrowed).
  - Baryons at each Υ: M_b(<R_k) = max(0, g_bar R_k²/G) at the measured radii, made monotone.
  - M_b ∝ r² inside the first radius.
  - Beyond R_last: a log-linear rise to M_b,tot(Υ) = (Υ L₃.₆ + 1.33 M_HI) × 10⁹ M☉ (or M_b(<R_last) if larger) at
    3 R_last, constant after.
  - Disclosed: spherical approximation of the disc.
- **Groups:** no group profile machinery is reachable here, so groups are NOT graded (named, not done).

## 3. Prediction and grading

- Gravity is Newtonian on M_b + M_cde,f, with no law, as in X38.
- **Clusters:** X30's keys and |Z| ≤ 2 in both h cells (KT 106 and all 326), with X38's grading code.
- **SPARC:** EM1's line (rms ≤ 0.110, median Υ 0.50–0.80), both backgrounds.

## 4. Verdict (per footing; the class needs both footings to agree)

- **SD + AC PASSES** — the SPARC line passes on both backgrounds AND every cluster key passes.
- **SD + AC PASSES SPARC ONLY** / **CLUSTERS ONLY** / **FAILS** — as in X38, with the failing keys and legs listed.
- Reported: X38 vs SD + AC per key (did contraction move MID T3 and the KT slope, and by how much); the variants (Gnedin,
  no BCG, a = 5 / 20 kpc); the contracted r₀,eff (radius enclosing half of M_cde inside 0.5 Mpc) per KT tercile; the SPARC
  Υ shift.

## 5. Checks (all must pass; `--mutate` must fail K1)

- **K0:** X38's SD numbers are reproduced with contraction switched off: SPARC rms 0.0795 / 0.0729 and cluster OUTER
  all-KT pred 0.697 / 0.663 (h 0.672), to 1e-4.
- **K1:** Blumenthal limits.
  - With M_b ≡ 0 and F = 0, r_f = r_i exactly.
  - For a point-mass baryon test case, the closed-form solution is reproduced to 1e-6.
  - Contraction conserves M_cde inside the shell mapping (1e-10).
- **K2:** the CFG922 BCG match count equals X21's printed "BCG>0" count.
- **K3:** peak RSS < 2 GB; one thread; minutes.
- **MUTATE:** the contraction equation uses (1 − F) in place of (1 + F); K1's point-mass test must fail.
