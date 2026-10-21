# WT-06 FROZEN CRITERIA: how long does the extra pull take to catch up after a sudden baryon change?

Lane WT-06 of `what_is_time/` (owner question 2026-10-21: "what is time, based on my framework?"). Written 2026-10-21, before any
script, run or number of this lane. Committed alone. Post-freeze changes are appended as dated amendments only.

Settings: κ = ½ FITTED (never derived). Footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), scored separately and
never pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is added. Raw data and framework-native
quantities only; instantaneous MOND appears only as a same-pipeline comparison, never as a yardstick in a verdict. Not "theory
closed". Nothing here says the data favour the framework. Identities are flagged where they occur.

## 1. Question

After an instantaneous change δM_b of a galaxy's baryons (gas blowout), how long does the framework's extra pull take to
re-equilibrate, and is the lag a signature that instantaneous MOND (a0 fixed, no medium) does not have?
- (a) Split the response in the CFG938 parent: (i) the field part (χ, Φ), (ii) the cold-energy mass part. Derive the governing
  timescales in sympy.
- (b) Spherical toy on NGC 3198 and one dwarf: remove 20% and 50% of the gas instantly; follow the circular speed in time; report
  t_50, t_90 at 2 and 5 disc scale lengths, both footings.
- (c) Compare with the CFG763 / CFG764 clock windows and with instantaneous MOND in the same pipeline.
- (d) Where would the lag show, what is the observable, and how big is it.

## 2. Inputs (read only; nothing downloaded; no other lane's file edited, run or staged)

| input | path | commit |
|---|---|---|
| parent action, static limit, R(u) = K W_rem′ = u²/(a0 − u), D_full = u + R, medium force f = −∇Φ_b + R(u)û, "drift = overdamped tether force" | `campaign_fresh_gravity/CFG938_medium_continuum_eft/` (DERIVATION §3–4, cfg938.py) | criteria 7a0d41e8b, README 92606e049 |
| record drift v_s = ατ(g − g_law), τ = (4πGρ_m)^(−1/2), τ_π = τ_ff/(2α), α causality max 1.186 | `campaign_fresh_gravity/CFG638_cold_energy_fluid_equations/` | 28ce71974 |
| galaxy-side α ≳ 0.5 | THEORY_CANONICAL 2026-10-21 DRAFT §1; CFG882; CFG889 | 9470c0433; f370e5577; 52812d58b |
| collisionless tether shells; sudden-loss surplus expelled with overshoot (coarse times only) | CFG747; CFG776 | c8771051d; criteria e2863f3ae, README dd0551dce |
| formation clock τ ∈ [0.724 can / 0.832 alt, 3.474] Gyr | CFG763 (`cfg763_results.json`; 3.474 = 8 Gyr/ln 10) | criteria 5b747a56b, README 14e6a9c17 |
| orbital clock τ = k t_orb, k ∈ [0.457 can / 0.525 alt, 1.196] | CFG764 (`cfg764_results.json`) | criteria 9990bf4b1, README 0fee9c16c |
| footings | `campaign_fresh_gravity/CFG4_common.py` (A0) | 3409d12da |
| SPARC rotmod NGC 3198, DDO 154 | `real_research/data/sparc_data/` | 999f94dfe |
| R_d, R_HI (NGC 3198 3.14 / 35.66 kpc; DDO 154 0.37 / 4.96 kpc) | `real_research/data/SPARC_Lelli2016c.mrt` | ef2e78c73 |

Systems: NGC 3198 (as CFG938) and DDO 154. DDO 154 is chosen here, before any number, as the record's standard gas-dominated SPARC
dwarf. Υ_disk = Υ_bul = 0.61 for both (CFG938's value).

## 3. Model (record equations only; no new constant)

**Field and mass.** Spherical weak-field limit of the CFG938 parent with stiffness off (L* → 0; declared, since L* ≥ 24 pc is far
below every cell radius; the stiffness-to-tether ratio in the global mode frequency is printed, report only).
- Baryons and light feel g = g_N + u, with u = G M_c(<r)/r² = χ′ (the medium's own potential gradient; χ is sourced by ρ_c only).
- The medium feels f = R(u) − g_N per unit mass, R(u) = u²/(a0 − u). The law is R(u) = g_N.

**Medium readings.** The record has no single settled dissipative law, so five record readings are run. None is invented.
- **M-I** (α = 0): ideal parent, r̈ = R(u) − g_N (CFG938 S3d). These are CFG747/776's dynamics with the full R(u) in place of
  the deep R = u²/a0.
- **M-D(α)**: overdamped record drift, ṙ = ατ(g − g_law(g_N)) (CFG541 FIX-1 / CFG638). τ = (4πGρ_m)^(−1/2), with
  ρ_m = ρ_b + ρ_ph,law of the current baryons at the marker's radius (declared smooth proxy).
- **M-ID(α)**: parent + record drift, ṙ = v + v_s, v̇ = R(u) − g_N.
- α ∈ {0.5 (galaxy-side floor), 1.186 (causality maximum)}. Readings: M-I, M-D(0.5), M-D(1.186), M-ID(0.5), M-ID(1.186).
- **MOND-I** (comparison only, not a framework reading): u = u_law(g_N(r, t)) at every instant.

**Baryons.**
- **B-F (primary):** after t = 0 the remaining stars and gas stay in place. This isolates the medium.
- **B-L (variant, report only, no class weight):** baryons as cold rotating shells, circular at t = 0⁻ (j² = r³g), with
  r̈ = j²/r³ − g. They feel g = g_N + u (framework) or g_law(g_N) (MOND-I). Run for M-I, M-ID(0.5) and MOND-I.

**Mass profiles.**
- Spherical-equivalent M_x(<r) = r V_x|V_x|/G per component, PCHIP in r between SPARC radii, ∝ r³ inside the first radius,
  constant beyond the last.
- Total M_b is made monotone by cumulative maximum (declared).
- **Blowout:** M_gas(<r) → (1 − f) M_gas(<r) at every radius at t = 0, with f ∈ {0.2, 0.5}. The removed gas leaves to infinity.

**Numerics.**
- N_c = 2000 Lagrangian medium markers, log-spaced from 0.02 R_d to 50 R_d. Each carries its enclosed mass μ_k = M_ph,law(r_k)
  of the original baryons. The mass inside 0.02 R_d is a fixed core (declared).
- Enclosed masses are recomputed by sorting at every force evaluation. Shell crossings are counted and reported; the
  single-stream EFT ends at a crossing (flag).
- Fixed-step RK4, dt = 0.02 × min local t_dyn at t = 0. T_max = 60 t_dyn(5 R_d) per system. Output every 0.02 t_dyn(2 R_d).

## 4. Definitions

- t_dyn(r) = r / V_c,0(r), with V_c,0 the law-state circular speed of the original baryons (= CFG638 K7's τ_ff for an SIS).
  t_orb = 2π t_dyn.
- Residual D(r, t) = log10[g / g_law(g_N)] in dex of g, with g and g_N at the same instant; D_V = D/2 is dex in V_c.
  - In B-F, D is also framework − MOND-I. Under MOND-I, D ≡ 0 by construction (identity).
- Recovery fraction F(r, t) = 1 − D(r, t)/D(r, 0⁺).
- t_50 = first sampled t with F ≥ 0.5.
- t_90 = earliest t with |1 − F(t′)| ≤ 0.1 for every sampled t′ in [t, T_max]. If the last sample fails, t_90 = "> T_max"
  (censored).
- **Lag L ≡ t_90**, in units of t_dyn(r).
- **Field part:** derived, not simulated. Φ is retarded at c (time r/c). χ is a medium-frame constraint whose source is ρ_c
  alone.

## 5. Verdict rules (frozen)

### V1. Lag class
Each reading has 16 cells: 2 systems × 2 footings × r ∈ {2 R_d, 5 R_d} × f ∈ {0.2, 0.5}, all B-F.

| class | rule |
|---|---|
| INSTANT | L ≤ 1 t_dyn in all 16 cells |
| FLOW-LIMITED LAG | L ≥ 2 t_dyn in all 16 cells (censored L counts as ≥ T_max) |
| SHORT LAG | 1 < L < 2 t_dyn in all 16 cells |
| MIXED | anything else; the cells are listed |

- **Overall class:** the common class of the five readings. If they differ, the overall class is **READING-DEPENDENT**, with
  each reading's class and the [min, max] of t_50 and L over cells.
- **Field part:** INSTANT if r/c ≤ 1e-3 t_dyn at every cell.
- **Named physics.** Each reading's clock must be the sympy one (check K3):
  - M-I: ω² = dg_N/dr + 2uR′(u)/r;
  - M-D: Γ = ατ·4πGρ_ph;
  - M-ID: s² + Γs + ω² = 0.

### V2. CFG763 / CFG764 relation
The same 16 cells per reading, with τ_resp ≡ t_50/ln 2 (the first-order clock with the same half-time).

**Per cell:**
- **CFG764:** CONSISTENT if k_min ≤ τ_resp/t_orb(r) ≤ 1.196, with k_min = 0.457 (canonical) or 0.525 (alt). FASTER below,
  SLOWER above.
- **CFG763:** CONSISTENT if τ_min ≤ τ_resp ≤ 3.474 Gyr, with τ_min = 0.724 Gyr (canonical) or 0.832 Gyr (alt). FASTER /
  SLOWER as above.

**Per reading:** CONSISTENT (all 16), INCONSISTENT-FASTER (all 16 FASTER), INCONSISTENT-SLOWER (all 16 SLOWER), else PARTLY
CONSISTENT (n/16).

**Text rule.**
- If a reading is INCONSISTENT-FASTER with a clock, that clock cannot be this reading's relaxation clock: **DIFFERENT PHYSICS**
  (formation/supply, not settling).
- If CONSISTENT, **SAME CLOCK POSSIBLE** in that reading.

### V3. Observability
- **Signal:** |D_V(r, t)| over the cells system × footing × f × r ∈ {2 R_d, 5 R_d, R_HI}, B-F.
- **Per reading:** OBSERVABLE if some cell has |D_V| ≥ 0.05 dex continuously for ≥ 100 Myr; else NOT OBSERVABLE.
- **Overall:** OBSERVABLE (ALL READINGS), OBSERVABLE (SOME READINGS: listed), or NOT OBSERVABLE.
- **Report only (no class weight):**
  - peak |D_V| and the time above 0.02 and 0.05 dex;
  - D_V(0⁺) closed form;
  - the gas fraction f* that would give D_V(0⁺) = 0.05 dex at DDO 154's R_HI;
  - the suppression of the peak by a gradual loss over T_loss for a first-order relaxer, (1 − e^(−ΓT))/(ΓT) (sympy);
  - the B-L variant.
- **Literature:** at most one WebFetch lookup (e.g. starburst or outflow durations), labelled PROVISIONAL, report only, never in
  a verdict.

## 6. Controls

- **K1 (static limit; identity flagged).**
  - (a) The parent equilibrium R(u) = g_N reproduces g_N = g²/(g + a0) at every SPARC radius of both systems, both footings:
    max |g/g_law − 1| ≤ 1e-12. R is built from the law, so this checks the code, not physics; as CFG938 K1.
  - (b) Unperturbed runs (f = 0), every reading and B-L: max |D| ≤ 1e-8 dex over T_max at all three radii.
- **K2 (Newtonian textbook mass loss).** Same RK4 shell code; test particle on a circular orbit about a point mass.
  - Impulsive δ = 0.2: apocentre/r0 = 1/(1 − 2δ) = 5/3 and radial period 2π a^(3/2)/√(G(1 − δ)M), with a = (1 − δ)r0/(1 − 2δ),
    each ≤ 1e-4 relative.
  - Impulsive δ = 0.5: specific energy 0 to ≤ 1e-12 (marginally unbound).
  - Adiabatic δ = 0.2, lost linearly over 300 initial periods: time-averaged final radius r0/(1 − δ) = 1.25 r0 to ≤ 2e-3.
- **K3 (clocks).** Single-marker linear tests at 2 R_d and 5 R_d of NGC 3198, canonical:
  - M-I: measured period vs 2π/ω, ≤ 0.5%;
  - M-D: measured e-fold rate vs Γ, ≤ 0.5%;
  - M-ID: measured complex root vs s² + Γs + ω² = 0, ≤ 1%.
- **K4 (convergence).** The NGC 3198 canonical f = 0.5 cells for M-I and M-ID(0.5) are rerun with one change at a time:
  N_c × 2, dt / 2, inner edge / 2, outer edge × 2. t_50 and uncensored t_90 must change by ≤ 5% or ≤ 1 output interval.
  Otherwise the affected reading's class is reported as UNRESOLVED.

**Main mode** exits 0 if K1–K4 pass, else 2. A failed check is reported as a failure, with no class changed after the fact.

## 7. MUTATE (WT06_MUTATE=1 → `wt06_MUTATE.out`, `wt06_results_MUTATE.json`)

| tooth | change | must FAIL |
|---|---|---|
| MU1 (remove the medium) | every framework reading replaced by MOND-I | the main-mode check "lag detected (t_50 > 0 in every reading)"; every class must read INSTANT |
| MU2 | R(u) → u²/a0 (deep tether, no wall) | K1a (law deviation at NGC 3198's high-g radii) |
| MU3 | drift sign flipped (v_s → −v_s) | K3's M-D clock check |

MUTATE exits 1 if all three teeth bite, 3 if any does not.

## 8. Compute and outputs

- One process, `OMP_NUM_THREADS=1 nice -n 10`, sympy/numpy/scipy.
- RSS guard 1 GB (peak via `/usr/bin/time -l`). Wall cap 60 min: if hit, stop, write partial outputs and disclose.
- No 1024³ work; another lane's run is live, so this stays a small job.
- Outputs: `wt06.py`, `wt06.out`, `wt06_results.json` (+ `_MUTATE`), `README.md`. Left uncommitted for orchestrator review.

## 9. Blindness disclosure

Read before freezing:
- CFG938's DERIVATION, README and K1;
- CFG638's README;
- CFG747's and CFG776's READMEs, including CFG776's D1 table: point mass, p = 1.5, m/r 1.051 at r = 2 r_M after 50 t0 and 0.992
  after 100 t0, with overshoot at 8–11 r_M;
- CFG763's and CFG764's windows;
- CFG889's ledger row (gated t_50 105–148 Myr/α);
- CFG955's README head.

Before freezing I estimated by hand only scalings (no code run, no cell number computed):
- M-I's linear frequency obeys ω t_dyn ≈ √(2 g_N/g) for a deep point mass;
- the drift e-fold is ≈ t_dyn/(α ρ_ph/ρ_m);
- D_V(0⁺) is ≈ 0.04 dex for 50% gas loss in a gas-dominated deep-MOND dwarf. This is near the 0.05 line, so V3 may read NOT
  OBSERVABLE. The 0.05 dex / 100 Myr threshold follows the lane brief's example and was not tuned to that estimate.

No WT-01 to WT-05 output was read.
