# D9_uv_parent FROZEN CRITERIA (written before any script or number of this lane)

Door 5 of the register: UV completion of the cold sector; no established covariant parent. κ = ½ is FITTED (the thermal
κ = Z/4π = 0.460659 is a postulate, Z = 5.78881). Footings a₀ = 9.36e-11 (canonical) and 1.13e-10 m/s² (alt) are reported
separately, never pooled. Cold energy is the extra mass; no particle species. Not "theory closed". Nothing here says the data
favour the framework over ΛCDM. Anything true by construction is flagged and carries no verdict weight.

## 0. Question (option (a) of the brief, with (c) as a side table)

AG6C NG2: a Lorentz-invariant U(1) realisation of the tether (C1, L(X) dual of W_full, Gauss law ∇·D = ρ_c − ρ̄ enforced) is
superluminal, v² = 1 + g/a₀. AG6C lists "L(X) without Y-dependence (L(X, Y) extensions not explored)" as a choice. DSF-21's action
(A33; frozen in `core_open_problems_round2_2026_10_20/03_relativity/report.md` §2) has a preferred foliation (P2) and a non-gauge
spatial covector P. Questions:
- (Q1) Does NG2 survive for every Lorentz-invariant L(X, Y), including parity-odd?
- (Q2) Does a preferred foliation (medium/cosmic frame) let a U(1) dielectric with the law be causal, and at what forced cost?
- (Q3) Why does DSF-21's action escape, and what does it pay instead?
- (Q4, side) Do the parent candidates have the same propagating field content as DSF-21 (gauge-equivalence test by count)?

## 1. Scope (declared)

Decoupling / principal-symbol limit: fixed flat metric, medium rest frame, uniform static background Ē = E ê (E = g > 0), B̄ = 0,
high-k plane waves; the medium's charge-current response and any mass terms are lower order and dropped. Rotational invariance in
the medium frame is assumed (so D ∥ E on the background). For Q3 the A33-family principal Lagrangian of round-2 §4 is a cited
input (it includes the shift coupling); this lane reproduces its reduction algebra from that Lagrangian, not from the full action.

## 2. Checks (script `d9_uv_parent.py`, sympy + numpy, deterministic)

Notation: quadratic Lagrangian ½δE·M·δE + δE·C·δB − ½δB·N·δB, Faraday δB = k×δE/ω, Ampère-type k×(NδB − Cᵀ δE) = −ω(MδE + CδB).
ε_∥ = dD/dE, ε_⊥ = D/E (forced by isotropy). "Extraordinary mode" X: k ⊥ ê, δE ∥ ê.

| id | test | PASS line |
|---|---|---|
| U1 | control: D(E) = a₀E/(a₀+E) with g = E, u = D gives g − u = g²/(g+a₀) | residual exactly 0 (sympy) |
| U2 | general Lorentz-invariant L(X, Y) (L_X, L_XX, L_Y, L_XY, L_YY all free symbols): solve the full dispersion for k ⊥ ê; mode X has v² = L_X/(L_X + 2X L_XX) = ε_⊥/ε_∥ | symbolic residual 0, independent of L_Y, L_XY, L_YY. If L_XY changes it, U2 FAILS and NG2's extension is scoped to parity-even L |
| U3 | with the law's D: v_X² = 1 + g/a₀ (NG2 reproduced) | residual exactly 0 |
| U4 | foliated class L(E², B², E·B) in the medium frame (M, C, N general isotropic-uniaxial about ê): v_X² = N_⊥/ε_∥. Define Λ_LV ≡ ε_⊥/N_⊥. (a) Λ_LV ≡ 1 for every L(X, Y); (b) v_X² ≤ 1 ⇔ Λ_LV ≥ 1 + g/a₀ | (a), (b) symbolic residual 0 |
| U5 | numeric cross-check of the dispersion code: random coefficients, the X-mode root of the full 3×3 determinant equals U4's formula | rel. diff ≤ 1e-10 at 20 draws |
| U6 | required Λ_LV at 1 AU (g = GM☉/AU²) and at g = a₀, both footings | arithmetic Λ_LV − 1 − g/a₀ ≤ 1e-12 (rel.); numbers reported |
| P1 | from round-2 §4's L_pr: longitudinal ω²/k² = (γ/η)Δ, Δ = 1 + ηPᵀS₀⁻¹P, and Δ = 1 − r₀ + (1+2β)r₀ sin²θ with r₀ = 2ηu²/(Kβ) | symbolic residual 0 (reproduction; low weight) |
| P2 | sup over θ and u ∈ [0, a₀) of the non-tensor v² in the A33 family = (γ/η)(1 + 4ηa₀²/K) (finite) | symbolic |
| P3 | the excess at η = γ = KL★²/2 is 2(L★a₀/c²)²; for L★ ∈ {24 pc, 1 kpc}, both footings | excess < 1e-12 at all four |
| P4 | structural contrast in the common capped variable u: U(1) cone factor a₀/(a₀ − u) → ∞ as u → a₀; A33 factor 1 + 4ηu²/K stays finite | both limits symbolic |
| G1 | A33's W(K\|P\|) is not invariant under P → P + ∇×C (first-order variation ≠ 0 for generic P, C), so A33's P_T is physical, unlike CFG938 (P_T = relabelling, S2a) and C1 (transverse D of a gauge U(1)) | variation not identically 0 |
| G2 | propagating non-metric field DOF on a static flat background, from the record: A33 = 5 − 2 = 3 (A68 C6), C1 = 2 (massless U(1)), CFG938/CFG938′ = 0 (χ, λ elliptic, WT-02 (a); CFG938′ uses the intrinsic leaf Laplacian, no u-derivative, WT-08 §2 definition) | the three counts are pairwise distinct (record-derived; low weight) |

`D9_UV_PARENT COMPLETE: N/M checks PASS.`; exit 0 iff all pass. MUTATE (`D9_MUTATE=1`): replace the law's D(E) by the linear
D = E (Maxwell). Then U1 and U3 must FAIL (v_X² = 1, not 1 + g/a₀). Outputs `d9_uv_parent_MUTATE.out`,
`d9_uv_parent_results_MUTATE.json`.

Constants (sources): G = 6.674e-11, c = 2.998e8, GM☉ = 1.32712e20 m³/s², AU = 1.495979e11 m, pc = 3.0857e16 m (standard);
a₀ footings (brief); L★ window 24 pc (A20) to 1 kpc (CFG820 upper end). No fitting, no scan of a free constant toward a target.

## 3. What each outcome means

- U2 + U4 PASS: **SCOPED NO-GO** for the U(1)-dielectric class: with the law, causality needs a dark-sector Lorentz-violation
  factor Λ_LV ≥ 1 + g/a₀ (unbounded in strong fields), Lorentz-invariant or foliated. NG2 is the Λ_LV = 1 special case.
- P1–P4 PASS: DSF-21's foliated Proca P escapes because its principal variable is the capped u, so its cone excess is bounded
  (≤ 4ηa₀²/K). Its price is read from the record, not computed here: preferred foliation; the phantom D·P = ς(ρ_c − ρ̄) is a
  matching identity, not a field equation (A33 §1, §7.3), which is also why NG1 (positivity) does not bite (by construction).
- G1 + G2 PASS: A33, C1 and CFG938(′) are distinct theories, not one theory in different gauges (count-level statement only).
- Any FAIL is reported as is; a FAIL in U2 for parity-odd L narrows the scope, it does not get repaired post hoc.

Not done: the full A33 cone with gravity off static backgrounds; A33 + a Route-A multiplier enforcing D·P = ρ_c − ρ̄ (the open
combination); any observational consequence of a slow dark mode. Not "established parent" under any outcome.
