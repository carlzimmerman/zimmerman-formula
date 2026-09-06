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

## k02 — a global constraint of the sequestering type (`k02_global_constraint_average.py`, 3 FAIL of 4)

The one class of principle that removes an additive zero mode without choosing a constant is a global constraint (vacuum-energy sequestering): Λ becomes a Lagrange multiplier fixed by the spacetime average of the field Lagrangians. The only sector with scale a₀² is the MOND scalar, whose on-shell curl-free Lagrangian density is (2−K_B)a₀²F(s)/(16πG) with F = 2sΔ − j (deep MOND (4/3)s^{3/2}, linear beyond saturation). Against the cosmic peculiar-acceleration field (Maxwellian, rms 0.005–0.012 a₀ today, ∝ D/a²):

| check | result |
|---|---|
| G2 today | ⟨L_φ⟩/ρ_Λ = 0.6–2.3 × 10⁻⁵ (v_rms 300–600 km/s, K_B 0–0.25, both footings; a halo term at 100× its filling factor changes nothing) |
| G3 future | the spacetime average to 10 t₀ is 10⁻⁸ of the average to t₀: the de Sitter future drives it to zero |
| G4 regime | the scalar's Lagrangian equals ρ_Λ only at s* = 54–89 a₀; the universe averages 0.01 a₀ |

Closed on magnitude by five orders, independently of sign and of the O(1) convention.

## k03 — can the data separate ½ from the horizon coefficient? (`k03_half_vs_two_pi_precision.py`, 4 FAIL of 4)

k01–k02 leave one coefficient-free, right-sign, right-size identification: a₀ = c²/(2πL_dS), κ = √(8π/3)/(2π) = 0.461 (the Gibbons–Hawking/Unruh form; **not** Milgrom 1999's construction, which gives a₀ = 2cH_Λ and is excluded). It sits 8.5% (0.036 dex) from ½.

| check | result |
|---|---|
| P1 | 3σ separation needs 2.8% on a₀; the corpus BTFR mass-budget floor is 9.47% (a factor 3.3, and a floor, not statistics) |
| P2 | κ = ½ on Planck H₀ and κ = 0.461 on SH0ES H₀ predict the same a₀ to 0.2%: the coefficient is degenerate with the H₀ tension at fixed Ω_Λ |
| P3 | BTFR 0.465 ± 0.076 is 0.5σ from ½ and 0.1σ from 0.461; distance-free 0.551 ± 0.043 is 1.2σ and 2.1σ; combined ln LR = +1.4 for ½, undecided |
| P4 | Gaia DR4 gives 21% on a₀; 4.3% is needed for 2σ |

**Standing after k01–k03.** κ = ½ stays the frozen empirical target; the present action class cannot derive it (k01); the only zero-mode-removing principle of the global type misses by 10⁵ (k02); the one principle-shaped coefficient not excluded predicts 0.461, which the data cannot separate from ½ and which is degenerate with the H₀ tension (k03). The coefficient is a precision problem gated by the stellar M/L zero point, the absolute gas scale and H₀.
