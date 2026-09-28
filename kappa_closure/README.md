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

## k04 — the four-form promotion of a₀ (`k04_four_form_promotion_consistency.py`, 2 FAIL of 6; relayed construction, independent audit in the user's download)

Promote the MOND scale to a conserved four-form flux, a₀ = β√G|q|, with vacuum action P(q) = Zq²/2. The four-form's gravitating energy is the Legendre form ε = qP_q − P, so the k01 constant comes out **positive** (F1) and both a₀ and ρ_Λ are set by one flux: a₀ ∝ √(Gρ_Λ) becomes structural and the flux amplitude cancels, κ² = 2β²/(Z + 2bβ²). The half is then **Z/β² = 7.96**, a ratio of two couplings that nothing in the action fixes (F2). Feeding a₀(q) back into the four-form equation dL/dq = const makes a₀ environmental: in the saturated regime the equation is linear in q, a₀_loc = a₀(1 − g_N/155a₀), and above 155 a₀ = 1.4×10⁻⁸ m s⁻² the only solution is q = 0, so the scalar switches off (a kink of |q|).

| check | result |
|---|---|
| F3 galaxies | a₀ 1.2% low at the RAR knee, 64% low at 100 a₀; the RAR moves by < 0.002 dex (invisible) |
| F4 Solar System | the scalar is off inside 205 AU: the planetary sunward residual vanishes without the coherence length; the Cassini quadrupole is set at s ≈ 1 where a₀_loc = 0.997 a₀, so ξ is still required |
| F5 wide binaries | a₀ 15% low at 2 kAU (1.5 M☉): δγ_v = −0.019 canonical / −0.015 alt in the 2 kAU bin, about 1σ for DR4 |
| F6 stability | Z_eff > 0 everywhere |

**Standing.** The construction reverses the sign and turns the seesaw form into structure, at the price of an environmental a₀ that is invisible in galaxies and a 1σ effect for DR4. The coefficient is untouched: "why 32π" has become "why Z = 8β²". Not a derivation; the cleanest statement of the open problem so far.

## k05 — is 32π special? (`k05_is_32pi_special.py`; the main run exits 1 because H1 and H2 failed as declared; MUTATE flips the sign of Λ and H0 fails)

The question asked of the number itself, not of an action.

| test | result |
|---|---|
| S1 convention vs content (sympy, exact) | a₀ = κc√(Gρ_Λ) ⟺ Λℓ₀² = 8π/κ² ⟺ ρ_Λc² = a₀²/(κ²G). **Every π in "32π" is Einstein's 8π.** The only convention-free content is 1/κ² = 4: the vacuum energy density is exactly 4a₀²/G. The rewritings 8 × 4π/3 (Friedmann) and 2 × 16π (Einstein–Hilbert) are the same 4 in other conventions. |
| S2 the horizon reading (Schwarzschild–de Sitter, exact) | a₀ = c²/(2R*) with R* = √(8π/Λ) reads as a horizon's surface gravity, and its area gives AΛ = 32π², the Chern–Gauss–Bonnet constant. That horizon needs AΛ = 316. Every SdS horizon has AΛ ≤ 12π = 37.7, and black holes ≤ 4π (also the positive-Λ area bounds under the dominant energy condition). A horizon at R* would need M√Λ = −18.5. **H1 FAILED.** The SdS black hole whose surface gravity *is* a₀ is a near-Nariai hole (r√Λ = 0.905, 98.7% of the Nariai mass, AΛ = 10.3). |
| S3 the look-elsewhere census | k03's two measurements combine to κ = 0.530 ± 0.037. That is 0.8σ from ½ and 0.9σ from 1/√π, which is equally simple (Λℓ₀² = 8π²). 1/√3 (24π), √2/3 (36π) and √π/3 (72) lie within 1.6σ; 104 simple constants lie within 1σ. **H2 FAILED:** the data do not single out ½. |
| R2 the natural constructions on the vacuum | κ = 2.894 (the de Sitter horizon's surface gravity cH_Λ; its ratio to ½ is exactly Z = 5.789), 1.447 (the Hubble sphere as its own Schwarzschild radius), 0.461 (Gibbons–Hawking as Unruh, k03), 4.19 and 8.38 (a Newtonian ball of vacuum). **None gives ½**; the nearest is 0.461, 8% away. |

**Standing.**
- 32π has no geometric content beyond the integer 4.
- ½ is not the output of any natural geometric construction on the vacuum, and the data cannot select it among simple constants.
- The one-half can only come from dynamics, and k01–k04 show the present action class does not supply it.
- **κ = ½ stays FITTED.**
- One exact identity worth keeping: a₀ = c H_Λ / Z, with Z = 2√(8π/3) the ratio of the de Sitter horizon's surface gravity to a₀.
