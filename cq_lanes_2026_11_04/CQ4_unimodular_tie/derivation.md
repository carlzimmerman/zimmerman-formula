# CQ4_unimodular_tie: derivation

κ = ½ FITTED; not theory closed. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not blind. No
particle, no cold sector. Nothing here says the data favour the framework. Literature is from memory and PROVISIONAL.
Every equation below is checked in `cq4_unimodular_tie.py`; the check id is given in brackets. Criteria:
`FROZEN_CRITERIA.md` (1118e49b50).

## 1. The action

Signature (−,+,+,+). This is v3s (`covariant_push_2026_10_22/V3_FULL_PICTURE.md` §1) with its constant Λ promoted to the
Henneaux–Teitelboim multiplier [PROVISIONAL: Henneaux & Teitelboim 1989]:

    S_U = (c³/16πG) ∫ d⁴x { √−g [ R − 2 J(Y; Λ) + 2 K(Q) ] + 2 Λ ∂_μ B^μ } − (γ_L/2) ∫ √−g (D_i P^i)² + S_m
    J(Y; Λ) = Λ − 2 α² Λ [ u − ln(1 + u) ],   u = √(Y/(α²Λ)),   α dimensionless.

Λ(x) is a scalar and B^μ(x) a vector density. Nothing else is new. In v3s, J already carries the one constant:
J(0) = Λ and a_geo² = Λ/(32π), that is α² = 1/(32π). Form G is any MOND sector whose only scale is the multiplier,
J = Λ j(Y/Λ). A matter vacuum energy enters as S_m ⊃ −∫√−g ρ_v c². Below, Λ_v ≡ 8πGρ_v/c².

## 2. Field equations

- **B^μ:** ∂_μΛ = 0, exactly as in Henneaux–Teitelboim [K0a]. The tie leaves this untouched, because B enters only
  through 2Λ∂_μB^μ, whatever J is [E1]. Λ is a constant of integration.
- **Λ:** ∂_μB^μ = √−g ∂J/∂Λ|_Y [E2]. This is 1 − α²h(u) for form U [E3b], where
  h(u) = 2(u − ln(1+u)) − u²/(1+u) = u³/3 − u⁴/2 + … and h > 0 for u > 0 [E3c, E3d]. For form G it is j − y j′ [E3a].
  Without the tie it is the unimodular volume ∂_μB^μ = √−g [K0b]. The equation fixes only B's divergence. Three of B's four
  components are gauge [H1c], and B is not observed.
- **Metric:** 2Λ∂_μB^μ contains no metric, so it has no stress tensor [E4b]. −2√−g J(0) gives the cosmological term
  J(0) g_μν = Λ g_μν (Jacobi's formula [E5]; J(0; Λ) = Λ [K1b]). In vacuum, with matter's constant,

      G_μν + Λ_obs g_μν = (8πG/c⁴) T_μν,   Λ_obs = Λ + Λ_v.

- **Khronon and P:** at constant Λ these are v3s's equations [E4, checked on a stand-in field with Y = (∂φ)²].
- **Consistency:** ∇^μ(Λg_μν) = ∂_νΛ = 0 on shell. Matter's action is diffeomorphism-invariant by itself, so
  ∇^μT^m_μν = 0 on matter's shell. Separate matter conservation therefore holds, and Λ stays constant. This is a standard
  identity and the script does not re-derive it.

## 3. Static weak-field limit and the scale relation (gate S, G5)

On shell the theory is v3s with a_geo² = α²Λ, so the static law is v3s's simple-μ law, 1 + J′ = u/(1+u) [K1a]. That gives
a₀ = c² a_geo = α c² √Λ. Against the gravitating vacuum density ρ_Λ,obs = Λ_obs c²/(8πG):

    κ² ≡ a₀² / (c² G ρ_Λ,obs) = 8π α² Λ/Λ_obs = 8π α² (1 − ρ_v/ρ_Λ,obs)        [S1]

At α² = 1/(32π) and ρ_v = 0 this gives κ = ½ [S2]. **S PASS.**

- **G5a (form): PASS, no gain.** From G, c and Λ the only acceleration is a number times c²√Λ, with exponents
  (G, c, Λ) = (0, 2, ½). So once the multiplier is the only scale, a₀ ∝ c√(Gρ) follows without a choice. The record
  already lists the form as forced (root README, standing 2026-09-28).
- **G5b (number): FAIL.** α is a constant of the action that nothing varies, and ∂κ²/∂α ≠ 0. Promoting α to a field gives
  ∂J/∂α = −2αΛ h(u), which is zero only at u = 0 [G5b′]. That would remove the MOND sector everywhere. κ is a free
  normalisation, κ = √(8π) α at ρ_v = 0. This is the record's open piece in another form: ξ = 1, or premise A (KC1).
- **G5c (tie to the observed vacuum): FAIL.** ∂κ²/∂Λ_v = −8πα²/Λ_obs ≠ 0. a₀ is tied to the multiplier, not to the
  vacuum density that gravitates.

## 4. Renormalisation (C1): FAIL

- Without the tie, Henneaux–Teitelboim gravity plus a vacuum energy is invariant under Λ → Λ + δ, Λ_v → Λ_v − δ. The
  Lagrangian changes only by 2δ∂_μB^μ, a total derivative [C1a]. That is why only Λ_obs is physical in unimodular gravity,
  and why the split between multiplier and matter vacuum energy is a convention.
- The tie breaks this symmetry. ΔL minus the total derivative is 2√−g δ α² h(u) + O(δ²), nonzero wherever u > 0 [C1b],
  and a₀ moves with Λ. The split becomes physical: a₀ measures Λ = Λ_obs − Λ_v, not Λ_obs.
- **Window.** Holding κ within the record's ±0.099 dex (KC1, current primary measurement) needs
  −0.578 ≤ ρ_v/ρ_Λ,obs ≤ 0.366.
- **Size, as an illustration** [PROVISIONAL formula: one-loop Coleman–Weinberg vacuum energy in MS-bar for a Dirac
  fermion, ρ = −4m⁴[ln(m²/μ²) − 3/2]/(64π²)]. At μ = m_e the electron alone gives ρ_v/ρ_Λ = 2.6e31 on the canonical
  footing and 1.8e31 on alt, with ρ_Λc² = 4a₀²/G at κ = ½ (FITTED). It moves by 3.4e31 (canonical) and 2.4e31 (alt) per
  e-fold of μ. Keeping κ therefore needs ρ_v tuned to about one part in 10³¹, and the tuning moves with the scheme. This is
  the cosmological-constant problem: unimodular gravity had decoupled it from Λ_obs, and the tie moves it into a₀.
- v3s as written, with Λ a coupling constant inside J, has the same exposure: J's Λ and Λ_obs differ by any matter vacuum
  energy. The promotion neither creates the problem nor removes it.

## 5. Time dependence (C2, reported, not graded)

∂_μΛ = 0 exactly, so the tied vacuum has w = −1 exactly and a₀(z)/a₀(0) = 1 at every z. The tie does not let a₀ track an
evolving ρ_DE: any evolving component would be a separate field that the MOND sector does not see. A change of matter
vacuum energy at a phase transition shifts Λ_obs and leaves a₀ alone. CFG689
(`campaign_fresh_gravity/CFG689_native_ruler_bao/`) reads the native a₀(z)/a₀(0) = √X(z) from BAO as "flat within about
1σ, with a mild decline preferred" (P2 1.97σ–2.61σ; flatness-sensitive flag). The tie's prediction is the exactly flat
line. A decline confirmed past that would contradict the tie. Nothing is graded here.

## 6. Health

- **H1 PASS.** The velocity Hessian of (Λ, B^μ) is zero [H1a]: there is no kinetic term, so there is no sign to get wrong.
  The momentum conjugate to B⁰ is 2Λ [H1b], a first-order pair. B^μ → B^μ + ∂_νω^[μν] is a gauge symmetry [H1c]. That
  leaves no local degree of freedom and one global one (Λ, conjugate to the unimodular time) [PROVISIONAL: the
  Henneaux–Teitelboim count]. The tie adds no kinetic term to the khronon, so the parent's health is inherited, not re-run:
  V3W W4 (c_T = c and galaxy backgrounds PASS) and V3X W4c ((a) and (c) PASS; (b) UNDECIDED with no instability found).
- **H2 PASS.** δΛ = 0 locally on shell [E1], so there is no new long-range field.
- **H3 PASS.** 2Λ∂_μB^μ is metric-free, and the Λ-dependence of J enters with no derivative of the metric. The tensor
  sector is v3s's at β = 0, so c_T = c.

## 7. Against k04 (remark, not a gain on G5)

`kappa_closure/k04_four_form_promotion_consistency.py` tied a₀ to the four-form flux q. The four-form equation conserves
∂F/∂q, so q follows the local MOND invariant. In the MUTATE here, dq/dY = +0.030 at u = 1 with Z = 8β², which is the
mechanism behind k04's a₀_loc = a₀(1 − g_N/155a₀). Tying to the multiplier, the Legendre partner, removes that feedback
exactly [E1]. In both cases the coefficient stays free: Z/β² in k04, α here.

## 8. What a pass would need

G5b needs a principle that fixes α, which is KC1's ξ = 1 or premise A. G5c and C1 need the MOND scale to couple to the
total gravitating vacuum density, the coefficient of √−g summed over all sectors, and that sum is not a field. A local
version would take Λ_obs = (R + 8πGT)/4 on shell. That makes the MOND sector depend on curvature and on the matter trace.
The record's volume-form study (`sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/volume_form/REPORT.md`) found that a
local density-following multiplier either breaks separate matter conservation or changes the source sector. This lane
does not pursue it.
