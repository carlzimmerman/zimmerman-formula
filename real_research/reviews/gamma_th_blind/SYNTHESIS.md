# Γ_th blind run — synthesis & diff (DO NOT propagate until Carl confirms)

*C. Zimmerman, 2026-06-09. Workflow `we9md0q49` (3 independent methods: canonical UDW response / open-system FDT / forward numerics), launched BLIND — the agents derived Γ_th, the gates, and the lag model from first principles with Fable's first-pass numbers withheld from the prompt. **The run was killed in the verify/synth tail (the recurring hung-`StructuredOutput` agent issue), after all three finder methods completed and were saved.** This doc is the salvaged synthesis. Artifacts here: `FINAL_summary.json`, `lag_results_FRESH.json`, `eps_table.json`, the cosmology + Part-A/C audit scripts.*

## The diff against Fable's independent first pass — CONVERGES
| Quantity | Fable (1st pass, withheld) | Blind run (3 methods) | |
|---|---|---|---|
| Γ_th gapless | λ²H/2π² | **Γ_th(ω→0) = λ²H/(2π²) = λ²T_GH/π** (all 3 methods, sympy) | ✅ exact |
| Γ_th(ω) full | — | (λ²ω/2π)·coth(πω/H) (all 3) | ✅ |
| τ_c (bath correlation) | 1/H | **1/H** (Wightman e-folds at H; fitted 1.03 H) (all 3) | ✅ exact |
| ε_resp(z=3) | 0.60 | **0.596** | ✅ |
| a₀(3)/a₀(0) zero-lag | 0.737 | **0.737** | ✅ |
| a₀(3)/a₀(0) response gate | 0.649 | ~0.65–0.76 (gate/IC) | ✅ |

**Per the pre-registered rule, convergence on the decisive numbers → ledger.** Three independent blind derivations reproducing Fable's Γ_th = λ²H/2π² and τ_c = 1/H *exactly* is the strongest possible verification of those forms.

## The state-existence convergence (the one Fable specifically designed)
Fable's instruction: *"if the agents land on negative response without being told, that's the convergent verification."* **They did.** All three blind finders' Part-E independently conclude:
> **"NO standard calculation yields T ∝ √ρ_DE in the actual matter-dominated z=3 universe"** — the entire thermal structure (T_GH ∝ √ρ_DE, Γ_th, τ_c) is a property of **exact de Sitter** (Bunch-Davies), and at z=3 ρ_m/ρ_DE = 54.2 (Ω_DE(z=3)=0.018), so it is not the response of the real cosmological state.

This is the **structural** version of Fable's **operational** result (a comoving UDW detector in real ΛCDM has a *negative* quasi-stationary response at z=0,1,3 — deceleration, not finite age, flips the sign; the dS-truncation control stays positive). Two independent routes, same conclusion: **the standard-state cosmological temperature does not exist / does not track √ρ_DE at the redshifts the framework cares about.** The demotion is **symmetric** across footings (constant's strict-thermal reading also describes the attractor), and the **Deser–Levin a-dependence (the deep-MOND shape) is untouched** (local/kinematic, not comoving cosmological response).

## The lag band (the one mild divergence)
`FINAL_summary.json`: zero-lag = 0.737; band over (gate, IC): **derived-rates [0.37, 1.00]**, all-rates [0.05, 1.00]. Fable's band was [0.54, 1.00]. The blind run's **lower edge runs lower** (cold-IC + fast-gate extremes: G5 T_GH(2π/H) cold→0.40, G3 cold→0.49, the non-derived H_DE_repo rate→0.07). **Not decision-relevant:** the central prediction (response gate G1, adiabatic IC) is ~0.65–0.76, converging with Fable's 0.649; the z≈3 test is ~0.65–0.74 vs constant 1.0 either way. The lower-edge difference is the one place to reconcile if a *tight* band is wanted (it is the cold-start, fast-equilibration corner) — flagged, not silently averaged.

## Step-4 conditionality (carried explicitly by all three, per the working rule)
Every ε and lag number is conditional on the Step-4 posit (inertia tracks ΔT = T(a)−T(0)), which selects the gate and is NOT derived here; and on the monopole coupling λ, which the framework does not fix (the z=0 SPARC anchor only *forces* λ²≳7.3, it does not derive it). Combined with the state-existence negative: **the entire temperature-evolution apparatus sits downstream of an effective-law posit whose standard-state derivation is now computed and excluded.** Static MOND (Deser–Levin shape) stands; the evolution is a posited effective law, decided empirically at z≈3.

## Status
- **CONVERGENT → ledger-ready**, but **propagation HELD** (Prompt 3): no edits to `CONVENTION_LOCK.md` or the prediction tables until Carl confirms this diff. On confirm: relabel 0.737 as the zero-lag value (not "maximal decline"), record the response-gate ~0.65 and the band, relabel the adiabaticity verdict gate-dependent, update the z≈3 target string with the Step-4/gate conditionality.
- **Reliability tax:** the run was killed in the verify/synth tail by the recurring hung-`StructuredOutput` agent. The 3 blind finders + their saved scripts are the salvage; the verify/tiebreak/synth agents did not complete. A lighter output contract is needed for the next orchestrated run.
