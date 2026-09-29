# CFG162 — KURVS a₀(z) as a function of the outer pressure-support strength: the crossing point, and where the published prescriptions sit. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's go, before any number of this lane has been computed.

**What this lane does and does not do.**
- It removes the which-calibration choice, but it adds a placement choice (the rule below).
- The decisive quantities remain the outer pressure support at 2–4.5 R_e and the total cold gas. This lane measures neither.
- A scoped or non-diagnostic answer is valid.

**Known before freezing** (disclosed):
- CFG160's decision-cell rows at α × 0.6, 1.0 and 1.4 (Kretschmer's α);
- CFG141's P2 and P3 grids;
- from CFG165, relayed by the orchestrator: flat's Δ′ drops below +2σ at s = 0.71, and the break-even gas is μ = 2.14 (flat) and 0.65 (the rival);
- CFG161's differential.

Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## The axis

- **s** is the outer pressure-support strength relative to Kretschmer et al. 2021: V_c² = V_obs² + s · α_K21(x) · σ², with α_K21(x) = −0.146x² + 1.204x + 1.475 and x = R/R_e − 1 clipped to [0, 4]. The functions are CFG160's, copied verbatim.
- **The range** is s ∈ [0, 4], on a grid of step 0.01. This is extended beyond the requested 1.6, declared here, so that every placeable prescription falls on the axis.
- **Everything else is CFG160's pipeline:** KURVS with CFG141's measured σ_out, the SPARC same-pipeline anchor with the same s, both footings, the gas bracket, the stellar-mass bracket, and the pooled errors.

## Primary output 1: the decision-cell curve (μ = 0.67, δ = 0, canonical) and its crossing points

- **Curves:** Δ′_flat(s) and Δ′_H(s), each with its σ.
- **The crossing points,** each computed by root-finding (brentq) on the continuous function, not interpolated from a grid:
  - **s_mid:** where Δ′_flat = −Δ′_H. There the data sit midway between the two readings. Flat is preferred below s_mid and the rival above it.
  - **s_f2:** where Δ′_flat = +2σ_flat. Flat is disfavoured above s_f2.
  - **s_h2:** where Δ′_H = −2σ_H. The rival is disfavoured below s_h2.
- **The errors on the crossings:**
  - **statistical:** 2,000 bootstrap resamplings of the ten KURVS discs, with seed 162, and the SPARC anchor held fixed. The 16th–84th percentiles are reported.
  - **the gas bracket:** the three crossings recomputed at μ = 0.25, 1.5 and 4.
  - **the footing:** the alt footing.
- **The full-grid verdicts against s:** for s ∈ {0, 0.25, …, 4}, the counts of the 24 cells that lean flat, lean rival, both within 2σ, or neither, by CFG160's map.

## Primary output 2: the gas axis at s = 1

- **Curves:** Δ′_flat(μ) and Δ′_H(μ) for μ ∈ [0.25, 4] on 60 log-spaced points (δ = 0, canonical).
- **The break-evens** μ_f (Δ′_flat = 0) and μ_h (Δ′_H = 0), computed by root-finding. They are also computed at each placed prescription's s.
- **The prior marked on the axis, and nothing else:** molecular gas μ_mol = 0.67 (the paper's 40%, from Tacconi+2020 scaling relations), within a range of 0.67–1.5 (molecular fractions of 0.4–0.6). HI is unmarked because it is unmeasured.

## The placement rule (fixed here, before any placement number)

- **What a prescription's s_eq is:** the root, in s ∈ [0, 6], of Δ′_flat(s × K21) = Δ′_flat(prescription) at the decision cell. The prescription is applied to KURVS (σ_out) and to the SPARC anchor (σ = 10 km/s) alike. Each prescription's own decision-cell verdict is reported beside it.
- **The prescriptions** (a fixed list; each was read, as noted):
  - **none (P0):** s_eq = 0 by definition.
  - **Kretschmer et al. 2021** (Table 1, gas in discs; read from the HTML): s = 1 by definition, with its stated 40% scatter as the band 0.6–1.4.
  - **Price et al. 2022,** eqs. 12–13 (read from the HTML text): α(R) = −d ln ρ_g/d ln R, with constant σ and ρ_g the deprojected Sérsic density.
    - For n = 1, the deprojected exponential gives ρ ∝ K₀(R/R_d), so α = y K₁(y)/K₀(y) with y = R/R_d. The intrinsic axis ratio does not enter the mid-plane slope.
    - n = 1 is the lane's declared disc profile, as in CFG140. The text quotes no numbers for this case, and none are taken from its figures.
  - **Dalcanton & Stilp 2010,** eqs. 16–17 (read from the HTML): turbulent pressure P ∝ Σ^0.92 (Joung et al. 2009), giving α = 0.92 R/R_d for an exponential disc. The page's sign rendering is taken to mean that pressure support adds to V_c, which is the only physical reading.
  - **Fixed scale height (P3):** CFG141's form, σ²R/R_d − R dσ²/dR capped at 0, with the measured gradient.
  - **Self-gravitating disc (P2):** 2R/R_d, as in Burkert et al. 2010 and CFG141.
- **A prescription is left unplaced** if no root exists in [0, 6].

## Checks

- **C1 CONTROL:** at s = 0.6, 1.0 and 1.4 the curve reproduces CFG160's committed decision-cell rows (3-decimal print).
- **C2 CONTROL:** the Price α(y) implementation matches y + 1/2 + O(1/y) at y = 50 (to 1e-3), and the direct numerical derivative of ln K₀ (to 1e-8).
- **C3 CONTROL:** with the P2 prescription, the placement code reproduces CFG141's committed P2 decision cell (1e-12).
- **R0 POWER** (printed before any curve value): the separation (Δ′_flat − Δ′_H)/σ at the decision cell for s ∈ {0, 1, 2, 4}.
- **H1 [HEADLINE; MUTATE must change it]:** the preference crossing s_mid exists in [0, 4] at the decision cell, and is reported with its bootstrap and gas-bracket ranges.

## MUTATE

MUTATE=1 multiplies every KURVS v_last by 10^0.3 (g_obs × 4), inherited from CFG140's exec'd prefix. Then Δ′_flat > 0 at every s and no s_mid exists in [0, 4], so H1 must fail and the script exits 1.

## Outputs

- A two-panel figure (`CFG162_pressure_gas_axes.png`). The left panel is the s-axis with the decision-cell curves, the crossings and the placed prescriptions. The right panel is the μ-axis at s = 1, with the break-evens and the molecular prior.
- The `.out` and `_results.json` files.

## Readings (declared)

- **The result is a map, not a verdict.** At the decision cell, flat a₀ is preferred for outer pressure support below s_mid (in units of Kretschmer's α) and the rival above it. The placed prescriptions show where the literature sits on that map. Any statement that "the data favour X" must name both s and μ.
- **If the placed prescriptions straddle s_mid,** the literature does not decide the question. If they all fall on one side, the lean follows the literature, conditional on the gas.
- **Untested (declared):**
  - which prescription is physically right for KURVS's discs;
  - anisotropy;
  - non-equilibrium;
  - the gas;
  - the placement's own uncertainties beyond Kretschmer's stated scatter;
  - n ≠ 1 for Price et al.;
  - the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
