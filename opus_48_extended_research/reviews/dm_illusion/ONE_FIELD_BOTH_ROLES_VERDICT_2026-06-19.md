# Does ONE dS-Unruh field give BOTH a0 AND the cold a^-3 clustering? — three senses, three answers (2026-06-19)

*Topic `one_field_both_roles`. Tests whether the framework's dS-Unruh scalar/aether sources BOTH the deep-MOND
galaxy term (a0, the AeST J(Y) spatial sector) AND the cold clustering condensate (the K(Q) a^-3 dust = the
"dark matter") as two modes of ONE field, or whether they are unavoidably independent. Calc in
`one_field_both_roles.py` + adversarial `adversarial_break_orthogonality.py` (both run clean). Primary source
Skordis-Zlosnik 2021 (arXiv:2007.00082) re-verified VERBATIM via ar5iv this session. Quarantine held; both-ways.*

## ONE-LINE VERDICT

**YES in the FIELD-CONTENT sense, NO in the SHARED-ORIGIN sense.** It is literally ONE gravitational-sector
scalar φ — split by the dS-named aether A_μ into a SPATIAL gradient Y (carrying a0) and a TEMPORAL gradient Q
(carrying the cold dust) — so the cluster+CMB "dark matter" is a genuine MODE of the framework's own field, NOT
a new particle or a separate field. But the two modes are **provably orthogonal**: a0 is a Lagrangian coupling
in the (FRW-invisible) Y-sector, the dust amount is a FREE integration constant I0 in the Q-sector;
`d(ρ_dust)/d a0 = d(ρ_dust)/dΛ = 0` structurally, and a0 is absent from linear growth. **Fixing a0 from Λ does
NOT fix how much "dark matter" there is.** So they are two STRUCTURES of one field, not one structure doing two
jobs. This is the strong-illusion claim's real, defensible content (no particle) — and its honest limit (the
amount is independent, the CMB still needs that energy).

## THE THREE SENSES (the question is genuinely ambiguous; resolved each, both-ways)

### S1 — FIELD-CONTENT: same scalar in both terms? **YES (exact).**
The AeST action carries ONE scalar φ and ONE aether A_μ. The two invariants are the complete orthogonal split
of |∇φ|² by the aether (sympy-verified identity `Y − Q² = (∇φ)²` in the rest frame):
- **Q = A^μ∇_μφ** — TEMPORAL projection (along the aether) → the cold a^-3 dust.
- **Y = q^{μν}∇_μφ∇_νφ, q = g + AA** — SPATIAL projection (orthogonal to the aether) → the a0 / Y^{3/2} MOND term.

Verbatim (ar5iv, this session): *"𝒬=A^μ∇_μϕ and 𝒴=q^{μν}∇_μϕ∇_νϕ where q^{μν}=g^{μν}+A^μA^ν is the three-metric
orthogonal to A^μ."* So at the level of degrees of freedom this is genuinely **"two modes of one field."** No
separate dark-matter field is added; the dS-Unruh aether (which the framework FOUNDS as the cosmic rest frame)
is exactly what does the splitting. **This is the strongest true form of "dark matter is the framework's own
field, not a particle."**

### S2 — SHARED ORIGIN/COUPLING: does ONE number set BOTH a0 and the dust amount? **NO (robust).**
On FRW, A aligns with cosmic time ⇒ `q^00 = g^00 + A^0A^0 = −1+1 = 0` ⇒ **Y ≡ 0 identically** ⇒ the entire a0
(Y^{3/2}) sector is invisible to the homogeneous background. The dust comes from the Q-sector alone:
shift-symmetry ⇒ first integral `dK/dQ = I0/a³` ⇒ `ρ̄ = ρ̄₀/a³` with `8πG̃ρ̄₀ = Q₀·I0`. Then:
- `d(ρ_dust)/d a0 = 0` and `d(ρ_dust)/dΛ = 0` **structurally** (a0 lives in Y; Λ enters K only as the additive
  −2Λ, invisible to dK/dQ). The dust amount depends ONLY on Q₀·I0, and **I0 is an INTEGRATION CONSTANT** (an
  initial datum), not an action coupling. Verbatim: *"As the solution depends on the initial condition I0, the
  density ρ̄ is not (classically) predicted"*; *"The CC ... remains a freely specifiable parameter, just as in
  the ΛCDM model."*
- **a0 is absent from linear growth (Bridge-1):** `d/dY[Y^{3/2}] = (3/2)√Y → 0` as Y→0, so the a0-sector cannot
  even in principle source the linear clustering that builds the 3rd peak. Verbatim: *"a0 does not appear in the
  linear cosmological regime but will play a role once nonlinear terms ... kick in."*
- **No dS identity hits the amount:** the why-now ratio Ω_dust/Ω_DE = 0.387 is missed by every dimensionless
  dS/holographic combo of {Λ, a0, Z, Ω_DE} by ≥19% without a hand-tuned O(1).

So "one number for both" is FALSE. It is one FIELD, two INDEPENDENT data: one coupling (a0, tied to Λ in the
dark-ENERGY face) and one initial constant (I0 ≈ Ω_dm, free). The Ω_dust ≈ Ω_dm closeness is **abundance, not
unification.**

### S3 — DERIVATION: does dS-Unruh DERIVE both modes of F(Y,Q)? **PARTIAL (form) / NO (amount + kernel).**
- Y-sector: dS-Unruh FORCES the n=3/2 √-law FORM (`g_obs=√(g_bar²+g_bar·a0)`, Deser-Levin T_eff) and the a0
  VALUE plugs into AeST's one a0 slot (Z=cH_Λ/a0=√(32π/3) machine-exact). Form motivated; but even the Y-sector
  KERNEL θ(y) is NOT fixed (MI_KERNEL verdict: wrong functional class, analytic memory, no √(ȧ)).
- Q-sector: dS-Unruh NAMES the aether (the thing that defines Q) but does NOT derive K(Q) = −2Λ + K2(Q−Q0)² + …
  — the curvature K2 (mass), the minimum Q0, and the amplitude I0 are FREE. And the aether is founded as a
  non-dynamical FRAME, not the dynamical FIELD (no K_B kinetic term derived).

## ADVERSARIAL (took the strong illusion claim seriously; four believer moves to TIE a0 to the dust — ALL FAIL)
| believer move to share ONE origin | result |
|---|---|
| (A) a Y·Q cross term in F(Y,Q) couples the sectors | FAILS — Y≡0 on FRW; δ(Y·Q) is 2nd-order in perts → only NONLINEAR (Skordis's own caveat), never the linear dust |
| (B) the same K2 (ghost-condensate mass) sets both | FAILS — K2 sets the dust SCALE (mu), never the AMOUNT (I0); K2 free + data-squeezed opposite ways |
| (C) dS-Unruh derives K(Q) so Λ fixes I0 | FAILS — dS-Unruh acts on the worldline RESPONSE (couplings); I0 is a cosmological integration constant — category-separate |
| (D) Verlinde "apparent DM = dS elastic back-reaction" (one mechanism) | FAILS — stays a DEAD MIRAGE: under-predicts cluster missing mass ~5–6× (toy: M_D/M_b≈1.06 vs needed ~6), wrong RC residual + footing (1/6≠1/Z). Guardrail honored. |

**Orthogonality is ROBUST under adversarial push.** It is not a numerology miss; it is a structural category
separation (action coupling vs initial datum) — the same fact as Bridge-1.

## HONEST LINE (held)
- The CMB 3rd peak still DEMANDS the Q-sector energy (CAMB-verified, omch2~0.12; P3/P2 0.527→0.980). "Literally
  nothing there" stays FORBIDDEN. Field ≠ particle is the honest meaning, and the AMOUNT stays free.
- "Dark matter is a MODE of the framework's own field (not a particle)" — DEFENSIBLE (S1). "a0 and the dark
  amount share a derived origin / one number" — NOT supported (S2). "dS-Unruh derives the dark sector" — NOT
  supported (S3, partial form only). No manufactured unification; no reflexive ΛCDM dismissal.

## NET
ONE FIELD, BOTH ROLES is **TRUE as field content** (the dark sector is a mode of the framework's own
gravitational scalar, split by the dS-named aether — the strong illusion claim's real content) and **FALSE as
shared origin** (a0 and the dust amount are provably orthogonal; the amount is free). The two roles share a
FIELD but not a STRUCTURE or a NUMBER. The dark sector is **relocated** (particle → a mode of the framework's
own field) **and its amount stays independent** — not eliminated, not derived, not pinned.

## SOURCES
- Skordis & Zlosnik 2021, PRL 127 161302 = arXiv:2007.00082 (ar5iv full text, 5 load-bearing phrases re-verified
  VERBATIM this session: Q/Y defs, "a0 does not appear in the linear cosmological regime", "ρ̄ not (classically)
  predicted", CC "freely specifiable ... just as in ΛCDM", "it is in this limit that a0 appears").
- Verwayen, Skordis & Zlosnik 2024, MNRAS 531 272 = arXiv:2304.05134 (mu "treated as a free parameter").
- Banked: AEST_EMBEDDING_2026-06-19, SQRT_LAMBDA_PINS_KQ_VERDICT_2026-06-19, DARK_SECTOR_CMB_CLUSTERS_2026-06-19,
  MI_KERNEL_FROM_DSUNRUH_2026-06-19, SKORDIS_GEOMETRIC_FRAMEWORK_REVIEW_2026-06, ROUTE_B_LAMBDA_EFFECTIVE_VERDICT
  (Verlinde/SdS back-reaction = banked mirage), TOE_LITERATURE_MAP_2026-06-15.
- Calc: `dm_illusion/one_field_both_roles.py`, `dm_illusion/adversarial_break_orthogonality.py` (both run clean).
