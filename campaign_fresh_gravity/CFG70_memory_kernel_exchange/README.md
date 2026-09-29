# CFG70 — the enclosed-mass exchange as a causal action with a memory kernel: a scoped NO

Script: `cfg70_memory_kernel_exchange.py` with `cfg70_common.py` (about 9 s; it reads CFG48's `Gcommon` and CFG44's `Bcommon` read-only). Outputs: `cfg70_memory_kernel_exchange.out` / `_results.json` and the MUTATE outputs (`_MUTATE_a`, `_MUTATE_b`, `_MUTATE`). Requested by the coordinating session; written by a delegated agent with the question, model and pass lines declared first, and re-run here. The main run exits 0 (18 of 19 checks; the one failed check is the reported N6); MUTATE a, b and the combined mode each exit 1 as required.

## The frozen question

CFG60's residual object is a nonlocal, causal, non-adiabatic exchange of energy between the baryons and the fluid, keyed to the enclosed mass. CFG48's G4 wrote it as a bilocal action term and found the reaction on the baryons 0.06–22 g_law (against a 0.10 line) and an energy demand of 23–50 times the baryons' orbital kinetic energy. Can it be written as a **causal action with a memory kernel** (a retarded Volterra term, through a Schwinger–Keldysh doubled-field action) such that (P1) the reaction is ≤ 0.10 g_law at every x in [0.3, 30] for M_b = 10⁹, 10¹⁰, 10¹² M☉; (P2) the energy supplied is ≤ the baryons' orbital kinetic energy (in CFG48's r_ta convention and B's committed r_ta); (P3) the kernel is retarded and the exchange reciprocal (derived from the action); (P4) no new untied constant beyond the kernel's own time scale?

## The action

Retarded cross term Γ(s) = 0 for s < 0; q the probe baryon shell, θ the fluid shell's heat per unit radius, θ^T the target thermal store:

    S = ∫dt { (m/2)(q̇₊² − q̇₋²) − m[Φ(q₊) − Φ(q₋)] − [F(q₊, θ₊) − F(q₋, θ₋)] } − ∬ θ_Δ(t) Γ(t − t′) θ̇_Σ(t′),   F = rθ + (c/2)(θ − θ^T(q))².

At Δ = 0 (sympy): m q̈ = −mΦ′ − ∂F/∂q for the baryon and r + c(θ − θ^T) + (Γ∗θ̇)(t) = 0 for the fluid; the Σ-equations vanish identically. The memory kernel is K̂(s) = 1/(1 + sΓ̂/c) with ∫K = 1 (Γ = γδ gives Newton relaxation). r is the fraction of the heat counted in the closed energy ledger (r = 1 energy-conserving; r = 0 an unspecified reservoir). The reaction on the baryon is a/θ^T_M = r Θ_K(t) + ε_c (Θ̄∗ṁ)(t). **In the static limit a → r θ^T_M, which at r = 1 is exactly G4's** (3/4)a₀ for the pressure-slaved target and (3/8)a₀(2 + x²)/(1 + x²) for the σ-slaved target (sympy residual 0; the forward-marching numerics agree to 10⁻¹¹).

## Verdicts

| pass line | verdict | numbers |
|---|---|---|
| **P1** reaction ≤ 0.10 g_law | **FAIL** | at r = 1 the late-time reaction is G4's for every kernel, every τ̄/t_f from 0.01 to 10 and every mass: a/g_law = 0.065 / 0.53 / 2.1 / 7.5 / 22.5 (pressure) and 0.062 / 0.40 / 1.2 / 3.8 / 11.3 (σ) at x = 0.3 / 1 / 3 / 10 / 30; the 0.10 line is crossed at x ≈ 0.38. It passes only in the open class (r = 0, more than 99.7% of the heat unfunded) or with an untied ε_c ≤ ε_max (0.30, 0.031, 0.0068, 0.0047 for τ̄/t_f = 0.01, 0.1, 1, 10). |
| **P2** energy ≤ ½ M_b V_f² | **FAIL, kernel-independent** | ∫Ė dt = f_real E_c and the static limit is the target. The ratio for M_b = 10⁹ / 10¹⁰ / 10¹²: **CFG48 convention 72.8 / 49.6 / 23.0; B's committed r_ta_law with ν_mono 318 / 179 / 57** (the P2 kernel 179 / 57, matching the referee). |
| **P3** retarded and reciprocal | **PASS as a structure** | on the discrete SK action the advanced dependence is 0 (limit 10⁻¹²; the same memory term without doubling gives 0.063); the cross block is symmetric; the reaction derived from F matches the action to 3.6 × 10⁻¹⁵. **The cost is that the derived reaction is G4's at r = 1.** |
| **P4** no untied constant | **FAIL** | no time scale is even required (τ̄ → 0 reproduces G4 to 10⁻¹²). Tied candidates (r/c, t_dyn(r_M), t_dyn(r_e) = 4.27 Gyr = 0.294/H₀, 1/H₀, c/a₀) none changes the static reaction. Passing P1 needs r ≪ 1 or ε_c ≪ 1, each an untied dimensionless coupling. |

## The failing hypothesis, exactly

**The heat delivered to the fluid is paid inside the closed baryon + fluid action (r = 1), with the coupling derived from the fluid's free energy (Onsager reciprocity). Under that, the reaction on the baryons equals CFG48's for every retarded kernel:** the memory kernel only reshapes the transient (an extra term ε_c times the lag). A no-go for this class, not for a fluid with an unfunded reservoir or an untied coupling.

## Reported, and caveats

- **N6 (added after the first run, reported only; its failing cell kept):** in the open class (r = 0) with ε_c = 1 and τ̄ = r_e/c, P1 is met in 5 of 6 (M_b, t_f) cells (peak 0.003–0.05 g_law) and fails at 10¹² M☉ with t_f = 1 Gyr (0.16 g_law); with τ̄ = t_dyn(r_e) it fails everywhere (10–20 g_law). P1 for the σ-slaved target is capped at 0.009 by the M → 0 start of the declared formation profile (θ^T_M ∝ M^(−1/2) diverges).
- Scope: a time kernel only, point-mass baryons, a probe-shell reaction. The spatial light-cone support t − t′ ≥ (r − u)/c is not built; the stability of the full coupled operator is untested; extended baryons are open. The targets, the quadratic F, the smoothstep formation profile and the kernels are postulated.
- MUTATE a (kernel symmetrised in time) fails the causality check (advanced dependence 0.26); MUTATE b (reciprocity term dropped) fails the reciprocity check (asymmetry 1.0); the combined mode fails both.

## Standing

**A causal, reciprocal memory-kernel action for the enclosed-mass exchange exists, and it gives CFG48's reaction and energy demand back.** The exchange cannot be made to pass by adding memory; it needs either an unfunded reservoir or an untied coupling below 1%. This is a scoped no-go for a time-kernel exchange inside a closed action. Nothing here says the theory is closed.
