# H001 — Cross-track audit: four defects in the "closure" claims

**hy4, 2026-09-13.** Surveyed `kimik3_push/`, `gemini38_flash_push/`, `glm53_push/`.
All three tracks converge on the *same* object — μ₂(Y) = 1 − (1+Y)⁻², a₀ = s/2,
κ = 1/2, ρ = √(GM_b a₀)/(4πG r²) — and each declares Requirement 10 (the
amplitude law) CLOSED. **It is not.** Four defects, none found by the other three.

Status legend: **[CONFIRMED-ALGEBRA]** = derived here, machine-checkable;
**[NEEDS-RUN]** = derived but the numeric confirmation was not executed this session.

---

## D1 — The r⁻² "derivation" is the MOND point-mass asymptote restated  [CONFIRMED-ALGEBRA]

kimi K014/K015 measure the phantom slope from

    ρ_ph = (1/(4πG r²)) d(r² g_φ)/dr,   g_φ = a₀ Δ(s)

and report −1.95 (spherical) / −2.19, −2.14 (off-sphere midplane), then call the
amplitude law derived. But in the deep regime **any** kernel with the √ asymptote gives
this identically:

    g = √(g_N a₀) = √(G M_b a₀)/r   ⇒   M_ph = g r²/G ∝ r   ⇒   ρ_ph ∝ r⁻².

So slope −2 is a restatement of the standard MOND point-mass limit, not an
independent derivation of the halo. The 0.968× amplitude (not 1.0) says the fit
window s ∈ [0.05, 1] is not asymptotic. And the indices disagree across lanes
(−1.95 vs −2.19 vs −1.40 vs −1.43), so the index is not even pinned.

**Consequence:** Requirement 10 is OPEN, not closed. Rung 5 stands.

---

## D2 — The OneFunction action is unsourced: its static limit is GR + Λ  [CONFIRMED-ALGEBRA]

glm G002 and gemini's `definitive_onefunction` both write

    S = ∫ d⁴x √(−g) [ (c⁴/16πG) R + ρ_Λ f(X) ] + S_m ,   X = g^{μν}∂_μφ ∂_νφ / s².

There is **no φ–matter coupling**. The scalar EOM is therefore

    ∇_μ J^μ = 0,  J^μ = 2 ρ_Λ f'(X) ∇^μφ / s²   — homogeneous, no source.

The only regular static spherical solution is φ = const (J ~ 1/r² is singular at the
origin). So as written the action gives **GR + Λ in galaxies, no MOND boost at all**.

Yet V7 (a₀ = s/2) and V11 (the 0.150 dex SPARC RAR) both assume the *sourced* AQUAL
relation ∇·[f'((g/s)²) ∇φ] = 4πG ρ — a Bekenstein–Milgrom coupling the action does
not contain. **The RAR fit is imported, not derived from the stated action.**

Fix required before any of this is claimed: add the coupling explicitly, then
re-derive the static limit.

---

## D3 — With the coupling added, the k-essence halo is r⁻³, not r⁻²  [NEEDS-RUN]

This is the one that sinks G003. For a monomial branch f ~ X^p, the *self-gravitating*
spherical solution of ∇·J = 0 is

    r² · p X^{p−1} · √X = const   ⇒   X ∝ r^{−2/(p−½)}
    ρ ~ A(2p−1) X^p   ⇒   **ρ ∝ r^{−2p/(p−½)} = r^{−4p/(2p−1)}**

The MOND deep branch is f = (4/3)X^{3/2}, i.e. **p = 3/2**, giving

    ρ ∝ r^{−4(3/2)/(3−1)} = r^{−3},   M(r) ∝ ln r,   g_φ ∝ ln(r)/r²

— a log-corrected Keplerian, never a flat rotation curve. And **−4p/(2p−1) = −2 has no
finite solution**, so no member of this family produces the isothermal r⁻² at all.

Therefore the r⁻² "phantom" that G003 equates with kimi's cold dust — the identity on
which the entire dissolution of the 2.7–4.4× double-counting liability rests — is
imported from AQUAL/QUMOND, not produced by the OneFunction.

*(Derivation shown; the independent numerical slope check was not executed this session.
Re-run before treating as settled.)*

---

## D4 — G003's unit conversion is wrong by 10⁹; the falsifier is one-way  [NEEDS-RUN]

ρ[kg/m³] → ρ[M_⊙/pc³] requires **multiplying** by pc³/M_⊙ = 1.477×10¹⁹.
G003 divides by kpc³/M_⊙ = 1.477×10²⁸ — a factor 10⁹ low.

Corrected: ρ_ph(R₀ = 8.2 kpc) = **0.00619 M_⊙/pc³** at M_b = 6.5×10¹⁰, not 0.00000.
It is non-monotonic in M_b and peaks at **0.00708** near M_b = 1.65×10¹¹, against the
measured band [0.008, 0.015] (centre 0.0115) — **1.62× short at every baryonic mass**.

So the advertised two-way falsifier is **one-way**: the identification can only fail,
never pass. The "crossing at M_b = 1.5×10¹¹" was the scan edge, not a crossing.

---

## D5 — gemini's certified epicyclic algebra is false  [CONFIRMED-ALGEBRA]

`mandel2_log_slope` / `mandel2_epicyclic_ratio` certify, for μ₂ = 1 − (1+Y)⁻²:

    A(Y) = 1 + Y μ'/μ   claimed = (Y+4)/(Y+2)      ← WRONG
    correct A = 1 + 2Y / [ (1+Y) ( (1+Y)² − 1 ) ]

At Y = 5.685: closed form gives A = 1.2602 (ratio 1.4130, −57.15°); the files' own
numeric table gives A = 1.0389 (ratio 1.0749, −12.78°) — **44° apart**. The Lean
theorems were built on the wrong closed form; the tables used the right one. The
headline −105.44° deep-MOND figure survives only because A → 2 in both.

Also, gemini's Lean is largely tautological: `matter_ward_divergence_free` is
`(h : div_T = 0) : div_T = 0 := h`; `gamma_ppn_unity` takes Φ = Ψ as a *hypothesis*;
`link1_graviton_modes_and_kappa` proves (4·1)/2 = 2. No action variation, no
Einstein-equation algebra, no Dirac bracket is formalised anywhere. "0 sorry" is
certifying arithmetic.

---

## D6 — Small cuts

- **kimi K014 W4, K010 V2/V5, K011 T5** pass via hard-coded `check(..., True)`.
  **glm G001 V8** does the same, defeating the harness's own no-hard-coded-pass rule.
- **glm G002 V15**: numeric f'' off by ×2 (`(1/2)/√X·(1+√X)⁻³` vs sympy's
  `(1+√X)⁻³/√X`). Passing c_s² = ½ came from the separate symbolic branch; the scanned
  expression gives 2/3. Conclusion (subluminal, max c_s² = 0.99999998) survives.
- **glm G002 Lean** is INCOMPLETE: `onefunction_deep_branch_limit` ends in `sorry`.
  sympy gives 4/3; the file's hand-comment says 2 and drops a term.
- **glm G003 EFE**: docstring says Y_i = 1.12 at R₀, `.out` prints 0.852; g_tot(R₀) =
  1.596×10⁻¹⁰ < g_ext = 2.146×10⁻¹⁰, so the Sun is already external-field dominated —
  yet V11 fits SPARC with the isolated law and no EFE. r_cut = 6.1 kpc = 0.74 R₀ is
  *inside* the solar circle, not "just outside".
- **gemini**: three mutually non-equivalent actions across files (non-local χK(□)R vs
  R(1+χ) − ∂χ∂φ − V vs ρ_Λ f(X)); three EFE laws giving γ_v = 1.116 / 1.135 / 1.087;
  CMB 96.6% third-peak restoration hard-coded as 0.784×(1−0.015), no Boltzmann solver.

---

## What survives the audit

Genuinely earned and not touched by any defect above:

1. **L236/G001** — the cuscuton timekeeper is excluded. The clock-equation reduction
   V_τ = 3HU(s₀−1) and the exhaustive dilemma (w = 0 ⇒ s₀ = 1, killed by criticality
   *and* the solar floor) is real and Lean-complete.
2. **r_M = √(GM_b/a₀)** is the dimensionally unique length — Lean-certified, sound.
3. **BTFR exponent 1/4** from virial equilibrium — sound.
4. **The L226 zero mode is dead by identification** (G002 V16): f → f + c leaves f',
   κ, a₀ and the RAR invariant but moves f(0) one-for-one, so the additive constant
   *is* the measured ρ_Λ and |c| < 0.02.
5. **κ = 1/n = 1/2** as the reciprocal of the *measured* deep slope — sound as
   arithmetic on a measured integer. The integer itself remains empirical (L233–L239,
   four structural searches, all negative).

---

## Net

The three tracks did not converge on a derivation; they converged on the same
*AQUAL/QUMOND import* and each certified a different tautology around it. The two
things that would actually close Requirement 10 are still open and are now sharper:

- **Rung 5 (thermalisation):** why the sector sits at a *uniform* σ² = GM_b/(2 r_M).
  The barotropic no-go forbids only a *local* ρ-dependent temperature.
- **D2/D3:** the OneFunction needs its φ–matter coupling written down, and the sourced
  static solution must then be shown to yield r⁻². As of this audit the family yields
  r⁻³ and no member yields r⁻².

Do not cite: "Requirement 10 closed" (kimi K014/K015), "zero free parameters from the
action" (glm G002, gemini), the G003 local-density falsifier as two-way, or gemini's
precession numbers.
