# S1_v3_hosted_small: v3's small systems in their host's field (N0 batch R1)

## Verdict

| tile | old | v3 | why it changed |
|---|---|---|---|
| 26 Dwarf satellites vs screened law | FAIL (+0.89 / +0.85 dex) | **FAIL** (+1.33 / +1.30 dex at L★ floor) | Same colour, larger gap. The host's external field (EFE) adds +0.58 / +0.57 dex. Native screening inside the field adds another +0.20 / +0.22 dex |
| 29 Coma ultra-diffuse galaxies | UNDEC (z +1.67 / +1.47 above the isolated law, with systematics) | **FAIL, ROBUST** (z_sys +4.3 / +4.1 at dmean, +4.7 / +4.5 at dproj) | The EFE of Coma's measured field. Isolated, the UDGs sit +0.33 dex above the law; in Coma's field they sit +1.12 dex above v3 |
| 19 Tidal dwarfs, DF2/DF4 | COND | not computed here (lane P4) | P4 has committed its frozen criteria and amendments (6c5e6161b9, 10305328f4) but no outputs yet |

κ = ½ is FITTED. Footings are canonical / alt (9.3603e-11 / 1.1312e-10 m/s²), never pooled. The extra mass is cold energy
(BS dust), not a particle. Not "theory closed". Nothing here says the data favour the framework.

- **What v3 is here:** its static equation, the stiffened AQUAL with μ = x/(1+x), solved for each system as a Plummer
  sphere sitting in a uniform total host field. The response is solved; no EFE recipe is used.
- **Solvers:** D10's solver (read-only), cross-checked against F2's independent AQUAL solver.
- **What is not in v3:** settling, supply, capture and ownership rules, and the P2 posit.
- **Checks: 10/10 PASS.** `--mutate` fails K3 and K4 as required (7/9, exit 1).

## Tile 26: the dwarf satellites (E3's 45 canonical / 46 alt systems)

**E3 did not use v3's external-field treatment.**
- E3 used ν₁ (v3's kernel), but with CFG691's isolated stiffness factor S(s), applied multiplicatively.
- It had no EFE.
- v3 puts every satellite in its host's field, where screening acts on the scale L★ itself (D10).

So the prediction was recomputed. The statistic is the bootstrap median over systems of log₁₀(g_obs/g_pred), ± its
bootstrap sd. The data side is E3's clean primary (Arroyo free-f binaries, Υ_V = 2) and the estimator is E-W.

| step (one change at a time) | canonical | alt |
|---|---|---|
| Newton (E3's g_bar) | +2.010 ± 0.113 | +2.000 ± 0.112 |
| S0 E3: CFG691 recipe, L★ 24 (reproduced; E3 +0.886 / +0.846) | +0.885 ± 0.127 | +0.842 ± 0.128 |
| S0 E3: unscreened law | +0.558 ± 0.099 | +0.506 ± 0.098 |
| S1 kernel ν₁ | no move (already E3's) | no move |
| S2 AQUAL solve, Plummer, isolated, L★ = 0 | +0.553 ± 0.099 | +0.502 ± 0.098 |
| S3 + EFE (host field E_mid) | +1.130 ± 0.154 | +1.075 ± 0.154 |
| **S4 v3 = + native screening, L★ floor (21.68 / 22.85 pc)** | **+1.331 ± 0.147 (9.0 sd)** | **+1.299 ± 0.147 (8.8 sd)** |
| S4 v3, L★ 24 pc | +1.355 ± 0.147 | +1.312 ± 0.147 |
| S4 v3, L★ 90 pc | +1.715 ± 0.138 | +1.681 ± 0.139 |
| worst-clean data W (Υ 4, f 0.7, lower σ, no upper limits), L★ floor | +0.964 ± 0.150 (6.4 sd) | +0.928 ± 0.150 (6.2 sd) |
| host bracket at the floor, E_lo / E_hi | +1.285 / +1.414 | +1.254 / +1.371 |
| side row: isolated native screening, L★ 24 (vs CFG691's +0.885) | +0.956 | +0.913 |
| estimator E-V (exact global virial), v3 at the floor | +1.418 | +1.383 |

**Frozen FAIL line: met on both footings.**
- |Δ| ≥ 3 sd at the floor, 24 pc and 90 pc.
- The worst-clean data W are ≥ 2 sd above the prediction (6.2–6.4 sd).
- The most favourable host cell (E_lo) is still 8.5–8.7 sd.
- The E-V estimator gives ≥ 3 sd everywhere.

**Why the gap grows.** The UFDs' internal fields are y ≈ 1e-4 – 1e-2 a₀. Their hosts' fields are x_e ≈ 0.02–0.87 a₀ (median ≈ 0.1).
- The satellites are therefore EFE-dominated, quasi-Newtonian with G_eff ≈ 1/μ(x_e). That is a median cost of
  0.58 dex against the isolated law. N0 quoted F3's estimate of −0.30 dex; the solved value is about twice that.
- The field also stops the isolated screening length L★²/2r_M from applying: in the field, screening acts at kL★ ≳ 1.4.
  That costs another 0.2 dex at the floor.
- Example: Segue 1 and Willman 1 drop to ×1.7 over Newton; Crater II drops to ×10.

Per system: `s1_per_system.csv`.

## Tile 29: the Coma UDGs (CFG933's 9 admitted)

The statistic is E = 2 ln(σ_obs/σ_pred), with CFG933's sealed convention.
- ⟨E⟩ is the unweighted mean.
- se is CFG933's (max of the scatter and measurement terms).
- σ_sys is CFG948's recipe (M★ ±0.2 dex, σ ±15 %, distance ±5 %), **rerun on the v3 prediction**. s_M grows from 0.24 to 0.46,
  because a quasi-Newtonian prediction scales as M★, not √M★.

The host field is Coma's measured hydrostatic total acceleration: the β-model of L23/CFG948 at the mean 3-D distance
(dmean) and at the projected distance (dproj).

| step | canonical ⟨E⟩ ln (dex) | z_stat / z_sys | alt ⟨E⟩ ln (dex) | z_stat / z_sys |
|---|---|---|---|---|
| S0 CFG933: isolated ν_e law (reproduced exactly; CFG948 σ_sys) | +0.760 (+0.330) | 2.90 / 1.67 | +0.669 (+0.291) | 2.56 / 1.47 |
| S1 kernel ν₁ | +0.760 | — | +0.669 | — |
| S2 AQUAL solve, isolated | +0.748 (+0.325) | 2.86 / 1.64 | +0.657 (+0.285) | 2.51 / 1.45 |
| S3 + EFE (Coma field, dmean), L★ = 0 | +2.581 (+1.121) | 9.86 / 4.28 | +2.481 (+1.078) | 9.48 / 4.11 |
| **S4 v3, L★ floor / 24 / 90, dmean** | **+2.581 (+1.121)** | **9.86 / 4.28** | **+2.481 (+1.078)** | **9.48 / 4.11** |
| S4 v3, dproj | +2.797 (+1.215) | 10.68 / 4.65 | +2.722 (+1.182) | 10.40 / 4.52 |
| field ÷ 2 (proxy for v3's law-on-baryons Coma field), dmean / dproj | +2.174 / +2.480 | z_sys 3.60 / 4.12 | +2.043 / +2.372 | 3.38 / 3.94 |
| S6 native H₀ (distance × 70/67.9, ASSUMED source H₀), dmean | +2.536 | 9.69 / 4.20 | +2.436 | 9.30 / 4.04 |
| estimator E-V, dmean | +2.846 | 10.87 / 4.72 | +2.746 | 10.49 / 4.55 |
| all 11 Coma, dmean | +2.542 | 11.51 / 4.33 | +2.440 | 11.05 / 4.16 |
| isolated bound (x_e = 0) | +0.749 | 2.86 / 1.65 | +0.658 | 2.51 / 1.45 |

**Frozen FAIL line: met.**
- |z_sys| ≥ 3 at dmean and at dproj, at every L★, on both footings.
- **ROBUST:** with the host field halved it is still 3.4–4.1.
- Screening is irrelevant here: Λ = L★/R_e ≤ 0.06 moves ⟨E⟩ by ≤ 1e-3.
- The Coma frozen line did not name an L★. All three were evaluated and they agree.
- Per galaxy, E rises from +0.14 to +1.86 (old) to +1.92 to +3.79 (v3, dmean); all 9 are above. File: `s1_coma_per_galaxy.csv`.
- **Hand check (DFX1):** the linear-AQUAL monopole boost in a field x_e = 0.498 is 2.52 (F2's far-field formula). That gives
  E ≈ +2.24 against the solved +2.247.

**What the FAIL rests on: equilibrium in the current field.** Isolated, the UDGs are only 1.4–1.6σ from v3. The internal
crossing time (R_e/σ ≈ 0.1 Gyr) is much shorter than the orbital time in Coma, and v3 has no memory, so the static
reading is the natural one. A UDG far out of equilibrium would escape it. That escape is a model assumption, not a v3
mechanism.

## S5: the μ_K² term (BS24 Eq. 35) and native H₀

- **Internal Helmholtz piece.** At BS's cap (μ_K = 14.8 h/Mpc), ε = μ_K²(3r₁₂)²/μ(x_e) reaches 0.024 / 0.026 (satellites,
  max: Crater II) and 0.064 / 0.073 (Coma).
  - This is **not below the frozen 1e-2 "negligible" line**.
  - As an order-of-magnitude bound it moves log g by ≤ 0.03 dex, against gaps of 0.9–1.3 dex. It is not solved.
- **Host dust inside the system.** The host's whole local dynamical density (law phantom included, E_hi host) is a fraction
  of each system's missing density:
  - satellites: median 8e-4, max 0.40 (Crater II);
  - Coma: mean 5e-3, max 0.011 (the measured β-model density).
  - The NOT DECIDABLE clause therefore does not fire. Whatever the μ_K² zero point, host dust cannot fill the gap.
- **Native H₀:** the satellites' distances are stellar and do not depend on H₀. For Coma, scaling the distance by 70/67.9
  moves ⟨E⟩ by −0.045 ln. The sources' H₀ is not on disk, so this step is labelled ASSUMED.

## Feed to tile 31 (one selector for the family), v3 numbers

| family member | v3 excess |
|---|---|
| dwarf satellites | +1.30 to +1.72 dex (L★ floor to 90 pc) |
| Coma UDGs | +1.08 to +1.22 dex (+2.5 to +2.8 ln) |
| cluster cores (F1) | ×1.5–1.9 |

All three sit **above** v3, and all three sit in a host field. For satellites and UDGs, the EFE is the single largest
contributor to the gap.

## Checks (`s1_v3_hosted_small.out`; 1113 s, one thread, peak RSS 0.52 GB, 8512 production solves, worst residual 1.0e-10)

- **K1:** E3 reproduced with this lane's own code to 0.005 dex (N 45 / 46).
- **K2:** isolated 2D solve vs the algebraic law, 2.3e-4.
- **K3:** D10 vs F2's independent AQUAL solver, embedded, 1.8e-3.
- **K4:** linear EFE vs Route F, 2.8e-3.
- **K5:** convergence, 8.6e-4.
- **K6:** Newton limit, 2.7e-8.
- **K7:** CFG933 per-galaxy E, ⟨E⟩ and se, 4e-16.
- **K8:** CFG948 σ_sys components, 1e-16.
- **K9:** every solve converged.
- **K10:** RSS < 1 GB.
- **`--mutate`** (the Newtonian y_e passed as the total background field) breaks K3 (1.17) and K4 (18.7). It runs the checks
  only and writes `*_MUTATE.*`.

## Record items this changes

- `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §3 "dwarf satellites +0.89 dex above screened prediction (E3)" is not v3's
  number. v3 gives +1.33 / +1.30 dex at the floor (+1.36 / +1.31 at 24 pc).
- Tile 29 changes colour: UNDEC → FAIL. Its old note ("isolated law", P2 posit, no-capture ceiling) belongs to retired
  models.
- N0's "F3 estimates the EFE costs −0.30 dex" is about half of the solved median cost (−0.58 dex).

## What this does not show

- Each system is a spherical Plummer in a **uniform** field. Not included:
  - tides (gradient terms; E3: 14 % of satellites have r₁₂ beyond the baryon-only Jacobi radius);
  - the field-induced flattening of the stars;
  - non-equilibrium.
- The host fields are approximate:
  - MW and M31 are spherical Hernquist law fields with bracketed masses; M31's 1e11 M☉ is an external label;
  - Coma's field is an isothermal hydrostatic β-model;
  - Leo T uses the MW field at its heliocentric distance.
- The μ_K² term is bounded, not solved. v3 fixes neither μ_K nor its zero point.
- Tile 19 (TDGs, DF2/DF4) is not computed here.

## Run
```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/S1_v3_hosted_small/s1_v3_hosted_small.py            # ~19 min
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/S1_v3_hosted_small/s1_v3_hosted_small.py --mutate   # ~12 s, exit 1
```
Files: `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (25c5861b57, committed alone first); script; `.out`;
`_results.json`; `s1_per_system.csv`; `s1_coma_per_galaxy.csv`; `*_MUTATE.*`.
