# CFG378 FROZEN CRITERIA: two species, Newtonian gravity only, the cold fluid physically settled toward the phantom target

Committed alone, before any script.

**Why.** CFG366, CFG372 and CFG374 apply the reservoir rule as gravity-level BOOKKEEPING. The extra source is e − W_Rc·e, and the cold fluid is never moved. CFG366 found that 21–26% of the mass sits where the catchment would need more cold than is present (the "overdraw"). This lane builds the physical version.
- Real cold mass is moved toward the law's target.
- Gravity comes only from the real mass of the two species.
- Mass is conserved by construction, so an overdraw is impossible.

**The settling force is a DECLARED scheme. It is not derived.** The candidate mechanism is CFG373's khronon lapse channel, which is CONDITIONAL. κ = ½ is fitted. No dark-matter particle species is added: the cold species is the record's cold fluid, and its amount (Ω_c/Ω_b = 5.36) is still required, not derived. This is not "theory closed".

## Model (everything else is CFG374's engine, copied and not imported)

**Two species from the same ICs.** Each has NP³ lattice particles with identical initial positions and momenta. The masses are f_b = 0.157 (baryons) and 1 − f_b (cold). The ICs are EH no-wiggle at z_i = 49, seed 359, L = 200 Mpc/h: the only ΛCDM input. The background, step grid, kick-drift-kick integrator and CIC are CFG374's.

**Gravity.** Newtonian from δ_tot = f_b δ_b + (1 − f_b) δ_c. The baryon phantom is NOT added as gravity.

**Switch.** The T1 switch f(x) is CFG361's (ε = 0.077, τ = (Δ_ta(z) − 1)/3), evaluated on the total field.

**Target.**
- s_ph = −∇·[(ν_mono(|g_b|/(a·a₀)) − 1) g_b], with g_b = f_b ∇φ[δ_b], where δ_b is the BARYON particle field filtered by CFG374's MIX-A phase response:
  W(k) = 0.28/(1 + k²/k_J(1e4 K)²) + 0.54/(1 + k²/k_J(1e6 K)²) + 0.18.
- This is the engine's phantom source with δ replaced by the baryon species.
- In mean-matter units, the target is ρ_t = max(s_ph / (1.5 Ω_m / a), F), the law's dark density.
- The cold density is ρ_c = max((1 − f_b)(1 + δ_c), F).
- The floor is F = 0.01 (1 − f_b), one percent of the mean cold density.
- a₀ is A0-FLAT, on both footings: 9.3603e-11 and 1.1312e-10 m/s².

**Settling step.** Applied after every drift, to cold-particle POSITIONS only; momenta are unchanged. It is an overdamped JKO step.
- λ(x) = f(x) · [1 − exp(−Γ(x) Δt)].
  - Δt is the cosmic time across the PM step.
  - Γ(x) = g / t_dyn(x), with t_dyn = 1/√(G ρ_tot,phys(x)) from the mesh total density.
- The step relaxes ρ_c geometrically toward ρ_t: ρ_new = ρ_c^(1−λ) ρ_t^λ.
- It is realised by ONE linearised Monge–Ampère step, using log det(I + ∇∇ψ) ≈ ∇²ψ:
  - ∇²ψ = S − ⟨S⟩, with S = λ log(ρ_c/ρ_t);
  - each cold particle moves by u = ∇ψ (CIC-interpolated).
- Removing ⟨S⟩ makes the whole box the reservoir. Inflow toward a sink is the minimal-L2 (optimal-transport, linear-order) flow, with displacement falling as 1/r².
- **Declared safety cap:** |u| ≤ 1 mesh cell per step. The clipped fraction is reported.
- The step is two-sided, following the working model's ρ_c → ρ_ph: where ρ_c > ρ_t in ON cells, cold is pushed out. The ON-mass fraction with ρ_c > ρ_t is reported.

**Rate bracket. No scan.**
- g = 1 (Γ = 1/t_dyn): PRIMARY, the lane verdict.
- g = 0.1 (Γ = 1/(10 t_dyn)): its own verdict.

## Runs (frozen)

- 256³ particles per species, 256³ mesh, A0-FLAT.
- {g = 1, g = 0.1} × {canonical, alt} = 4 runs.
- Work data go to ../_external_data/cfg378_work/.
- Development runs at 128³ are labelled DEV and are not scored.
- S0 = ../_external_data/cfg359_work/cfg359_S0_FLAT_canonical_N256.json, read-only.

## Decision (CFG361's cuts verbatim; per footing; never pooled)

For each run vs S0 at z = 0, using the TOTAL-matter P(k):
- **GROWTH OK:** |σ₈ ratio − 1| ≤ 5% AND max over k ≤ 1 h/Mpc of |P ratio − 1| ≤ 10%, on BOTH footings.
- **TENSION:** the σ₈ shift is in (5%, 20%], or the P shift is > 10% with σ₈ within 20%.
- **FAIL:** the σ₈ shift is > 20% on either footing.

The lane verdict is set by g = 1. g = 0.1 gets its own verdict.

## Measured and reported (not extra cuts)

- **Realised fraction**, at z = 1, 0.5 and 0:
  - R = Σ f·min(ρ_c, ρ_t) / Σ f·ρ_t;
  - Q = Σ f·ρ_c / Σ f·ρ_t.
  - Both are compared with a g = 0 baseline (R₀, Q₀) from a g = 0 run at the same resolution (always at 128³ DEV; at 256³ only if that run is made, stated). The share of the deficit realised is (R − R₀)/(1 − R₀).
- **Overdraw:** the number of cold particles is constant; the min cold CIC density is ≥ 0; the overdraw is 0 by construction.
- **Settling speeds:** the rms and max |u|/Δt (km/s), and the clipped fraction.
- The σ₈ and P(k) of each species separately.

## Controls (`cfg378_checks.py`)

- **C1 mass conservation:** at every snapshot, the cold deposited total equals N_c to 1e-10 relative; the cold particle count is unchanged; min ρ_c ≥ 0.
- **C2 Γ = 0 reproduces S0:** at 128³, a two-species g = 0 run vs a single-species S0 run from the same engine at 128³. Requires |σ₈ ratio − 1| ≤ 1e-4 and max |P ratio − 1| ≤ 1e-3 at z = 0.
- **C3 step algebra:** on a 64³ test field, one settling step with λ = 0.2 everywhere must reduce Σ (log ρ_c − log ρ_t)² while keeping the particle mass total exact.
- **MUTATE** (CFG378_MUTATE=1, separate outputs named *_MUTATE): the target is multiplied by 10. At 128³, canonical, g = 1, the MUTATE run's z = 0 σ₈ must differ from the unmutated 128³ g = 1 run's by ≥ 1%.
  - The check script declares the settling "measurably active" only if this holds.
  - If it does not, that is disclosed as an insensitive scheme.

## Scope (declared before running)

- The settling scheme is declared, not derived. Momenta are not changed by settling (overdamped), so settled cold particles keep their prior velocities.
- The linearised Monge–Ampère step is first-order in S. Accuracy improves with small λ per step.
- The baryons are collisionless. Gas pressure enters only through the linear MIX-A filter on the phantom's source, as in CFG374.
- t_dyn uses the mesh-smoothed density (cell 0.78 Mpc/h at 256³), so Γ is underestimated in unresolved cores.
- Whole-box reservoir: there is no causal limit on supply distance beyond the 1-cell-per-step cap.
- The cold fluid is still required. κ = ½ is fitted.
