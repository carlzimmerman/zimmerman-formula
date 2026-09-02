# a₀² = G V(χ)/4 from the condensate action — VERDICT (2026-09-01)

**Asked:** derive the promotion coefficient, a₀² = G V(χ)/4 (⟺ κ = ½ ⟺ a₀ = c²√(Λ/32π)), from the condensate
action itself, with a committed script.
**Script:** `a0_from_condensate_action_2026.py` (rc=0, 25 checks; `MUTATE=1` breaks B1 → rc=1, so the checks are live).
**Action used:** THE_COMPLETION v9 = THE_GENERALIZED_COMPLETION — MOND term (a₀²(Q)/8πG)·G(√Y/a₀) with the exact
exponential primitive G(y)=y²+2(1+y)e^{−y}−2, condensate K(Q)=−M⁴√(1−μ²(Q−Q₀)²/M⁴) with −K(Q₀)=M⁴=ρ_Λ, and the
promotion a₀²(Q)=α·G·(−K(Q)). CDE-L4C's V(χ) is −K(Q) here.

## What IS derived
- **The FORM.** a₀² = α·G·V is the unique promotion from {G, c, V}: exponent matrix det = 2, solution (1, 0, 1), so
  **no power of c enters and α is a pure number**. Negative control: admitting the condensate's Helmholtz mass μ
  turns it into a one-parameter family (nullspace dim 1) — the form is forced only under "no new dimensionful
  scale in the promotion", which is exactly the v9 assumption.
- **The pressure route** (stage 17 re-verified): −K(Q) decreases with excitation (a₀ falls into the past, MOND off
  at recombination) while ρ_Q increases (density promotion would switch MOND on at the CMB).

## What is NOT derived — and provably cannot be from this action
**Modulus theorem (by exhibited family).** Every established consistency condition of the v9 action is α-independent:
| condition | why α drops out |
|---|---|
| FLRW background | Y=0 on FLRW and G(0)=0 ⇒ the MOND term vanishes identically |
| no-ghost / gradient health | λ_⊥ = 1−e^{−y} > 0, λ_∥ = 1+(y−1)e^{−y} > 0; α enters only as the positive prefactor a₀² |
| promotion feedback on Q | d(a₀²)/dQ = −αGK′(Q) = 0 on the vacuum branch (w = −1 exact survives); off-vacuum ∝ the charge |
| c_T = 1 | the MOND term is algebraic in the metric (through Y) |
| Bianchi / γ_PPN = 1 | minimal single-metric coupling; α only rescales the MOND radius r_M ∝ α^{−1/4} |

So the action is consistent for **every α ∈ (0, ∞)**: α = κ² is a free modulus. No calculation internal to the action
can output ¼. Only a postulate from outside the action can, and this is what the candidates give (canonical footing,
ρ_Λ = Ω_Λρ_c; measured κ = 0.465±0.076 BTFR, 0.551±0.043 distance-free):

| postulate | α = κ² | κ | a₀ [m s⁻²] | verdict |
|---|---|---|---|---|
| P1a the MOND kernel's own regime offset (exactly 2 in units a₀²/8πG, constant-independent) IS ρ_Λ | 4π | 3.545 | 6.64e−10 | **EXCLUDED ~7×** |
| P1b with the repo's G(0)=0 the kernel carries no FLRW vacuum energy | — | — | — | ρ_Λ must be the separate M⁴ ⇒ α free |
| P2 de Sitter surface gravity a₀ = cH_Λ | 8π/3 | 2.894 | 5.42e−10 | **EXCLUDED ~5.8×** |
| P3 Gibbons–Hawking temperature a₀ = cH_Λ/2π | 2/3π | 0.461 | 8.63e−11 | allowed (just below band) |
| P4 Friedmann identity a₀ = cH_Λ/Z, Z² = 32π/3 | ¼ | 0.500 | 9.36e−11 | identity, no content |
| P5 surface gravity of L_Λ = c/√(Gρ_Λ), a₀ = c²/2L_Λ | ¼ | 0.500 | 9.36e−11 | allowed, but L_Λ is not in the action (dS horizon is L_Λ√(3/8π)) |
| P6 Jeans 1/√π | 1/π | 0.564 | 1.06e−10 | allowed, not in the action |
| P7 cuscuton FLRW 3μ_c²H = −V′ | — | — | — | re-introduces the same free κ_H |
| P8 DBI-wall μ²Λ_D² = M⁴ | — | — | — | a₀-blind |

Three readings (0.461, 0.500, 0.564) sit inside the data band and the data cannot separate them (~8% precision floor,
κ error budget); the action cannot either. **κ = ½ stays FITTED.** The kernel's regime modulation of the vacuum energy
at κ = ½ is κ²/4π = 1/(16π) ≈ 2% of ρ_Λ — a real, small, computable effect, not a derivation.

Alt footing (the same ¼ on ρ_total): a₀ = 1.13e−10.

## What would count as a derivation — EVALUATED the same night
The graviton-bath CTP nonlinear drift was the only lane where a rational κ was the right kind of number. It is evaluated in
`graviton_bath_ctp_drift_2026.py` / `GRAVITON_BATH_CTP_VERDICT.md`: the drift exists, ⟨g₂h_uu²⟩ = m(n/12π)ℓ_P²(a²+c²H²), but every
Λ-dependent term is O(ħ) (theorem: T_GH ∝ ħ), its size is n/(6S_dS) ≈ 5e−124 of the de Sitter acceleration, it is ∝ r, and it has no
MOND shape (f = T² ⇒ q = 0). **Every named derivation lane for κ = ½ is now closed.** "a₀² = GV/4" is a constitutive relation with
one fitted number, 0.465–0.551, and must be cited that way. Layer A untouched.
