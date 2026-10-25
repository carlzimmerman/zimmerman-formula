# NU1_cluster_gap_sources — FROZEN CRITERIA (before any script or number)

Rules: `rebuild_2026_10_22/BRIEF.md` (and the briefs it names). Inputs and classes: `ASSUMPTION_LEDGER.md`.
κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. No dark-matter particle is adopted.
Never "theory closed"; never "the data favour the framework".

## Question

F1 (and X2/X7 on F1's measurement) find that the law, applied to the eRASS1 clusters' baryons, falls short of the raw-KiDS
stacked lensing in MID (0.5–1.2 Mpc): A_MID ≈ 1.68–1.85 canonical / 1.54–1.70 alt (F1), 1.64–1.68 / 1.50–1.55 at X2's C\*.
Can ordinary mass whose amount is bounded by independent data close it without a new fitted constant?

## Sources and their allowed maxima (fixed here; no scan)

N. **Massive neutrinos** (three active species, sourcing the AQUAL field like any mass).
- Masses: (N0) oscillation minimum, normal ordering, Σ = 0.0588 eV; (N0i) inverted, Σ = 0.0995 eV; (Nrec) the record's
  m₁ = ρ_Λ^{1/4} value Σ = 0.0613 eV (real_research/neutrino_desi_2026_10_06); (NK) KATRIN direct bound m_β < 0.45 eV (90 % CL),
  taken as three degenerate states, Σ = 1.35 eV — the **allowed maximum**. No cosmological (ΛCDM-fitted) Σ bound is used.
- Budget cap (infall / fair share): the clustered ν mass within 3 Mpc ≤ (Ω_ν/Ω_b) × M_b(< 3 Mpc), with Ω_ν h² = Σ/93.14 eV
  and Ω_b h² = 0.0222 (BBN deuterium; PROVISIONAL external fact). h cancels. Neutrinos and baryons fall in from the same
  Lagrangian region; the hot ν cannot be over-represented relative to the cold gas, so this is generous.
- Phase-space cap (Tremaine–Gunn, fine-grained): per flavour ν + ν̄ with f ≤ ½ per helicity state, so
  n_ν(r) ≤ (4π/3) (m v_esc(r) / h_P)³ per flavour, ρ_ν ≤ 3 m n_ν. v_esc(r)² = 2 ∫_r^{R_ta} g dr with the law's g of baryons
  plus neutrinos (iterated to convergence), R_ta = 5 Mpc primary; 3 and 10 Mpc reported.
- **Maximal profile** (graded): ρ_ν = ρ_TG(r) from the centre outward until the cumulative mass reaches the budget cap,
  zero beyond (most concentrated allowed, maximises the MID signal). Reported: ν tracing the baryons at the fair share
  (capped by TG).
- Sterile neutrino (reported only, a NEW constant, never adopted): the minimum m_s (TG, g f = 1) whose phase-space limit can
  hold the gap's needed mass profile inside 1 Mpc for the median cluster of each tercile, and the abundance Ω_s/Ω_b the gap
  needs (from the gas-tracing needed amount, solved on the C\* pipeline); with the independent constraints listed in words.

B. **Hidden baryons** (bounds from measurements on disk / in the record only).
- (B1) hot-gas normalisation: allowed max × 1.236 (the X-COP N = 5 median of M_gas,deep / M_gas,eRASS1, the largest
  population-level ratio in the record; ACCEPT N 51 median 1.034 (F1 C3d); CFG922 N 68 median 1.081). The per-cluster 84th
  percentile 1.50 (CFG922 ρ_84) is reported as an **extreme bracket**, not as an allowed population offset.
- (B2) stars incl. BCG, satellites and ICL: allowed max f* = 0.30 of the gas (F1 C4; 3 × the X-COP measured upper end
  M*/M_gas(<0.5 Mpc) = 0.104, CFG922). ICL has no table on disk; it is inside this ×3 margin (stated, not measured).
- (B3) cold atomic + molecular gas: a central point mass of 2e11 M☉ per cluster (CFG922's HI bracket upper end is
  0.75–1.9e11; molecular gas in BCGs is not on disk — the literature maximum of a few 1e10 M☉ is PROVISIONAL). Allowed max.
- (B4) clumping: C ≥ 1 lowers the X-ray gas mass (CFG922 2d) → adds 0 (wrong sign). (B5) non-thermal pressure / hydrostatic
  bias: the X-ray gas mass does not use hydrostatic equilibrium; the law uses the baryon mass, not M_HSE → adds 0 (CFG922 2c).
  (B6) gas beyond the X-ray aperture: F1/X2's shapes already extend the gas to 3 Mpc; more outer gas raises OUTER, not MID
  (X2 a3, F1 G2) → no extra allowance.

## Pipeline (read-only reuse) and statistic

- F1's functions and X2's model (C0 = F1 PRIMARY; C\* = X2's corrected baseline: CFG814 gas shape, EFE noclu, reduced shear),
  exec'd read-only from their source text, as X7 does; X2's replay npz (equal to F1's measurement) as the data.
- The added mass enters the AQUAL source (M_src) of each cluster; its own lensing is included through the law's total.
- Terciles in catalogue Mgas500 (X7/X2 edges 7.37e12, 1.73e13 M☉). Primary errors: **X7's CAL treatment** (X7 committed
  b1a2ffcb6b): A_CAL = A − leak, σ_CAL² = σ_STAT² + σ_sys², with σ_sys (leakage, cross-shear excess, R−R excess) taken from
  X7's JSON per tercile and per all-cluster stack and rescaled exactly by Σ W P_old / Σ W P_new (every term is a band sum over
  the same model denominator); σ_STAT = max(jackknife, bootstrap) recomputed on the new model with X7's bootstrap seeds.
  C0 with jackknife errors is reported.

## Reproduction checks (must pass before any graded number)

- K1: my C\* and C0 models with no added mass reproduce X7's per-tercile and all-cluster A (MID, OUTER) for all 4 cells
  (2 footings × h 0.672 / 0.686, boost convention) to ≤ 1e-6, and X7's σ_STAT to ≤ 1e-6.
- K2: my rescaled CAL machinery with no added mass returns X7's A_CAL, σ_CAL (trend 'sig') and Z_CAL to ≤ 1e-6.
- K3: an added component = λ × gas through my code equals X2's comp "GS" with the same λ to ≤ 1e-10 (one cell, all clusters).
- K4: Tremaine–Gunn unit test: a degenerate Fermi sphere in closed form (n = (4π/3)(p/h)³ per state pair) reproduces a
  numerical phase-space integral to ≤ 1e-6; and m = 2 eV, v = 2000 km s⁻¹ gives ρ within 1e-6 of the hand value.
- K5: the budget cap holds: the integrated ν mass ≤ cap (to 1e-9) for every cluster; ρ_ν ≤ ρ_TG at every radius.
- K6: a planted extra mass (gas × 1.5 tracing the gas) is recovered as A ratio = Σ W P_old / Σ W P_new exactly by the
  rescaling (≤ 1e-12).

Script prints `K# PASS|FAIL value threshold`, ends `NU1 COMPLETE: N/M checks PASS.`, exit 0 iff all pass; writes
`nu1_cluster_gap_sources.out`, `nu1_cluster_gap_sources_results.json`. `--mutate`: the neutrino density cap uses (v_esc)⁻³
instead of (v_esc)³ and K3/K6 feed a mis-scaled denominator (×1.1): K4 (or K5) and K6 must FAIL; outputs `*_MUTATE.*`.
Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes.

## Rows (each on both footings, both h ends, C\* graded, C0 reported)

R0 baseline (no added mass) · N0 / N0i / Nrec / NK maximal profile · NK tracing baryons · B1 · B1-extreme (×1.50, bracket) ·
B2 · B3 · **ALLOWED-MAX COMBINATION** = NK maximal + B1 + B2 + B3 (B4–B6 add 0) · EXTREME = NK + B1-extreme + B2 + B3 (bracket).

## Verdict rule (graded on C\*, X7 CAL errors; both footings must agree, else the weaker class)

Per cell: residual per tercile r_T = A_MID,CAL − 1 with Z_T = r_T / σ_CAL,T; all-cluster Z_MID.
**OUTER broken**: in the combination, the all-cluster Z_OUT,CAL ≤ −2, or any tercile with Z_OUT,CAL > −2 at R0 moves to ≤ −2.
- **CLOSED BY ALLOWED MASS**: the ALLOWED-MAX COMBINATION gives all-cluster Z_MID,CAL < 1 and every tercile Z_MID,CAL < 2 in
  all 4 cells, and OUTER is not broken.
- **PARTLY**: not CLOSED, but the ALLOWED-MAX COMBINATION removes ≥ 25 % of the all-cluster residual (A_MID,CAL − 1) in all
  4 cells (or would be CLOSED except that OUTER breaks).
- **NOT CLOSED**: anything else.
Reported, never graded: the EXTREME bracket, C0 rows, R_ta 3 / 10 Mpc, the sterile-neutrino requirement.

## AMENDMENTS (append-only)
