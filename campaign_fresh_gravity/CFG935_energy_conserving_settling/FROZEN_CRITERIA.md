# CFG935 FROZEN CRITERIA: the minimal energy-conserving form of cold-energy settling

Date: 2026-10-20. Block CFG930–939 (ledger row "CFG930–939 RESERVED", reservation commit 4e4f0f5e4: "CFG935 energy-conserving
repair of the record's settling equation (CFG932 Q1 found it non-conserving)"). This file is committed ALONE, before any CFG935
script exists and before any CFG935 number has been computed. It is never edited; post-hoc changes go into dated, labelled
amendments in the README.

Settings: κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m s⁻², never pooled: every physical number is
computed and reported per footing. The 1-D tests are in G = a₀ = 1 units, where the footing does not enter (it only sets the
unit of length and time); the footing enters only the physical tables of §6. "Cold energy" throughout; its mass is required;
no particle species. Not "theory closed". Nothing here may say the data favour the framework. Framework-native inputs only.

## 0. Disclosure: what was read and seen before this file

- **Record read (read only):** CFG932 README, DERIVATION, FROZEN_CRITERIA, `cfg932.py` (the Q1 `drift_test`), its JSON keys;
  CFG638 README; CFG542 ACTION + README (Pb, Pb*, Pc1, Pc2, K10); CFG544 README head + kinetic-gate rule; CFG639 / CFG641 README
  heads; CFG747, CFG776, CFG889 READMEs; CFG760 / CFG761 README heads and the CFG762 ledger row; CFG630 README + JSON brackets;
  the CFG689 and CFG748 / CFG882 ledger rows; THEORY_CANONICAL 10-14 S2/S3 (the one-field action and "the law is a two-sided
  attractor"); MASTER_COLD_ENERGY_EQUATIONS.md Supplements C and F (another agent's file, read only). LEDGER.md has no ZAR-09-CL
  row (targeted grep); nothing else was searched.
- **Record numbers seen (they shape the expectations below):** CFG932 Q1 two-sided drift test ΔW/|W₀| = +0.5927, identity
  1.86e-3; CFG932 Q2 whole-catchment ΔE_tot < 0 for every system (settling releases energy); CFG544: drift-only release 0.77–1.01
  V_f² per M_cat, FIX-2 reheating needs 0.51–0.71, whole-history net 0.26–0.31 (the books close only if the dark-energy exchange
  runs both ways); CFG747 / CFG748: collisionless tether shells put the inner halo on the law (0.2–1.7%) with escaped mass
  0.22–2.07 M_b and outer deficits, K2 ≤ 1.6e-4; CFG776: surpluses are expelled and overshoot; CFG630: settling feeds dark
  energy at Δρ_DE/ρ_DE ≈ 0.80–1.10e-6 (can) / 0.92–1.25e-6 (alt) since z = 1, below sensitivity; CFG689: constant dark energy
  not rejected (1.97σ primary); CFG760–762: the record's P field has a mass gap, P radiation is closed as an infall export channel;
  CFG542 Pc2: a healthy local scalar mediator of ψ gives static energy −F (settling reverses).
- **Hand reasoning done before this file (no code, no number from a CFG935 calculation):**
  - (H1) An exact energy theorem: in a closed system the law can be the end state only if the initial energy equals the law
    state's energy, or if the excess leaves (escaping cold energy, a partner, radiation).
  - (H2) In the canonical S2 action the potential energy of the cold energy at fixed mass is pointwise convex in the enclosed
    mass m(r), so the settled law profile min(m_law, M_c) is its unique minimum (the cold, static ground state).
  - (H3) For the Newtonian (CFG638-type) energy with one-sided settling, every stationary profile with m ≥ m_law inside the
    occupied radius is more bound than the Jeans-supported law, so an initial state with more energy than that law has no bound
    one-sided stationary state at all.
  - (H4) For a Hamiltonian version of FIX-1 (energy λF), the heat released is ∝ λ, as is the stiffness, so the heated
    equilibrium's deviation from the law may not shrink with λ; and the baryons feel a reaction force whenever ψ ≠ 0.
- **Expectations (disclosed, not verdict inputs):** R-d conserves by construction and keeps the record's equilibrium (its
  cost is a dynamical dark energy); R-c's channel is closed by CFG760–762 for the record's own field; R-b fails on the infall
  start unless mass escapes; R-a(ii) (canonical S2) lands on the law in the inner halo with escaped mass, as CFG747/748 did;
  R-a(i) may fail through retained heat or the baryon reaction. This lane is therefore NOT blind.

## 1. Question and candidate repairs

The record's settling (CFG638 = CFG541 E3 drift + CFG544 FIX-2 bath; FIX-1 two-sided ψ, CFG541 E5 one-sided, CFG639 gated) obeys
d(K_c + K_b + W)/dt = P_drift + P_bath (CFG932 Q1). A repair must (a) conserve total energy exactly with every source and sink
booked; (b) keep ρ_c = ρ_ph as an equilibrium of an isolated settled galaxy; (c) reduce to the record's tested behaviour
(inward infall and deficit fill reach the law) and keep the record's passes (the law in rotators: baryons feel exactly g_law
at equilibrium; the shear-pass engine's one-sided source: deficit fill complete, surplus removal not required where resolved).

Candidates (all tested on the same 1-D spherical toy, §2):
- **R-a, Vlasov plus a settling potential in the Hamiltonian** (the released infall energy goes into cold-energy motions):
  - **R-a(i), Hamiltonian FIX-1:** H = K + W_N + λF, F = (1/8πG)∫_{r<R_C}|∇ψ|², ∇²ψ = 4πG(ρ_ph − ρ_c) (FIX-1's own functional,
    CFG544; minimised by the inside-out fill, CFG541 V4). Force on cold energy −λ∇ψ. New dimensionless constant λ (primary
    λ = 10, variant λ = 100) and an unestablished mediator (CFG542 Pc2). Newtonian self-gravity (G9).
  - **R-a(ii), canonical S2 tether (THEORY_CANONICAL S2/S3):** the static on-shell energy of the S2 action in spherical symmetry,
    V_S2 = Σ μΦ_b(r_i) + ∫4πr² W_rem(G m(<r)/r²) dr, K W_rem′(u) = u²/(a₀ − u) (cold self-gravity cancelled by the tether; baryons
    feel g_b + g_c). No new constant. The stiffness term (γ/2)|∇P|² is neglected (L* ≪ the toy's scales; disclosed).
- **R-b, one-sided settling with booked heat:** N-type gravity + the record's one-sided drift (CFG541 E5, v_s = −ατ∇ψ, ∇²ψ =
  4πG max(ρ_ph − ρ_c, 0) on B∩C), with the drift's exact energy change booked as cold-energy heat. No bath target (σ_J removed).
- **R-c, explicit radiation channel:** R-b plus one-way cooling of cold-energy motions above the record's Jeans target σ_J²
  (FIX-2's target), at FIX-2's rate 2α/τ, into a declared radiation reservoir E_rad. Outward pushes cannot be fed by radiation,
  so R-c is one-sided. Record check: CFG760–762 (P gap).
- **R-d, exchange with an evolving dark energy (CFG542 Pb):** the record's two-sided drift (FIX-1) and FIX-2 bath unchanged,
  with both energy changes booked to a dark-energy partner E_DE (Q = −ρ_c v_s·∇Φ plus the bath term). Allowed only if ρ_DE is
  dynamical. Size compared with CFG630 and CFG689 (§6).

## 2. The 1-D spherical toy (identical for every repair)

- Units G = a₀ = 1. Static Plummer baryons M_b = 1, a = 1. Law: simple ν (the task's g_N = g²/(g + a₀)),
  ν(y) = ½(1 + √(1 + 4/y)), y = G M_b(<r)/(r² a₀), M_ph(<r) = M_b(<r)[ν(y) − 1]. Settled edge r_* = 10, so M_c = M_ph(<10).
  Catchment (mobility / settling region) R_C = 30. α = 1. τ = (4πGρ_m)^(−1/2), ρ_m = ρ_b + ρ_c (binned).
- Cold energy: N = 10000 equal-mass shell particles (μ = M_c/N) with (r, v_r, L), L the specific angular momentum. Enclosed
  cold mass at a particle: m_in = μ(k + ½), k = number of particles strictly inside (thin-shell rule).
- **N-type gravity** (R-a(i), R-b, R-c, R-d): V_N = Σ μΦ_b(r_i) − G Σ μ m_in,i / r_i; force −μG[M_b(<r) + m_in]/r².
- **S2-type** (R-a(ii)): V_S2 above, evaluated in closed form between sorted radii (m piecewise constant); force on a particle =
  −μ g_b + (r²/G)[w(G(k+1)μ/r²) − w(Gkμ/r²)], w(u) = −u²/2 − a₀u − a₀² ln(1 − u/a₀) (the exact step derivative).
- **λF** (R-a(i)): F = (G/2)∫_0^{R_C} [M_ph(<r) − m(<r)]²/r² dr evaluated exactly between sorted radii; force on a particle
  inside R_C = −λGμ[M_ph(r) − m_in]/r².
- **Drift** (R-b, R-c, R-d): positions move by v_s dt at fixed v_r and L (the record's drift sub-flow; CFG889 convention).
  Two-sided (R-d): v_s = −ατG[M_ph(r) − m_in]/r² per particle (FIX-1, exact). One-sided (R-b, R-c): v_s = −ατG M_d(<r)/r² with
  M_d the cumulative of d_b = max(ΔM_ph,b − M_c,b, 0) on 40 log bins from 0.05 to R_C (plus an inner bin), linearly interpolated.
  No drift beyond R_C.
- **Jeans target** (R-c, R-d): isotropic Jeans pressure of the binned cold density in the N-type total field,
  p_J,b = Σ_{b′>b} ρ_c,b′ g_b′ Δr_b′ + ½ρ_c,b g_b Δr_b, σ_J,b² = p_J,b/ρ_c,b. Bath on the 3-D dispersion about the bin's mean radial
  velocity, s3² = ⟨(v_r − v̄_r)²⟩ + ⟨L²/r²⟩: s3² → 3σ_J² + (s3² − 3σ_J²)e^{−2γdt}, γ = α/τ_b, by scaling (v_r − v̄_r) and L. R-d two
  way; R-c only where s3² > 3σ_J².
- **Heat booking** (R-b, R-c): after each drift substep the exact matter-energy change ΔE_d (kinetic incl. L²/2r², plus V_N) is
  computed; Q = −ΔE_d is injected into the radial velocities of the drifted particles with weights ∝ μ|v_s||a| (v_r → ±√(v_r² +
  2q/μ), sign kept, random if v_r = 0); if Q < 0 it is removed by scaling their v_r (then L) by a common factor. Exact by construction.
- Integrator: kick-drift-kick on the Hamiltonian part with a global adaptive step; reflecting inner boundary at r_min = 0.01; no
  outer boundary (cold energy may leave). Numerical knobs (step constant, r_min) are implementation choices, set only on the K2
  integrator check, and disclosed.

**Initial states** (positions by deterministic quantiles of the cumulative profile; RNG seed 935 for velocities / signs):
- **IC-L (settled galaxy, control):** the law profile to r_*. N-type: isotropic Maxwellian velocities with the isotropic Jeans
  dispersion of the law in the N-type field (approximate equilibrium). S2-type: cold, at rest, each particle placed at its exact
  discrete static equilibrium (force zero to ≤ 1e-10 relative).
- **IC-I (infall / deficit fill):** uniform sphere of radius 15 holding M_c (cumulative deficit everywhere inside r_*), v_r = 0,
  L = 0.05 r v_c,N(r) with v_c,N² = G[M_b(<r) + m_IC(<r)]/r.
- **IC-S (surplus core, CFG776-like):** m_IC(<r) = min(1.5 M_ph(<r), M_c) (cumulative surplus everywhere inside r_*), same
  velocity rule as IC-I.

**Runs:** each repair on IC-L (t_end 200), IC-I and IC-S (t_end 400); R-a(i) at λ = 10 on all three plus λ = 100 on IC-I.
Samples every Δt = 1. Windows W1 = [0.50, 0.75] t_end, W2 = [0.75, 1] t_end.

## 3. Measures

- **Energy:** E_tot = K + V (+ λF) (+ E_rad or E_DE). Conservation error ε_E = max_t |E_tot(t) − E_tot(0)| / E_ref, with E_ref =
  the sum of the absolute values of the energy components at t = 0.
- **Law gate (the record's CFG544 kinetic-gate density part):** D = median over 16 log bins in S = [0.1, 0.9] r_* = [1, 9] of
  log10(ρ̄_c/ρ_ph), ρ̄_c the W2 time-averaged binned density. ON THE LAW iff |D| ≤ 0.1 AND |D(W2) − D(W1)| ≤ 0.05.
- **Reported, no gate weight:** X_m = max over r ∈ {2, 5, 8} of |log10(m̄(<r)/M_ph(<r))| (the rotation-curve offset scale);
  f_esc = fraction of M_c beyond R_C at t_end; for N-type the virial ratio X = Σ v²/3 / Σ σ_J²(r_i) over particles in S (W2);
  energy flows (heat booked, E_rad, E_DE net and gross).
- **Baryon reaction (R-a(i) only):** a_b(r) = λψ′(r) ∂M_ph/∂M_b|_r, ψ′ = G[M_ph − m̄]/r², ∂M_ph/∂M_b = ν − 1 + yν′(y), from the W2
  averages; reported as max over r ∈ {2, 5, 8} of |a_b|/g_law. For every other repair the baryons feel only g_b + g_c by
  construction (stated in DERIVATION).
- **Energy theorem numbers (§5 of DERIVATION, computed in the script with the toy's discretisation):** E_init(IC) per type;
  E_law(M) = energy of the settled law with mass M (N-type: W_N + isotropic Jeans K; R-a(i): plus λF_min(M); S2: V_S2 of the cold
  profile min(m_law, M)); f_min = 1 − M_rem/M_c solving E_law(M_rem) = E_init (marginal escape) when E_init ≥ E_law(M_c);
  otherwise the energy deficit E_law(M_c) − E_init is reported (the law is unreachable without an energy input).

## 4. Class rules (per repair)

- **(a) CONSERVES:** ε_E ≤ 1e-3 in every run of the repair AND the derived energy equation books every source and sink to a
  named, existing or declared reservoir. A repair whose reservoir is excluded by the record (R-c with the record's gapped P field;
  R-d with exact Λ) passes (a) only with a declared new field, which makes it at best VIABLE-WITH-COST.
- **(b) LAW IS AN EQUILIBRIUM:** IC-L is ON THE LAW.
- **(c) RECORD'S BEHAVIOUR AND PASSES:** IC-I is ON THE LAW (inward infall / deficit fill reaches the law) AND the baryon
  reaction (R-a(i)) is ≤ 0.1 g_law at r ∈ {2, 5, 8}. IC-S is reported (the record is split on surpluses: one-sided retains,
  FIX-1 and the S2 push expel) and carries no class weight.
- **VIABLE:** (a), (b), (c) with no new field or constant. **VIABLE-WITH-COST:** (a), (b), (c) only with a new field or constant
  (named). **NOT VIABLE:** any of (a), (b), (c) fails.
- **Overall:** REPAIR FOUND if at least one repair is VIABLE; REPAIR NEEDS NEW PHYSICS if none is VIABLE and at least one is
  VIABLE-WITH-COST; NO REPAIR otherwise. The README states plainly what the overall class means for "the law is the settled state",
  with f_esc and f_min: a repair that reaches the law only by unbinding part of the supply is reported as such.

## 5. Controls

- **K0:** a verbatim copy of CFG932's `drift_test(two_sided=True)` reproduces ΔW/|W₀| = 0.5926642444000018 and identity_rel =
  1.8633353183663936e-3 to ≤ 1e-9 relative. **K0b:** the same run with exact discrete-gradient bookkeeping (the partner takes the
  exact potential-energy change of each step) closes W + E_X to ≤ 1e-12 |W₀|.
- **K1:** the IC-L runs (criterion (b)); plus the S2 discrete static state's force residual ≤ 1e-10 relative at t = 0.
- **K2:** pure N-type Vlasov (no settling term) on IC-I to t = 200: ε_E ≤ 1e-3 (integrator check).
- **MUTATE** (separate run, `CFG935_MUTATE=1`, outputs `_MUTATE`; t_end 100): M1 R-d on IC-I with the partner booking off →
  matter energy |ΔE|/E_ref ≥ 1e-3; M2 R-b on IC-I with the heat booking off → ≥ 1e-3; M3 R-a(ii) on IC-I with the tether energy
  left out of the books (E = K + Σ μΦ_b) → ≥ 1e-3. The MUTATE run exits 1 when all three bite (record convention).

## 6. Physical tables (both footings, no class)

From CFG932's committed JSON (central corner EPS 0.05, L = 1, per footing): the excess energy E_x = −ΔE_a,tot (self-consistent,
whole catchment) per system in erg, E_x/(M_cat c²), and the minimum escape fraction for an N-type repair with retained heat,
f_min ≈ E_x/(M_cat |Φ(r_*)|), |Φ(r_*)| = G(M_b + M_cat)/r_*. From CFG630's committed JSON: the cosmic exchange R-d needs
(Δρ_DE/ρ_DE since z = 1, per footing) and the matching radiated energy density for R-c, compared with CFG689's constant-DE result.

## 7. Execution limits (a 1024³ job may run beside this lane)

One process at a time, OMP_NUM_THREADS=1, nice -n 10, < 1 GB. Run order: K / MUTATE first, then main. Outputs: `cfg935.py` →
`cfg935.out`, `cfg935_results.json`; MUTATE → `cfg935_MUTATE.out`, `cfg935_results_MUTATE.json`. Every quoted number comes from a
JSON. κ = ½ FITTED; footings never pooled; not theory closed.
