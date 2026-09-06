# kappa_closure — can the action relate a₀ to Λ?

**Rule of the branch (2026-09-06):** no mechanism counts unless a₀ and Λ begin independent and the equations remove one degree of freedom. No 32π in a coupling, no vacuum constant chosen after integrating, no convention changes. The empirical target is a₀ = ½ c√(Gρ_Λ), i.e. Λℓ₀² = 32π with ℓ₀ = c²/a₀; measured κ = 0.465 ± 0.076 (BTFR) and 0.551 ± 0.043 (distance-free); the footings are κ = ½ (canonical) and 0.602 (alt).

## k01 — zero-mode theorem and the Λ-free vacuum (`k01_zero_mode_theorem_and_lambda_free_vacuum.py`, 3 FAIL of 6 checks, all against the framework)

| check | result |
|---|---|
| K1 statics | the static field equations contain the MOND primitive J only through J′: J → J + C is a symmetry (sympy, generic J) |
| K2 FLRW | the background sees only Λ_eff = Λ + (2−K_B)J(0)/2 + K(Q₀)/2; with Λ explicit and free **no equation of the action relates a₀ to Λ** (outcome 3, proven) |
| K3 Λ-free, sign | delete Λ and fix the primitive's zero by an empty Newtonian vacuum: the background vacuum energy is **negative** for both kernels, both K_B, both footings (the scalar's gradient term carries the attractive sign, so its primitive rises toward the Newtonian end) |
| K4 Λ-free, size | its magnitude is 0.4–0.7 % of ρ_Λ (ν_RAR; 0.06–0.1 % for the carrier); the needed J(0) is 100 a₀² against the primitive's whole span 0.45 a₀² — a factor 220 |
| K5 QUMOND reading | the constant 4π⁴/15 of the ν_RAR primitive is what the **unsaturated, non-monotone branch** returns (2∫s dΔ = −4π⁴/15; −2 for the carrier), the branch the bounded-boost theorem forbids; read as the vacuum energy anyway it gives κ = 0.98–1.05 (≥ 6.8σ) for ν_RAR and 3.5 for the carrier |
| K6 guard | the coefficient needed for κ = ½ is 7.7 against the action's (2−K_B) ∈ [1.75, 2]; (2−K_B)² gives 0.70–0.80; no term of the action supplies it — recorded so that no factor is adopted by hand |

**Conclusion.** κ = ½ is an empirical boundary condition that this class of local MOND actions cannot derive. A derivation needs a structure outside the present action: a principle that fixes the absolute zero of the scalar's primitive **and** reverses its sign relative to the gradient term. The dark-sector completion hunt is frozen while this stands (relic dead in g04i; four condensate doors dead in g03w–g03z).
