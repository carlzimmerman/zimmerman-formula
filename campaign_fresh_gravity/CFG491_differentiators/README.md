# CFG491: where does the framework differ from BOTH ΛCDM and standard MOND? Differentiator matrix + the on-disk three-way test

**Bottom line.** Candidate B is a hybrid by construction. It behaves like **ΛCDM** wherever the matter content or the external-field effect decides (wide binaries, cluster satellites, voids, growth, clusters), and like **MOND** wherever the arrangement inside a galaxy decides (RAR shape and tightness, BTFR, isolated dwarfs). Only three kinds of observable separate it from both at once:
1. the **lensing edge**: where the isothermal phantom stops, and how that radius scales with mass and environment;
2. the **conjunction "no EFE and a tight RAR"**, read off one rotation-curve sample;
3. **a₀(z) tracking an evolving ρ_DE**, which is distinct only if w ≠ −1, and by ≤ 0.1 dex.

The on-disk version of (2) was run with frozen criteria. Verdict: **NOT SINGLED OUT (LOW POWER)** on both footings, and its MUTATE was **not detected**, so the test cannot separate the framework from MOND with SPARC. No test on disk discriminates all three; the data needed for (1), the best one, are listed below and need the owner's go.

Criteria are in `FROZEN_CRITERIA.md`, committed alone first (788eeec2c). κ = ½ is FITTED: one input, fixed on SPARC. Both footings are reported and never pooled. The cold mass is still required, and no dark-matter particle is added. Nothing here says the data favour the framework.

## Step 1: the differentiator matrix

F is the framework (candidate B: the law inside bound halos, no EFE, cold fluid settled into the phantom and cut at r_edge = r_M/ln(1 + f_ret f_b/(1 − f_b))). L is ΛCDM. M is standard MOND (AQUAL/QUMOND with the EFE). Numbers come from committed lanes (IDs given) or from `cfg491_matrix_numbers.py` (marked †). Inputs marked (U) are recalled, not read from disk.

| # | observable | F (framework) | L (ΛCDM) | M (MOND + EFE) | F differs from | size vs errors | data on disk | F parameter-free? |
|---|---|---|---|---|---|---|---|---|
| 1 | **Isolated-lens ΔΣ edge (truncation radius vs M_b, environment)** | Isothermal to r_edge, then point mass. r_edge = 5.85 r_M at f_ret = 1; 0.26 / 0.72 Mpc at log M★ 10 / 11 for f_ret = 0.1†. d log r/d log M_b = 0.50 at fixed f_ret, **1.18 at ΛCDM-equal retention**†. Independent of environment and accretion rate | Splashback ≈ 0.95–1.36 R200m (More+15, U): 0.20–0.28 / 0.63–0.91 Mpc at log M★ 10 / 11†. Slope 0.56†. Depends on accretion rate Γ | No edge in isolation (ΔΣ ∝ 1/R). EFE turns the field Newtonian-like beyond r_M/e: 0.10–0.24 / 0.27–0.67 Mpc for e = 0.05–0.02†. Slope 0.5; scales with 1/e (environment) | **L and M** | At ΛCDM-equal retention r_edge/R_sp runs from ~0.35 (log M★ 10) to ~3 (log M★ 11.3)†: a factor ~10 across the mass range. Current stacks cannot read it: two-halo template-dependent (CFG413/486) | KiDS-1000 (Brouwer+21), DESI DR1 lensing: **Y, but not decisive** | **No**: f_ret is a postulate (CFG461/462/488/490) unless taken from a census |
| 2 | **No-EFE AND tight RAR on one sample (this lane's test)** | β = 0, S2 ≈ 0.10 dex (noise + M/L) | DMO: β = 0, S2 0.19–0.20 (CFG476 0.205). Feedback ΛCDM: no parameter-free number | β ≈ +1 (mock +0.95…+1.17), S2 0.11 | DMO-L and M (conjunction only) | Separates F/M from DMO-L (power 75–85%), but **not F from M (18–20%)** | SPARC + Chae+21 e_N: **Y** | Yes (κ fitted) |
| 3 | a₀(z) under DESI evolving DE | Δlog a₀ = +0.014…+0.037 at z 0.5; **−0.08…−0.11 dex at z 2.5** (DESI DR2 w₀w_a chains)† | No a₀. DMO-emergent scale 3.9e-10 at z 0 (CFG476); feedback sims not crisp | 0 (flat) | M only if w ≠ −1 (identical to M at w = −1); L not crisp | ~0.1 dex against a ≥ 0.3 dex/galaxy calibration wall (PAPER38, CFG213–229). The a₀ ∝ H(z) rival is at +0.58 dex† | z ≲ 2.5 compilations: Y, calibration-limited | Yes, given DESI w(z) |
| 4 | Old tidal dwarfs | Settling branch: Newtonian (= L). Fork branch (CFG391): isolated law | Newtonian | Law + EFE | Only on the fork branch | NGC 5557-E1 forecast: Newton 16–24, law+EFE 28–41, isolated law 45–58 km/s (CFG441) | **N** (no old TDG has kinematics; CFG441/448) | Yes |
| 5 | Wide binaries (Gaia) | Newtonian, γ = 1.000 (Amdt 21, Arm C) | Newtonian | Arm A ν_RAR floor 1.161/1.192; P2 merge 1.063–1.127 | **M only** (F = L) | EFE-blind force excluded by DR3 at 7.7σ (CFG447). DR3 γ̂ 1.075 ± 0.055 against Newton-through-pipeline 1.016–1.020 | DR3 Y; **DR4 2 Dec 2026** (prereg frozen) | Yes |
| 6 | Satellites in host fields | Isolated law: cluster satellites χ² 0.7, +0.01 dex (PAPER44). Dwarfs: M31 LVD +0.116, MW UFD +0.355 dex low (h43) | Fits Sifón (it is their model); accommodates dwarfs | EFE: χ² 99.7, +0.81 dex; M31 LVD +0.381, MW UFD +0.825 | M only | Large (Δχ² ~ 99) | Y | Yes |
| 7 | Directional (aligned) EFE asymmetry | 0 | 0 | +1–4% | M only | +2.95 (n 16), −1.70 (n 25 WALLABY); detection vs null needs N ≥ 560 | Y (underpowered) | Yes |
| 8 | Outer-RC EFE amplitude (Chae) | 0 | 0 | Chae's e_N trend | M only | CFG8 weighted slope +0.57…+0.71 ± 0.25, Spearman p 0.57–0.87 | Y | Yes |
| 9 | RAR tightness alone | Zero intrinsic | DMO 0.205 vs data 0.099 (CFG476) | Zero intrinsic | DMO-L only | ×2 | Y | Yes |
| 10 | Growth / CMB lensing | σ₈ ×1.0037–1.0046, max\|P−1\| 0.033–0.040 (CFG424–439, CFG460) | 1 | Without cold mass: growth ×7, excluded | M only (F ≈ L) | Few % at k ~ 1–10 h/Mpc, below the baryonic-feedback uncertainty | Y (own PM) | Zero-knob fix; amount of cold fluid input |
| 11 | Clusters (incl. Bullet) | Needs the cold fluid | Needs CDM | Short by ~×2 | M only | Large | Y | Cold amount = input |
| 12 | Voids / cosmic web | Law off outside bound halos: growth = L (CFG324, Planck lensing 1.000) | — | Boosted void outflows | M only | — | partial | Yes |
| 13 | Isolated field dwarfs | Law (centring Υ_V 1.3, scatter 0.128 dex; h43) | Accommodates (diversity) | Law | DMO-L only | — | Y | Yes |
| 14 | BTFR zero point vs z | = row 3 | — | flat | as row 3 | as row 3 | as row 3 | as row 3 |

**Where F simply agrees with someone (not distinctive):**
- With **L** on rows 5–8 and 10–12. Every EFE test and every test set by the cosmic amount of matter cannot single the framework out from ΛCDM.
- With **M** on rows 9, 13 and 3 (if w = −1). Every test of the arrangement inside a galaxy cannot single it out from MOND.

**Ranking (discriminating power against BOTH × readiness):**

| rank | test | why it ranks here |
|---|---|---|
| 1 | Lensing edge scaling (row 1) | The only observable where all three models give different numbers, by a factor of 2–3 in radius at the ends of the mass range and up to ×10 in r_edge/R_sp. Not ready: the two-halo term, isolation completeness, and f_ret is not parameter-free. |
| 2 | No-EFE + tight-RAR conjunction (row 2) | On disk and parameter-free. Run here: low power against MOND, and the ΛCDM side is DMO-only. |
| 3 | Gaia DR4 wide binaries (row 5) | The strongest and most ready test, but F = L there, so it can only separate F (and L) from MOND. |
| 4 | a₀(z) tracking DESI w(z) (row 3) | Parameter-free, but ~0.1 dex against a 0.3 dex wall; identical to MOND if w = −1. |
| 5 | Old tidal dwarfs (row 4) | Distinct from both only on the fork branch. No data exist. |

## Step 2: the on-disk three-way test (frozen; `cfg491_threeway.py`)

**Sample:** 91 SPARC galaxies (Q ≤ 2, Inc ≥ 30°, with a Chae+21 environmental field); 89/90 enter the EFE statistic.

**Statistics:**
- **S1, the EFE slope β:** the partial coefficient of the per-galaxy EFE template D_i in R_i ~ 1 + D_i + X_i. Here R_i is the mean residual about the isolated law at x < 1, and X_i is the mean log x.
- **S2:** CFG476's RAR rms.

**Mocks:** all three models go through one estimator and one nuisance model (Υ, gas, distance, inclination, e_N errors, V noise), 300 mocks per model per footing.

| footing | data β (bootstrap σ) | data S2 | F: β / S2 median, p_β, p_S2 | L (DMO): β / S2, p_β, p_S2 | M (ν_RAR @1.2e-10 + EFE): β / S2, p_β, p_S2 | P_single | verdict |
|---|---|---|---|---|---|---|---|
| canonical | **+2.30 (1.06)** | 0.1094 | +0.01 / 0.104, **0.087**, 0.80 → consistent | −0.22 / 0.198, 0.073, **0.013** → inconsistent | +1.17 / 0.110, 0.38, 0.96 → consistent | 0.083 | **NOT SINGLED OUT (LOW POWER)** |
| alt | **+2.21 (1.03)** | 0.1094 | −0.24 / 0.102, **0.087**, 0.78 → consistent | −0.33 / 0.193, **0.013**, **0.003** → inconsistent | +0.95 / 0.109, 0.36, 1.00 → consistent | 0.113 | **NOT SINGLED OUT (LOW POWER)** |

M_same, the EFE with the framework's own kernel and footing (reported only), is consistent on both footings (β +0.98 / +0.96).

**Reading:**
- **DMO-ΛCDM is inconsistent** through the RAR's tightness, as CFG476 found. This does not test feedback ΛCDM.
- **The framework and standard MOND are both consistent.** With SPARC and Chae's e_N the EFE statistic cannot tell them apart: the F–M separation is 0.9 F-mock σ, and F pseudo-data reject M only 18–20% of the time.
- **Against interest:** the data β is on the EFE side. It lies +1.83σ from F's median (p_β 0.087, just above the 0.05 line) and +0.8–0.9σ from M's, at about twice MOND's amplitude. This matches CFG8 and PAPER44 (Chae's signal under this law, 1.7–3.0σ). It is a lean, not a detection, and it is reported as a strain on the no-EFE reading.
- **POST HOC (`cfg491_posthoc_loo.py`, not in the criteria):**
  - The leave-one-out range is +1.72…+2.62 (canonical) and +1.63…+2.52 (alt); the most influential galaxy is UGC07577.
  - Without the X_i covariate β is +1.28 / +1.36.
  - Spearman(D_i, R_i) gives ρ +0.15 / +0.18, p 0.17 / 0.09.
  - So the lean is not one galaxy, but it is weak.

**Controls:**
- K1: S2 on CFG476's sample is 0.0994. PASS.
- K2: the EFE kernel reduces to the bare kernel at e → 0, to 3e-11. PASS.
- K3: F(F⁻¹(e)) = e to 8e-9. PASS.
- K4: the DMO generator with V noise only gives 0.1986 against 0.205. PASS.
- **MUTATE (data := one standard-MOND + EFE realisation): NOT DETECTED.** β̂ = +1.60 / +1.71 leaves F consistent (p_β 0.19 / 0.18). The frozen rule therefore records that **the test lacks teeth for F vs M**, which is consistent with P_single ≈ 0.1. The MUTATE run exits 0, as frozen for "not detected".

## What would decide it: the best test, and the data it needs (needs owner go)

**Lensing edge scaling (rank 1).** The statistic would be the radius where d ln ΔΣ/d ln R crosses −1.5 for isolated lenses, in ≥ 4 stellar-mass bins over log M★ 10–11.3, and its slope against M_b. The predictions:
- **F:** 0.50 at fixed f_ret (1.18 at ΛCDM-equal retention), with no environment dependence at fixed mass.
- **L:** 0.56, plus an accretion-rate dependence.
- **M:** no edge in isolation; the radius scales as r_M/e, so it shrinks in denser environments.

Data needed, none of it on disk in decisive form:
- DESI DR2 (or a later DR1-BGS release) spectroscopic isolated lenses with complete neighbour redshifts within 3 Mpc / 1000 km/s. CFG316 found DR1 isolation empty: 1,002 of 1,034 lenses have a neighbour.
- Source shapes from KiDS-Legacy, HSC-Y3, DES-Y6 or Euclid DR1 over the DESI footprint.
- A two-halo template for that isolation cut, computed from mocks before fitting: either the repo's own 512³ PM boxes or a public ΛCDM light-cone.
- An f_ret(M_b) from an independent baryon census (eROSITA/SZ hot-CGM stacks), so that F's edge is a prediction rather than a fit.

**For the rank-2 conjunction to gain power:** N ≳ 1,000–1,300 galaxies with resolved outer rotation curves and external-field amplitudes (h28: N ≈ 1,313 for 3σ at the predicted amplitude). The sources would be full WALLABY / MeerKAT kinematic releases. This needs the owner's go.

## Files

- `FROZEN_CRITERIA.md`: frozen first, 788eeec2c.
- `cfg491_threeway.py`, with outputs `cfg491_threeway.out` / `_results.json` (rc 0) and `cfg491_threeway_MUTATE.out` / `_MUTATE_results.json` (rc 0 = not detected). About 10 s each.
- `cfg491_posthoc_loo.py`, with output `cfg491_posthoc_loo_POSTHOC.out` / `_results.json`. Post hoc, labelled.
- `cfg491_matrix_numbers.py`, with output `.out` / `_results.json`: the edge radii, the scaling exponents and the DESI a₀(z) shifts. It reads the on-disk DESI DR2 chains (`../../../_external_data/desi_dr2_chains`, as CFG417 does).

Run from anywhere: `python3 campaign_fresh_gravity/CFG491_differentiators/cfg491_threeway.py` (and with `CFG491_MUTATE=1`). No downloads were made.
