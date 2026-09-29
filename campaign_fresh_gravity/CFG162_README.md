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
