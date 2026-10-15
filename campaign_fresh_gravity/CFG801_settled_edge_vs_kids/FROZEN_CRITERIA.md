# CFG801 FROZEN CRITERIA: does KiDS lensing show the settled-halo break at 5.84 r_M (ARGON02 kill test b)? (committed before any script)

**Prediction under test.** ARGON02 (f02494fda), its kill test (b). The settled cold halo has the exact law profile
M_c(r) = M_b(√(1+4r²/r_M²) − 1)/2, truncated at the supply edge r_e = 5.843 r_M, where M_c = 5.364 M_b. Here
r_M = √(G M_b/a₀) and a₀ = 9.3603e-11 (canonical; alt reported separately, never pooled). ESD = baryon point mass
+ projected settled halo.

**Rival (same law, no edge).** The same profile continued to infinity (deep SIS), i.e. no supply edge.

**Data.** Brouwer et al. 2021 (KiDS-1000), Fig. 3 "lensing rotation curves" of isolated galaxies:
- 4 stellar-mass bins, log M* = [8.5, 10.3, 10.6, 10.8, 11.0];
- 15 radii, 0.035–2.6 Mpc;
- the full 60×60 covariance;
- bias-corrected exactly as the README says.

Already in the repo (real_research/data/lensing_rar). Raw survey product; no ΛCDM model is used.

**Radius ranges.**
- **Primary:** R ≤ 0.31 Mpc (8 radii per bin), where B21 consider the isolated sample clean.
- **Secondary:** all 15 radii. Two-halo contamination grows outward and biases this range AGAINST the break
  (disclosed direction).

**Statistic.** χ² with the full covariance, summed over the 4 bins. Two versions:
- **(P) shape test:** M_b profiled per bin (one free normalisation per bin, applied identically to both models; grid
  log M_b 9–12).
- **(Z) zero-knob:** M_b = M* at provisional bin means log M* = 10.14, 10.46, 10.70, 10.89 (quoted from memory),
  with no gas.

Δχ² = χ²(edge) − χ²(no edge).

**Classes** (primary range, version P decides; Z reported):
- **EDGE EXCLUDED** if Δχ² ≥ 9.
- **EDGE FAVOURED** if Δχ² ≤ −9.
- **UNDECIDED** otherwise.

Also report each model's absolute χ² and p.

**What it means.**
- If EXCLUDED, the settled-only halo dies as the full lensing mass; the outer mass must then come from S4 free
  debris (or a different supply rule), and ARGON02 kill test (b) has fired on public data.
- If FAVOURED, it is a new positive lensing signature.

**Controls.**
- K1: r_e/r_M = 5.843 ± 1e-3.
- K2: the no-edge ESD at 20 r_M equals the ARGON02 locked deep value σ²/(2GR) × 0.969 within 1%.
- K3: the B21 velocity conversion reproduces their Eq. 23 on one row.
- MUTATE (separate outputs): replace the data by the edge model plus covariance noise (seed 801); it must give
  EDGE FAVOURED.

**Not tested:** S4 free-debris profiles (not specified in the record). Merger-free disks (B21 has no clean
disk-only radius-binned file; colour bins are RAR-format).

κ fitted; not theory closed.
