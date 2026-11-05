# CQ4_unimodular_tie: FROZEN CRITERIA (committed alone, before any derivation or script)

κ = ½ FITTED; not theory closed. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not blind (the
author knows the record's κ results). No particle, no cold sector; nothing here reinstates the retired cold sector. Nothing
here says the data favour the framework. Literature is from memory and PROVISIONAL; no web search, no downloads.

## Question

Gate G5 of `rebuild_2026_10_22/AX1_action_for_law/` ("a₀ ∝ √(Gρ_DE) from the action") is by hand in every class AX1 graded.
In unimodular gravity in the Henneaux–Teitelboim form [PROVISIONAL: Henneaux & Teitelboim 1989; record entry
`citations/works/henneaux-1989-the-cosmological-constant-and-general-covariance.md`], Λ is a field Λ(x) whose equation,
from a Lagrange-multiplier vector density B^μ, makes it a constant of integration. CQ4 asks whether letting the SAME
constant set the MOND sector's kinetic scale makes a₀ = κ c √(G ρ_Λ) come out of the action, and what fixes κ.

## Record check (done before freezing)

- `kappa_closure/k04_four_form_promotion_consistency.py`: a₀ tied to a four-form FLUX q (a₀ = β√G|q|, P(q) = Zq²/2).
  Found the form structural, κ² = 2β²/(Z + 2bβ²) a free coupling ratio (F2 FAIL), and environmental feedback
  a₀_loc = a₀(1 − g_N/155a₀) because the conserved quantity is ∂L/∂q, not q (F3).
- `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/volume_form/REPORT.md` §4: a₀ tied to the unimodular VOLUME
  (V₀ = v★ χ^(−d)); an Euler reaction is forced and the ratio is still chosen by v★ or u.
- `kappa_closure/k02_global_constraint_average.py`: the reverse direction (sequestering, ρ_Λ = η⟨L_φ⟩); closed on
  magnitude by five orders.
- KC1 (`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CLOSURE_2026-11-03.md`): every route reduces to ξ = 1,
  a length exactly c/√(Gρ) (premise A), which no field equation supplies. KF1
  (`rebuild_2026_10_22/KF1_argon_kappa_routes/`): κ = 1/(2ξ), nothing forced.
- v3s (`covariant_push_2026_10_22/V3_FULL_PICTURE.md` §1): J = Λ − 2a_geo²[u − ln(1 + u)] with a_geo² = a₀²/c⁴ =
  Λ/(32π) at κ = ½, Λ a coupling constant. v3s already uses one constant; the 32π is put in by hand.
- `opus_48_extended_research/reviews/bridge_scout/SCOUT_lambda_cc_desi_2026-06-19.md`: "unimodular ... make Lambda free;
  they cannot fix a0's value" (a literature scan, not a derivation).

**Why this is not ALREADY ON RECORD.** None of these ties a₀ to the Henneaux–Teitelboim MULTIPLIER Λ itself, the variable
made constant by B^μ's equation. k04's flux is the Legendre partner of that variable. CQ4 must say what the multiplier tie
adds beyond k04, and whether any of it is a gain on G5.

## The action (frozen)

Signature (−,+,+,+). Λ(x) is a scalar field, B^μ(x) a vector density; both are new, and nothing else is added.

**Form U (primary, the v3s instance).**

    S_U = (c³/16πG) ∫ d⁴x { √−g [ R − 2 J(Y; Λ) + 2 K(Q) ] + 2 Λ ∂_μ B^μ } − (γ_L/2) ∫ √−g (D_i P^i)² + S_m[g, matter]
    J(Y; Λ) = Λ − 2 α² Λ [ u − ln(1 + u) ],   u = √( Y / (α² Λ) ),

with α a dimensionless constant of the action (v3s's value is α² = 1/(32π)). Y, Q, K, P, γ_L are v3s's, unchanged.

**Form G (generic).** Any MOND sector whose only scale is the multiplier: L_X = Λ ℓ(X₁/Λ, X₂/Λ, ...) for invariants X_i of
dimension length⁻² (AQUAL-type: X = g^{μν}∂_μφ∂_νφ), plus the same 2Λ∂_μB^μ term.

A matter vacuum energy ρ_v enters as S_m ⊃ −∫√−g ρ_v c² (the generic constant, classical or from loops).

## Gates

- **S [scale relation]** Derive the field equations. The static weak-field limit must reproduce the parent law (v3s's
  simple-μ law for form U) with a₀ = α c² √Λ, and the script must give κ² ≡ a₀² / (c² G ρ_Λ,obs) in closed form, where
  ρ_Λ,obs is the gravitating vacuum density in the metric equation. Fails if the parent law is not reproduced.
- **G5a [form]** a₀ ∝ c √(G ρ_Λ) follows without a choice once the multiplier is the only scale. Reported; the record
  already lists the form as forced, so G5a alone is no gain.
- **G5b [number]** κ is fixed by the action with no free dimensionless normalisation. PASS only if no free constant (α or
  any other) remains in κ.
- **G5c [tie to the observed vacuum]** κ² is independent of ρ_v at fixed ρ_Λ,obs (∂κ²/∂ρ_v = 0 exactly).
- **C1 [renormalisation]** The tie survives a shift of the matter vacuum energy δρ_v and the renormalisation-scale
  dependence of ρ_v. Quantify the window of ρ_v/ρ_Λ,obs that keeps κ within the record's ±0.099 dex (KC1, current primary
  measurement) and compare it with the one-loop electron vacuum energy in MS-bar as an order-of-magnitude illustration
  [PROVISIONAL formula]. PASS only if the shift is absorbed with no change in κ.
- **C2 [time dependence, reported, not graded]** What the action does to ρ_Λ's time dependence (w of the tied component)
  and what it predicts for a₀(z)/a₀(0). State it against CFG689's native-ruler reading
  (`campaign_fresh_gravity/CFG689_native_ruler_bao/`); no data are graded here.
- **H1 [no ghost, kinetic signs]** The (Λ, B^μ) sector has no kinetic terms (zero velocity Hessian) and no local
  propagating mode; the tie adds no kinetic term to the parent. The parent's own health is inherited and named, not re-run.
- **H2 [no new fifth force]** No new long-range field beyond the MOND sector: δΛ must vanish locally on shell.
- **H3 [c_T = c]** The tie adds no term that changes the tensor sector; c_T is the parent's (v3s: c_T = c, V3W W4).

## Checks

- **K0 [known answer]** Without the MOND sector, the (Λ, B) equations are ∂_μΛ = 0 and ∂_μB^μ = √−g, and the metric
  equation is GR with a cosmological constant.
- **K1 [known answer]** v3s's J gives 1 + J′ = u/(1 + u) and κ = ½ at α² = 1/(32π) with ρ_v = 0.
- **MUTATE** Tie a₀ to k04's four-form flux q instead of the multiplier. The script must find feedback (q, and so a₀,
  depending on the local MOND invariant) in the MUTATE and exactly none for the multiplier tie. If the MUTATE shows no
  feedback, the check is broken and the lane does not grade.
- Symbolic identities must simplify to exactly 0 in sympy; numeric checks to relative 1e-12. Rerun the script and require a
  byte-identical output.

## Labels

- **TIE DERIVED (healthy)**: S, G5a, G5b, G5c and C1 pass, and H1–H3 pass.
- **TIE BY HAND (no gain over AX1)**: S and H1–H3 pass, but G5b, G5c or C1 fails.
- **UNHEALTHY**: any of H1–H3 fails. This overrides the TIE labels.
- **NO GO**: S fails (the parent law is not reproduced), or the system is inconsistent (Λ not constant on shell, or
  separate matter conservation broken).

Anything the multiplier tie does better than k04 (for example no environmental feedback) is reported as a remark. It is
not a gain on G5.
