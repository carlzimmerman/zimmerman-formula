# CFG162 — KURVS a₀(z) as a function of the outer pressure-support strength: the crossing point, and where the published prescriptions sit

**This lane removes the which-calibration choice but adds a placement choice. The decisive quantities remain the outer pressure support at 2–4.5 R_e and the total cold gas; this lane measures neither.**

- **Criteria:** frozen in `CFG162_FROZEN_CRITERIA.md` (9f098e8a8).
  - Known before freezing, and disclosed there: CFG160's rows at α × 0.6/1.0/1.4, CFG141's grids, CFG165's s = 0.71 and its break-evens (0.65, 2.14), and CFG161.
- **Script:** `CFG162_pressure_axis.py`, about 30 s. The figure is `CFG162_pressure_gas_axes.png`.
- **Runs:**
  - The main run passes C1, C3 and the headline H1, fails control C2 (see Controls), and exits 1.
  - The MUTATE run (velocities × 2) has no crossing in [0, 4]; H1 fails, so the control is informative.

## Bottom line

**A map, not a verdict.**
- At the decision cell (μ = 0.67, δ = 0, canonical), flat a₀ is preferred when the outer pressure support is below **s_mid = 0.67 × Kretschmer et al.'s α** (bootstrap 16–84%: 0.51–0.85), and the rival a₀ ∝ H(z) above it.
- **Every published prescription sits above s_mid at that gas level.** So at the paper's molecular-only gas, the literature places KURVS on the rival side.
- **The crossing moves with the total gas,** and the published prescriptions then straddle or fall below it. Given the literature, the KURVS test reduces to the total gas.

| prescription (placed by the frozen rule) | s_eq | own decision cell: Δ′_flat / Δ′_H | break-even gas: flat / rival |
|---|---|---|---|
| none (P0) | 0 | −2.3σ / −4.6σ (neither) | — |
| **Kretschmer et al. 2021** (VELA; ±40% band 0.6–1.4) | **1.00** | +3.3σ / −0.1σ (lean rival) | 2.11 / 0.62 |
| Dalcanton & Stilp 2010 (P ∝ Σ^0.92) | 1.42 | +4.1σ / +1.2σ (lean rival) | 3.10 / 1.26 |
| fixed scale height (P3) | 1.62 | +3.5σ / +1.3σ (lean rival) | 3.56 / 1.56 |
| Price et al. 2022 (deprojected exponential, n = 1) | 1.69 | +4.7σ / +1.9σ (lean rival) | 3.73 / 1.67 |
| self-gravitating disc (P2) | 3.00 | +6.0σ / +3.7σ (neither) | > 4 / 3.83 |

- **The crossing against the gas** (canonical, δ = 0):

  | μ | s_mid | how the placed prescriptions sit |
  |---|---|---|
  | 0.25 | 0.44 | — |
  | 0.67 | 0.67 | all above: lean rival |
  | 1.5 | 1.11 | Kretschmer (1.0) now below, i.e. flat side; Dalcanton & Stilp, P3 and Price above; they straddle |
  | 4 | 2.39 | all but P2 below: flat side |

  The alt footing gives s_mid = 0.66.
- **Other crossings at the decision cell:**
  - s_f2 = 0.73: flat is disfavoured above it;
  - s_h2 = 0.60: the rival is disfavoured below it;
  - between them, both readings are within 2σ.
- **The same map read the other way.** For the published prescriptions (s = 1.0–1.7), flat a₀ fits KURVS if the total cold gas is μ ≈ 2.1–3.7 M*, and the rival if μ ≈ 0.6–1.7 M*. The molecular prior (μ_mol = 0.67 from the paper; 0.67–1.5 for molecular fractions of 0.4–0.6) sits at the rival's end, and HI is unmeasured.
- **Full grid:**
  - at s = 1: 14 of 24 cells lean rival, 6 lean flat;
  - at s = 0.5: 10 lean flat, 4 lean rival;
  - for s ≥ 2.5: no cell leans flat.
- **Power:** (Δ′_flat − Δ′_H)/σ is 2.5, 3.4, 3.1 and 2.6 at s = 0, 1, 2 and 4.

## Controls

- **C1:** at s = 0.6, 1.0 and 1.4 the curve reproduces CFG160's committed decision-cell rows (for example +0.1441 / −0.0060 at s = 1).
- **C3:** the P2 prescription in the placement code reproduces CFG141's committed P2 cell to 1e-12.
- **C2 FAILED as implemented, and is kept.**
  - The frozen text asked that Price's α(y) = y K₁/K₀ "match y + 1/2 + O(1/y) at y = 50 (to 1e-3)". I checked it against a next-order term I derived wrongly, y + 1/2 + 3/(8y); the correct expansion is y + 1/2 − 1/(8y).
  - The implementation itself passes the other two parts: the leading-order bound (0.0025 < 1/y) and the numerical −d ln K₀/d ln y to 1e-8.
  - Post hoc, labelled: α(50) = 50.4975485 against y + 1/2 − 1/(8y) = 50.4975000 (difference 4.9e-5), and at y = 200 the difference is 3.1e-6.
  - C2 alone makes the main run exit 1; the MUTATE's informative failure is H1.

## Readings (as frozen)

- **The result is a map:** any statement that the data favour a reading must name both s and μ.
- **At the paper's molecular gas, the placed prescriptions all fall on one side,** the rival's. So there the lean follows the literature, conditional on the gas.
- **At μ = 1.5 they straddle s_mid, and at μ = 4 nearly all fall on the flat side.** The literature does not decide the question once the gas is uncertain.
- **The decisive quantity is therefore the total cold gas, given the published prescriptions:**
  - rival break-even 0.6–1.7 M*;
  - flat break-even 2.1–3.7 M*.
  - CFG163, KURVS-15's archival ALMA, is the first measurement aimed at it.

## Disclosures

- **The axis runs to s = 4,** beyond the requested 1.6, so that every placeable prescription falls on it. This was declared in the frozen file.
- **Price et al. 2022 is placed with n = 1** from its eq. 13, not from its figures. Dalcanton & Stilp's sign is taken as pressure adding to V_c.
- **The break-even gas at each prescription** is root-found on a μ grid of step 0.25 in [0.25, 4]. P2's flat break-even lies above 4 and is left unplaced.

## Untested (declared)

- which prescription is physically right for KURVS's discs;
- anisotropy;
- non-equilibrium;
- the gas;
- the placement's own uncertainties beyond Kretschmer's stated scatter;
- n ≠ 1;
- the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## After CFG168's independent re-derivation (appended 2026-09-29; the text above is unchanged)

- **Wording: the KURVS lean rests on a calibration and gas region the data cannot fix; it is not a detection either way. On this map, a flat world with more gas looks like a rival world.**
- **What reproduces.** CFG168 (7c0d1f428) is the Opus chat's independent re-derivation. Every headline row reproduces within its frozen pass lines:
  - s_mid 0.6693, s_f2 0.7257, s_h2 0.5993;
  - bootstrap 0.513–0.844;
  - gas-bracket crossings 0.444 / 1.108 / 2.387;
  - break-evens 2.109 / 0.621;
  - the placements 1.422 / 1.617 / 1.688 / 3.001, the counts and the power row.
- **Corrections:**
  1. **The break-evens are brentq roots.** They are bracketed on a μ grid of step 0.25 and then solved continuously, so "root-found on a μ grid of step 0.25" misleads. The bracket stops at μ = 4, so P2's flat break-even, printed "> 4", is 6.85 (CFG170 gets 6.845).
  2. **With P2 included, the flat break-even range is 2.1–6.9 and the rival's 0.6–3.8.** The summary "flat 2.1–3.7, rival 0.6–1.7" covers K21, Dalcanton & Stilp, P3 and Price only.
  3. **K21 as a band straddles the crossing.**
     - Kretschmer's ±40% band edge (s = 0.6) lies below s_mid, and 33% of the ten-disc bootstrap resamples have s_mid < 0.6.
     - With R_e = 2 R_eff, K21 at s = 1 falls to the flat side (s_mid = 1.058).
     - The other four prescriptions stay above s_mid in every placement variant.
  4. **The crossing moves at the 0.1 level with:**
     - the gas-disc scale: +0.138 at 1 R_d, −0.109 at 3 R_d;
     - the anchor-offset statistic: −0.105 with the median instead of the pooled mean;
     - which discs are in: jackknife range 0.203;
     - the velocity scale: −15% and −10% in V move s_mid to 1.03 and 0.91; +26% removes s_h2, and +50% removes the crossing.
  5. **The region where both laws are within 1σ is empty** (minimum separation 2.24σ).
  6. **The crossing does not identify the law.** A flat world at (s, μ) = (1, 2.14) and a rival world at (1, 0.65) give the same s_mid distribution.
- **Label items:** the README's MUTATE says "velocities × 2", but the code uses 10^0.3. The MUTATE printout shows s_mid = nan (cosmetic). C2's wrong asymptotic is already disclosed above.

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.
