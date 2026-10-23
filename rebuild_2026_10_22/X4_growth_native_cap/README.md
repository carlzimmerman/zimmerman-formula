# X4_growth_native_cap: v3's linear growth at the μ_K S4 allows, and whether Q7's large-λ_D DBI door survives its own checks

Lane X4 of `rebuild_2026_10_22/X0_explanation_map/MAP.md` (§1.B items 1–2; §3 "Growth at the cap").
Frozen criteria and assumption ledger committed alone first: 2060d39ced. AMENDMENT A1 is post-result and changes no
verdict line.

κ = ½ FITTED. a₀ is absent at linear order on FRW (Q6 D0), so neither footing enters any number computed here; S4's
inherited guard holds on both footings (9.3603e-11 / 1.1312e-10 m/s²), never pooled. No dark-matter particle. λ_D is a
growth-set knob: graded here, never adopted. Not "theory closed". Nothing here says the data favour the framework.

## Verdicts

| question | frozen verdict | the numbers (JSON key) |
|---|---|---|
| **(i)** v3's linear growth at the μ_K that S4's galaxy guard allows | **GROWTH FAILS AT THE NATIVE CAP** | Boltzmann (Q6 LOB) R_B = **0.00317** at 0.03 Mpc⁻¹ and **0.00523** at 0.1 Mpc⁻¹ (`x4_growth_results.json` `R_B`). F3's ODE (J_x, a_i = 1e-3, an upper bound) gives 0.0757 / 0.0817 (`ode.*.bsk2_ai0.001`). The shortfall to 0.95 is **×300 / ×182** (Boltzmann) and ×12.5 / ×11.6 (ODE) (`gaps.sigma8_shortfall_0.95_over_R`). The μ_K gap is **8.1e3–5.7e4** at 0.03 and **2.4e3–1.7e4** at 0.1 (`gaps.mu_gap_mu95_over_mu_guard`). |
| **(ii)** Q7's large-λ_D DBI door | **DOOR CLOSED BY F (the forest gate) at all three λ_D,95 points; the consistency check D does not close it.** The P2μ closure is **marginal**. | D: max linear rms δQ / line = **0.048 (cap), 0.098 (P1μ), 0.35 (P2μ)**, all PASS (`D.*.rows.*.S_rms_over_L`). F at z = 3: cap band **0.12–0.32**, P1μ **0.22–0.40** (FAIL, every bin a factor ≥ 2 below the 0.8 edge). P2μ's band **passes** (0.98–1.00 at z = 3, 0.92–0.99 at z = 2), but L319's T²(k5) is **0.972 (z = 3) and 0.896 (z = 2)**. That fails the strict 0.995 line at both z and the loose 0.9 line at z = 2 by 0.004 (`F.*.primary`). |

**Plain reading.**
- (i) At the μ_K the galaxies allow, v3's khronon dust never clusters on σ₈ scales. Linear σ₈ is 0.3–0.5 % of the dust
  limit, so the record's "0.391 / 0.073 at the cap" overstates v3's growth by another ×14–23.
- (ii) The DBI fix is self-consistent at linear order. The forest kills it at the galaxy cap and at P1's μ, which S4's
  guard already excludes.
  - At P2's μ (22.3 Mpc), the one point inside S4's untested gap between 0.03 and 0.1 Mpc⁻¹, the forest fails only on
    the record's strict WDM-calibrated line.
  - It fails the loose line by 0.4 % at z = 2. At z = 3 alone that point is not decided (band passes, strict line fails,
    loose line passes).

## Unit conversion (FROZEN_CRITERIA §1)

- S4's μ_K is physical, in Mpc⁻¹.
- F3 quotes μ in h/Mpc at its background A: μ[h/Mpc] = μ[Mpc⁻¹]/h_A, with h_A = 0.6757803.
- So 10 Mpc⁻¹ = 14.7977 h/Mpc (G0c reproduces F3's value to 1e-9), **0.03 Mpc⁻¹ = 0.04439 h/Mpc** and **0.1 Mpc⁻¹ =
  0.14798 h/Mpc** (`conversion`).
- Q6/Q7's CLASS takes `aest_K2` = μ² in Mpc⁻², so no h enters the Boltzmann runs.

## Step 0: reproductions (all PASS)

| id | result | line |
|---|---|---|
| G0a | F3's ODE copy gives 0.390800 / 0.202602 / 0.120552, equal to F3 K4 | ≤ 1e-4 |
| G0b | Q6's binary gives DUST σ₈ 0.827959 and LOB 14.8 σ₈ 0.0607512, so R_B 0.073375, equal to Q6 | ≤ 1e-4 |
| G0c | 10/h_A = 14.7977084631 h/Mpc, equal to F3 | ≤ 1e-9 |
| D0a | Q7's CAP@l95_best and LCDM_best z = 0 P(k): **bit-identical** (max \|Δln P\| = 0). Ratios 0.97677 / 0.32937 / 0.09799 and σ₈ 0.787585 are exact | ≤ 1e-4 |
| D0b | R_B at λ_D,95 (fixed P0): 0.95001 (cap), 0.95000 (P1μ), 0.95003 (P2μ) | \|R_B − 0.95\| ≤ 0.002 |
| D0c | δ_K extraction on DUST: δ_K vs d_cdm ≤ 1.4e-6 and θ term ≤ 2.0e-6, at every z ≤ 500 | ≤ 1e-5 |
| D0d | P(k,z) = (2π²/k³) A_s (k/k_p)^{n_s−1} d_m²: ≤ 5.5e-6 | ≤ 1e-3 |
| D0e | analytic DBI ρ_K vs CLASS background ≤ 1.8e-12 (z ≤ 500); I₀ ≤ 8.6e-12 | ≤ 1e-6; ≤ 1e-8 |
| F0a | L346 gate from its JSON: sw5_canon z = 3 1.0644–1.2168, sw5_alt 1.0728–1.2463, so FAIL (as L346); control exactly 1 | to 1e-9 |
| F0b | L319 strict line T²_5.3keV(k5 = 4.6199) = 0.99519 (L319: 0.995) | ≤ 5e-4 |
| F0c | the gate on ΛCDM: DUST vs vanilla ΛCDM and DBI(10³⁰) vs DUST give 1.000000 in every bin, so PASS | within 1e-3 of 1 |

## Step 1, question (i) (`x4_growth.py`: 6/6 PASS, exit 0, 25 s, peak 0.29 GB; MUTATE 3/6, exit 1)

| μ_K (physical) | h/Mpc at h_A | Q6 LOB R_B | ODE J_x, a_i 1e-3 | ODE J_x, a_i 1e-4 | 0.95/R_B | μ_K,95/μ_K |
|---|---|---|---|---|---|---|
| 0.03 Mpc⁻¹ (guard PASS) | 0.04439 | **0.003169** (σ₈ 0.00262) | 0.07574 | 0.04144 | 300 | 8126 (F3 bsk2 1e-3), 9261 (Jeans), 5.73e4 (bsk2 1e-4), > 5.72e4 (Q6) |
| 0.1 Mpc⁻¹ (guard FAIL) | 0.14798 | **0.005232** (σ₈ 0.00433) | 0.08171 | 0.04470 | 182 | 2438, 2778, 1.72e4, > 1.72e4 |
| cap 10 Mpc⁻¹ (record) | 14.80 | 0.07337 | 0.39080 | 0.20260 | 12.9 | 24–172 (F3) |

- The Jeans columns are skipped by F3's own rule (3/(a_i μ_h) > 3000).
- G1: every estimator is monotone in μ_K. So R at the true guard edge (between 0.03 and 0.1) lies in [R(0.03), R(0.1)).
- The Boltzmann P(k)/P_dust at z = 0 is 1.6e-5 at k = 0.1 h/Mpc and ~1e-11 at k = 1 h/Mpc (`boltzmann_Pk_over_DUST_z0`).
  - At these μ the LOB khronon has c_s² ≈ ε/(1+ε) ≈ 1 until z ≈ 35–78. After that it is held on k > aμ ≲ 0.15 h/Mpc.
  - So it never clusters on σ₈ scales: growth is essentially baryon-only, with Silk-damped small scales.
  - The ODE starts both fluids as growing dust at a_i, which is why it stays near F3's 0.075 (the BS24 scale).
- Reported (`literal_background_reported`): the literal quadratic K is even further from BBN at these μ.
  - ΔN_eff,equiv(1 MeV) = 8.5e18 (0.03) and 7.7e17 (0.1). The cap value 7.698e13 reproduces Q6.
  - So LOB (a dust background) is not the literal theory here either, as at the cap.

## Step 2, question (ii) (`x4_dbi_door.py`: 9/9 PASS, exit 0, 20 s, peak 0.48 GB; MUTATE 5/9, exit 1)

The points are Q7's committed λ_D,95 values. The cap point is primary as Q7's CMB best fit (Δχ² +1.58) against ΛCDM's
best fit. P1μ and P2μ are at the fixed C7 ΛCDM-refit parameters against DUST (Q7 fitted neither).

**D: linear rest-frame δQ (gauge-invariant, Q6 D2) against L = λ_D^{-1/2}/3.** z grid 0–500, k ≤ 10 h/Mpc.

| point | μ (Mpc⁻¹) | λ_D,95 | L | max_z σ_δQ (z) | max per-ln-k (z, k h/Mpc) | σ/L | D | headroom ratio (reported) |
|---|---|---|---|---|---|---|---|---|
| cap (best fit) | 9.998 | 7.840e9 | 3.765e-6 | 1.80e-7 (37) | 1.29e-7 (37, 0.34) | **0.048** | PASS | 0.32 |
| cap (fixed) | 9.998 | 7.840e9 | 3.765e-6 | 1.80e-7 (37) | 1.29e-7 (37, 0.34) | 0.048 | PASS | 0.32 |
| P1μ | 4.484 | 3.551e10 | 1.769e-6 | 1.74e-7 (10) | 1.26e-7 (10, 0.33) | **0.098** | PASS | 0.68 |
| P2μ | 0.04484 | 3.978e9 | 5.285e-6 | 1.84e-6 (0) | 1.49e-6 (0, 0.074) | **0.35** | PASS | **5.7** (z = 3) |

- δQ peaks where the hold scale aM bottoms out (cap: aM = 0.65 h/Mpc at z ≈ 37). It equals the khronon's own
  Yukawa-screened potential, as pre-stated. The synchronous-gauge values are the same to three digits.
- **Headroom (reported only, no verdict weight).** At P2μ the DBI background sits within ~3e-8 of the ceiling at
  z ≳ 2, so 3σ of linear δQ exceeds the remaining headroom by up to ×5.7.
  - That means linear theory is not valid there, since δQ/headroom ≈ 2δ_rest.
  - It is not a complex root: K′ diverges at the ceiling, so density alone cannot push Q through it.
  - The static-branch cluster estimate (Q7: ceiling = 1.02 / 0.48 / 1.42 × v²/c² of a 1000 km/s cluster) is inherited
    and was not re-graded.

**F: the record's forest gates on linear P(k)** (`F.<point>.primary.z`).

| point | z = 3 L346 bins (1.10–3.56 h/Mpc) | z = 2 bins | T²(k5) z = 3 / z = 2 | L346 [0.8, 1.2] | L319 strict (≥ 0.995) | L319 loose (≥ 0.9) | outside [0.5, 2] | F |
|---|---|---|---|---|---|---|---|---|
| cap (best fit vs ΛCDM best fit) | 0.323 → 0.123 | 0.311 → 0.106 | 0.107 / 0.090 | FAIL | FAIL | FAIL | yes | **FAIL** |
| P1μ | 0.404 → 0.218 | 0.363 → 0.175 | 0.199 / 0.158 | FAIL | FAIL | FAIL | yes | **FAIL** |
| P2μ | 0.998 → 0.981 | 0.986 → 0.922 | **0.972 / 0.896** | PASS | FAIL | FAIL at z = 2 only | no | **FAIL (marginal)** |

- At z = 3 alone (the task's "z ~ 3"): cap and P1μ FAIL; P2μ is not decided (band PASS, strict FAIL, loose PASS;
  `z3_only`).
- Reported only (A1): T² at exactly 5.00 h/Mpc for P2μ is 0.968 / 0.888, which is lower.
- Context, P/P_ref at z = 0 for k = 0.1 / 1 / 3 h/Mpc (`context_Pk_ratios`):
  - cap best: 0.977 / 0.329 / 0.098;
  - P1μ: 0.974 / 0.338 / 0.119;
  - P2μ: 0.951 / 0.681 / 0.534. Its hold arrives late (aM = 4.3 h/Mpc at z = 3, 0.085 h/Mpc today), so it
    suppresses low-z power instead of forest-epoch power.

**G: S4's guard (inherited, not recomputed).**
- cap and P1μ: FAIL (μ ≥ 0.1 Mpc⁻¹).
- P2μ: NOT ON S4'S GRID (0.0448 lies between the passing 0.03 and the failing 0.1).
- λ_D(v²/c²)² at 220 km/s is 2.3e-3 / 1.0e-2 / 1.2e-3. So the DBI K is quadratic to ≤ 1 % in galaxies, and S4's
  quadratic-K static solve applies to the DBI door there.
- Restricted to points not excluded by G: only P2μ, where F is FAIL (marginal).

## Amendments

- **A1 (POST-RESULT; changes no verdict line).** L319's "k = 5 h/Mpc" line is evaluated at L319's own grid point
  k5 = 4.6199 h/Mpc, where its 0.995 holds. The scripts used k5 from their first run.
  - T² at exactly 5.00 was added afterwards as a reported-only number, and the step-2 script was re-run (deterministic;
    every other number unchanged).
  - The same entry records two implementation details: h comes from CLASS's background file (12 digits), and output
    files are located by glob.

## Files and commits

| commit | content |
|---|---|
| 2060d39ced | `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md`, alone, before any script or number |
| c778d300e8 | `x4_growth.py`, `x4_dbi_door.py`, their `.out` / `_results.json` (main and MUTATE), AMENDMENT A1 |
| (this commit) | README |

Run from this directory (CLASS run files go to `../_external_data/x4_growth_native_cap_2026_10_23/`, not committed):
- `OMP_NUM_THREADS=1 nice -n 15 python3 -I x4_growth.py`
- `OMP_NUM_THREADS=1 nice -n 15 python3 -I x4_dbi_door.py`
- `X4_MUTATE=1` gives the `*_MUTATE.*` files.
  - Step 1 MUTATE: the no-hold kernel plus Q6's MUTATE binary break G0a and G0b (and G1).
  - Step 2 MUTATE: Q7's MUTATE binary plus an extraction without photons, ur and θ break D0a, D0b, D0c and F0c.

Compute: one thread, nice 15, one CLASS process at a time. Peak 0.29 GB (step 1) and 0.48 GB (step 2), 25 s and 20 s.
The heavy queue's live L1 run was not touched. No PM simulation, no download, no λ_D or μ_K scan, no fit.

## What this does not show

- **No nonlinear growth.** v3's deep-MOND Y^{3/2} channel is L1's question. (i) is the linear sector only. The CMB's
  acoustic scales are out of a₀'s reach anyway (MAP §1).
- **F is a linear proxy.** L346 graded nonlinear PM matter power, and L319's line is a linear WDM-calibrated transfer
  criterion; neither is the forest flux power.
  - For the cap and P1μ every bin sits a factor of 2–7 below the band edge (worst bins 0.12–0.22), beyond the
    pre-declared [0.5, 2] margin that nonlinear refill would have to bridge.
  - For P2μ the closure rests on L319's lines alone (strict at both z; loose at z = 2 by 0.004) and is marginal.
- **P2μ was never CMB-fitted** (fixed ΛCDM-refit parameters). Its G status is unknown on S4's grid. Its z = 0 power at
  1–3 h/Mpc is 0.53–0.68 of ΛCDM, a low-z suppression this lane does not grade (KiDS, small-scale lensing).
- **D is linear.** The headroom diagnostic shows linear theory fails near the ceiling at P2μ. The nonlinear and static
  (cluster) branches of the DBI root are not solved.
- **Not tested:** μ_K or λ_D other than the pre-declared points, in particular a DBI λ_D,95 at μ ≤ 0.03 Mpc⁻¹ (stop
  rule), and non-DBI K shapes.
- **Provisional inputs.** BS24/BS25 equations and parameter values remain the record's PROVISIONAL WebFetch
  transcriptions. The forest lines are LITERATURE-INPUT (ΛCDM-calibrated).

## Records this affects (suggested fixes; not edited)

- `X0_explanation_map/MAP.md` §1.B1 / §3 ("likely ~10⁴×"): the computed μ_K gap is 2.4e3–5.7e4, and the σ₈ shortfall
  at the native cap is ×182–300 (Boltzmann).
  - The record's "0.391 at the cap" (ODE) and "0.073" (Boltzmann) should be read as graded at a μ_K that S4 excludes.
    At the guard edge v3 gives R_B 0.003–0.005.
- MAP §1.B2 and Q7 README §5 ("the door"): the door is closed by the forest at all three λ_D,95 points (P2μ marginal),
  not by its own linear consistency (D passes by ×3–21). The "K goes complex in clusters" remark stays an inherited
  static-branch estimate.
- `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §2 (μ_K "FREE"; growth requirement 361–2542 h/Mpc): add that S4's guard
  caps μ_K at 0.03–0.1 Mpc⁻¹, where linear R_B = 0.003–0.005.
- Status board growth tile and LEDGER: no row exists for X4 yet; suggested wording is in the verdict table above.
