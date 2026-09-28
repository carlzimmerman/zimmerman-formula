# AS022 — What a scale identity can actually derive (meta-audit)

**Run:** `AS022_r01_20260927T200914` · **Worker:** `sa-1-dfebe105` (Hermes subagent,
model deepseek/deepseek-v4-flash-0731 via OpenRouter) · **Ran:** 2026-09-28T00:09–00:20 UTC
**Task:** `deepseek_push/astra_spawn_ideas/AS022_what_a_scale_identity_can_actually_derive.md`
(sha256 `0d481977be086a459ce20c38b43932d0b03c30152d4698d66d8c31679abc531a`)
**Branch cell:** CORE scale identities (branch-independent; no Q/RAR/MU2/EXP/MONO kernel is
used for any conclusion except the explicitly-labelled Q composition example in §3.4).
**Sources pinned at assembly hashes:** README.md `91a5fac4…6b6ed`, FRIED_CHICKEN_SPEC.md
`98d9149f…d8e3f`, DERIVATIONS.md `8da8176e…fb889`, STANDING.md `660462eb…bf63`,
SOURCE_MANIFEST.json — all verified unchanged before execution.

---

## 0. Outcome in one paragraph

The scale identity `a0 = kappa·c·√(G·rho_Lambda)` with `kappa = 1/2` **adopted**, together with
the companion vacuum relation `F2: Lambda = 8·pi·G·rho_Lambda/c²`, is a **relationship among
quantities**: two independent constraints on three variables `(a0, rho_Lambda, Lambda)`. The
constraint system has rank 2 and its solution set is a **one-parameter family**; the identity
therefore *derives relations* (rearrangements, equivalent-variable identities, compositions with
stated kinematics) but **cannot derive the magnitudes** of `kappa`, `rho_Lambda`, `G` or `a0` —
one external measured datum is always required. Every "derivation of kappa" or "prediction of
rho_Lambda" in the framework corpus that this audit examined reduces to (A) an exact rearrangement
or composed identity (legitimate, and certified here in Lean), or (B) an empirical
determination/data-selection dressed in identity language, or (C) an adopted input. The strongest
statement and its domain are in §6; the exact outstanding implication in §8.

---

## 1. Step 1 — precise claim, symbols, assumptions

**Symbol dictionary (SI).**
| symbol | meaning | units |
|---|---|---|
| `a0` | vacuum acceleration scale | m·s⁻² |
| `B = g_N` | (positive) Newtonian baryonic radial acceleration | m·s⁻² |
| `g` | (positive) total radial acceleration | m·s⁻² |
| `rho_L` | vacuum mass density | kg·m⁻³ |
| `Lambda` | cosmological constant (curvature) | m⁻² |
| `G` | measured Newton coupling `G_N = 6.67430e-11` | m³·kg⁻¹·s⁻² |
| `c` | speed of light `299792458` | m·s⁻¹ |
| `kappa` | normalization coefficient, **= 1/2 adopted** | 1 |
| `r_M` | MOND radius √(G·M_b/a0) | m |
| `v_flat` | deep-MOND flat speed | m·s⁻¹ |
| `lambda` | free parameter of the solution family (= rho_L) | kg·m⁻³ |

`G_N`, `G_bare`, `G_cosmo` remain **separate symbols**; only `G_N` appears here, and every
`Lambda`-statement carries the same-G proviso (`G_E = G_N`; the ratio `G_E/G_N` is carried
explicitly wherever a transfer would need it — §8).

**Framework inputs (adopted, not conclusions of this task):** `kappa = 1/2`; `G_N`, `c`;
the two labelled footings `a0_can = 9.3619e-11` and `a0_alt = 1.1279e-10 m/s²` as *separate
normalization conventions* (they may not share a fixed `rho_Lambda` and a fixed `kappa`
simultaneously); no observational fit is performed.

**Constraints under audit (task's "Mathematics and principal test").**

    F1:  4 a0² − G c² rho_L = 0          (= a0 = (c/2)√(G rho_L), squared; carries kappa = 1/2)
    F2:  Lambda − 8 pi G rho_L / c² = 0

**Precise claim audited (meta-category).** "The scale identity is dimensionally consistent and
gives the same prediction in equivalent variables without adding independent fitted inputs, and
it (partially) derives the framework's scale content." The audit resolves this into two
constitutent questions, answered separately below:
(Q1) which mathematical objects *are* derivable from F1∧F2 alone (relations, ranks, compositions);
(Q2) which objects are *not* (magnitudes, kappa).

**Assumptions / domain.** Positive real variables; smoothness of F1, F2 (algebraic, so
automatic); no dynamics, no cosmology, no field equations; the branch cell is the identity itself.

---

## 2. Step 2 — constraint rank and parameterization

Jacobian of (F1, F2) w.r.t. (a0, rho_L, Lambda):

    J = [ 8 a0          −G c²          0 ]
        [ 0              −8 pi G / c²   1 ]

`rank J = 2` (row 1 has `dF1/da0 = 8a0 ≠ 0`, row 2 has `dF2/dLambda = 1`), and 2 < 3 variables,
so the regular solution set is a **1-parameter family**:

    (rho_L, a0, Lambda) = (lambda, (c/2)√(G·lambda), 8 pi G·lambda/c²),   lambda > 0.

**Independent datum still required even when both equalities hold exactly:** exactly **one**
measured magnitude out of `{rho_L, a0, Lambda}` (any one determines the other two through the
family; the pair of constraints never does). Equivalently: the identity fixes the *ratios*
`a0²/rho_L = G c²/4` and `Lambda/rho_L = 8 pi G/c²` and the composed ratio
`Lambda = 32 pi a0²/c⁴` — nothing absolute.

**kappa enters only as the member-selector of the family.** With general kappa, F1 reads
`a0² − kappa² c² G rho_L = 0`, the family is
`(rho_L, a0, Lambda) = (lambda, kappa·c√(G·lambda), 8 pi G·lambda/c²)`, and kappa is a *second*
adopted parameter — the identity is silent about its value. (Corpus agreement: STANDING rev. 8–10:
"κ measured 0.465 ± 0.076 … consistent with ½, **not derived**; every derivation route closed";
k01 zero-mode theorem: the MOND primitive enters the field equations only through its derivative,
so the a0–Λ normalization is a zero mode of local MOND actions; k02 sequestering-type global
constraints miss by ~5 orders; k04 four-form promotion leaves kappa as the free ratio
`Z/beta² = 8`; k03 horizon form `a0 = c²/(2 pi L_dS)` gives kappa = 0.461, degenerate with the
H0 tension. The PAGE-27 scale erratum's "derivation" `kappa = a0/[c·sqrt(G rho)] = 1/n` is the
same identity read backwards: a definitional rearrangement whose left side is then *measured*,
not derived — §5.4.)

---

## 3. Step 3 — intermediate algebra, units, limits

### 3.1 Units

    [c √(G rho_L)] = (m/s)·√(m³ kg⁻¹ s⁻² · kg m⁻³) = (m/s)·s⁻¹ = m s⁻²          ✓ a0
    [8 pi G rho_L / c²] = m s⁻²·m⁻¹·(m² s⁻²)⁻¹·… = m⁻²                              ✓ Lambda
    [√(G M_b / a0)] = √(m³ kg⁻¹ s⁻² · kg · m⁻¹ s²) = m                              ✓ r_M
    [G M_b a0] = m³ kg⁻¹ s⁻² · kg · m s⁻² = m⁴ s⁻⁴ = [v_flat⁴]                     ✓ BTFR

### 3.2 Per-footing consequences (60-digit Decimal; both footings SEPARATE)

| quantity | canonical `a0=9.3619e-11` | alternative `a0=1.1279e-10` |
|---|---|---|
| `rho_L = 4 a0²/(G c²)` [kg/m³] | 5.8444124540218754e-27 | 8.4830896195590974e-27 |
| `eps_L = rho_L c²` [J/m³] | 5.2526959597261136e-10 | 7.6242207272672790e-10 |
| `Lambda = 8 pi G rho_L/c²` [m⁻²] | 1.0907997632807349e-52 | 1.5832818476965227e-52 |
| `Lambda = 32 pi a0²/c⁴` [m⁻²] | identical (residual 0E-111) | identical (0E-111) |
| `a0 ← c² √(Lambda/32pi)` [m/s²] | 9.3619000…e-11 (residual 4e-59) | 1.1279000…e-10 (residual 0) |
| `Lambda·(c²/a0)²` | 32·pi = 100.53096491487338… | same (exact to 60 digits) |

Float64 residuals: F1 residual 0.000e+00 both footings; cross-route F2 residual 1.855e-68
(canonical) and 0.000e+00 (alt). These are **exact identities**, not finite numerical
consistency fits — the residuals are zero at the working precision by construction of the
back-substitution, and the Lean certificate (§7) proves the algebraic content.

### 3.3 Composed identities (derived relations, with their stated assumptions)

**MOND radius** — definition `B(r_M) = a0` with `B = G M_b/r²` gives `r_M² = G M_b/a0`
(Lean-certified). Fiducial `M_b = 10^11 M_sun`: `r_M = 12.20 kpc` (canonical) /
`11.12 kpc` (alt); `M_b = 1 M_sun`: `r_M = 1.19e15 m = 0.0386 pc` (canonical) / `1.08e15 m`
(alt).

**Deep law** — composition of the deep limit of Q (`g² = a0·B`), circular kinematics
(`g = v²/r`) and the spherical source convention (`B = G M_b/r²`) yields exactly
`v_flat⁴ = G M_b a0` (Lean-certified `deep_v4_composition`). In vacuum variables,
`v_flat⁴ = (1/2) c G M_b √(G rho_L)` (Lean-certified `btfr_vacuum_form`) — the README's
"deep-MOND BTFR" form. **These are derivations of relations conditional on the named kinematics
and source convention; they are not derivations of a0 or of any magnitude.**

### 3.4 Limiting regimes with leading neglected term

For the composition `g = √(B² + a0 B)` (Q branch used only as the composition law here):

- deep `x = B/a0 → 0`: `g = √(a0 B)·√(1+x) = √(a0 B)(1 + x/2 − x²/8 + x³/16 − 5x⁴/128 + …)`,
  domain `0 < x < 1`, leading neglected term `+ (B/(2 a0)) √(a0 B)`. Numeric (x=0.1): exact
  0.3316624790…, 2nd-order expansion 0.3316438696…, rel err 5.61e-5. (x=0.5): rel err 4.89e-3.
- Newtonian `x → ∞`: `g = B√(1 + a0/B) = B(1 + a0/(2B) − a0²/(8B²) + a0³/(16B³) − …)`,
  domain `x > 1`, leading neglected term `+ (a0/(2B))·B = a0/2`. Numeric (x=10): exact
  10.4880884817…, expansion 10.48750, rel err 5.61e-5.
- Boundary case `B = a0`: `g = √2·a0` exactly; belongs to neither expansion regime (they hold
  for `x < 1` and `x > 1` respectively).
- The exact factor identity `√(B² + a0B) = √(a0B)·√(1 + B/a0)` is Lean-certified
  (`deep_limit_factor`).

---

## 4. Step 4 — independent check in a different representation

1. **Substitution back into F1, F2** at 60-digit precision for both footings: residuals
   `0E-79` (F1) and `0E-111` (F2) — the actual residuals, not Booleans (as022_numeric_run.out).
2. **Cross-route Lambda**: `Lambda` computed two independent ways (F2 direct vs closed form
   `32 pi a0²/c⁴`) agree to 111 digits on both footings.
3. **Reconstruction**: `a0` rebuilt from `Lambda` via `c²√(Lambda/32 pi)` reproduces the footing
   value to the last decimal (worst residual 4e-59).
4. **Lean re-derivation** of the algebraic content (7 theorems, zero `sorry`, axioms ⊆
   {propext, Classical.choice, Quot.sound}) — an independent representation of the same
   identities (§7).

---

## 5. Step 5 — negative control and the strongest surviving statement

### 5.1 Negative control (must be capable of failing)

**Claim under test:** "F1 ∧ F2 together fix the absolute values of (a0, rho_L, Lambda) — the
identity derives the scale." **Control:** exhibit two distinct members of the family and check
both satisfy F1 ∧ F2 exactly. Members λ = 5.844e-27 and λ′ = 4λ: (a0, Λ) = (9.36157e-11,
1.09072e-52) and (1.87231e-10, 4.36289e-52) — **both pass F1 and F2 to < 1e-30** while differing
by a factor 2 and 4 in the magnitudes. The control *fails the claim*, exactly as required: the
identity does not single out any member. (This is also the counterexample side of the deliverable:
the task explicitly does not pre-judge outcome; the identified "failure" is the claim of
magnitude-derivation, and the surviving content is the family structure.)

### 5.2 Control — rearranged copies do not create constraints

Five rearranged copies of F1 (`4a0²=Gc²rho`, `a0=(c/2)√(G rho)`, `rho=4a0²/(Gc²)`,
`16a0⁴=G²c⁴rho²`, `a0²=(c²G/4)rho`) plus two copies of F2 were written down and treated as
"new equations". Symbolic Jacobians (sympy, exact):

- generic (off-curve) rank of the 5 F1 copies w.r.t. (a0, rho): **2** — the copies are not
  identical as *functions*; the test that matters is the solution set;
- on the solution curve: rank of the 5-copy system = **1**; rank of the full
  {F1a…F1e, F2, F2b} system w.r.t. (a0, rho, Lambda) = **2**.
- Conclusion: 7 written equations still carry 2 constraint directions and a 1-parameter family —
  **rewriting F1 cannot be counted as new physics**. This control could have failed (if the
  copies had independent zero-sets, e.g. a sign-flipped copy `4a0² + Gc²rho = 0` — which this
  audit deliberately does NOT include, since it is not an equivalent rewrite — the rank would be
  2 and the family would be cut); it passes on the equivalent-rewrite set.

### 5.3 The taxonomy: which moves are legitimate derivations, which are re-labelling/adoption

| # | Move | Corpus example(s) | Verdict |
|---|---|---|---|
| A1 | **Rearrangement of the identity** (solve for one variable given the others) | README key-eq block: "equivalently `4a0² = G c² rho_Lambda`, `Lambda = 32 pi a0²/c⁴`"; L180 `(cH0/a0)² = 8π/(3κ²Ω_Λ)` | Legitimate *relation*; zero new content; Lean-certified here. "Deriving rho_Lambda from a0" is this move and requires a0 as input — it never produces the magnitude from nothing. |
| A2 | **Equivalent-variables identity** (same prediction in different variables) | README: `a0 = c²√(Lambda/32 pi) = 9.3619e-11` | Legitimate; exact; both footings applicable through the family (§3.2); Lean-certified (`a0_from_lambda`). |
| A3 | **Composition with stated kinematics/source conventions** | README deep-MOND BTFR `v_flat⁴ = G M_b a0 = (1/2) c G^{3/2} M_b √(rho_Lambda)` | Legitimate *derived relation*, conditional on the named kinematics (circular motion) and source convention (spherical B); Lean-certified (`deep_v4_composition`, `btfr_vacuum_form`). Not a derivation of the scale. |
| A4 | **Moment-closure identities on a branch** | DERIVATIONS.md §1: `a_mean = a − (Var(g)−Var(B))/⟨B⟩` (exact on Q) | Legitimate derived relation with explicitly stated averaging assumptions; the source itself lists "what these chains do not derive: … kappa …". Model for the boundary this audit draws. |
| B1 | **Coefficient bookkeeping dressed as derivation** | PAPER27 erratum: printed "`a0 = s/c, kappa = 1/c`" (overloaded `c`); corrected: `a0 = s/n, kappa = 1/n` | Rearrangement + a *definition* of n; the value of n (hence kappa) is adopted or measured, never derived by the identity. |
| B2 | **Empirical determination of kappa via data selection** | README rev. 19 / L232: accelerations in units of `s = c√(G rho_L)`; data select `n = 2`, i.e. κ = 1/2 on 155/175 SPARC curves | A measurement/determination (itself inference under the RAR branch), explicitly labelled by the corpus as "selected by data, not derived" — consistent with this audit’s verdict: the *identity* played no role in fixing κ beyond supplying the unit system. |
| C1 | **Adopted input stated as input** | STANDING: "κ = 1/2 fitted, not derived; every derivation route closed"; k01/k02/k03/k04; FRIED_CHICKEN req. 13: "DO NOT fake a derivation … say so explicitly" | The correct labelling; the closure spec itself requires what this audit enforces. |
| D1 | **Historical coefficient under other premises** | README credit block: Milgrom 1999 dS–Unruh derives `a0 = 2c H_Lambda` (κ = 1/2π-candidate coefficient 8% away) | A derived coefficient *inside a different set of premises*; under the framework’s F1 (κ = ½) it is a comparison branch, not a transferable derivation (FRAMEWORK_CONTRACT: historical branches remain labelled). |

The audit’s boundary is therefore: **F1∧F2 alone derive exactly the content of rows A1–A4
(relations, ranks, compositions, moment closures). They do not derive the content of rows
B1–C1 (absolute magnitudes, kappa).** No corpus claim examined contradicts this boundary; the
framework’s own standing record is the strongest confirmation (κ "measured, not derived").

---

## 6. Strongest surviving statement

**Theorem AS022 (meta, scoped).** Let `a0, rho_L, Lambda, G, c > 0` satisfy F1:
`4 a0² = G c² rho_L` and F2: `Lambda = 8 pi G rho_L/c²`. Then:

1. The solution set is the one-parameter family `(rho_L, a0, Lambda) = (λ, (c/2)√(Gλ), 8πGλ/c²)`,
   `λ > 0` — rank 2 on 3 variables, so **one external datum λ (equivalently one measured
   magnitude among rho_L, a0, Lambda) is required**; the pair never fixes an absolute scale
   (negative control §5.1).
2. Any finite set of *equivalent rearrangements* of the constraints has the same rank on the
   family (1 for F1-copies, 2 for the full copy system) — rewriting adds no constraint (§5.2).
3. On the family, exactly: `Lambda = 32 pi a0²/c⁴` and `a0 = c² √(Lambda/32 pi)` (Lean-certified).
4. Composition with the stated kinematics/source conventions yields exactly `v_flat⁴ = G M_b a0`
   and `r_M² = G M_b/a0` (Lean-certified) — derived *relations*, not magnitudes.
5. `kappa` enters only through the choice of family member (via F1); its value is **not** a
   consequence of the identity. With κ = 1/2 adopted: canonical footing λ_can = 5.84441245…e-27
   kg/m³ ⟷ a0 = 9.3619e-11 m/s²; alternative footing λ_alt = 8.48308962…e-27 kg/m³ ⟷
   a0 = 1.1279e-10 m/s² — **separate normalizations**, never combined.

**Domain:** positive real variables, SI units; no dynamics, no cosmology, no observational fit;
branch cell CORE scale identities. The dimensionless algebraic content (statements 1–4) applies
to both footings through the same family; all dimensional numbers are carried per footing.

**Criterion:** the "proposed vacuum acceleration scale is dimensionally consistent and gives the
same prediction in equivalent variables without adding independent fitted inputs" — **supported in
the sense that the relation content is exact and input-free; the magnitude of a0 is an adopted
normalization of the same relation.** This task adds no new assumption and no fitted input.

---

## 7. Lean certificate

`AS022_scale_identity_certificates.lean` — 8 theorems, compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>`:
`scale_identity_iff` (squaring equivalence with 0 ≤ a0), `lambda_from_two_constraints`
(Λ = 32πa0²/c⁴), `a0_from_lambda_sq`, `a0_from_lambda` (a0 = c²√(Λ/32π) with 0 ≤ a0),
`deep_v4_composition`, `btfr_vacuum_form`, `deep_limit_factor`, `rM_transition_sq`.
Result: **exit 0, zero `sorry`, every theorem’s axiom set ⊆ {propext, Classical.choice,
Quot.sound}** (printed by `#print axioms` in lean_check.out). House-traps observed and handled:
`Real.sqrt_mul` in Mathlib 4.34 has explicit-`y` signature `{x} (hx : 0 ≤ x) (y : ℝ)` (two failed
arity attempts recorded); no trailing tactic after a closing `field_simp`/`rw`; positivity
hypotheses bound before rewrites.

---

## 8. Next unresolved implication (first bridge to the operative target)

The operative target is filtered **MONO** under causality criterion B (FRIED_CHICKEN_SPEC
amendment block). Nothing in this audit touches dynamics, so no gate beyond 13’s
input-labelling is claimed. The first missing bridge to transfer the audit to that target is a
**substitution lemma**:

> Let the amplitude `a0` inside the operative filtered quasistatic sector
> `∇²Φ = 4πGρ_b + S*∇·[(ν_mono(|∇S u|/a0) − 1)∇S u]` be replaced by `(c/2)√(G rho_Lambda)`
> with `rho_Lambda` the SAME vacuum density appearing in F2. Prove (and Lean-certify) that the
> equations are identical in form — i.e. the replacement is a pure parameter re-labelling
> (`a0 → (c/2)√(G ρ_Lambda)`), with `Lambda = 32π a0²/c⁴ · (G_E/G_N)` bookkeeping if the
> Einstein-sector coupling `G_E` differs from `G_N` (FRAMEWORK_CONTRACT: `Lambda_eff =
> 8π G_E rho_Lambda/c² = 32π (G_E/G_N) a0²/c⁴`).

This is precisely the "branch-translation proved before transferring" step the contract
requires; it is stated as ready-for-dispatch child **AS022.C01** (spec written in this run dir,
`AS022.C01_child_spec.md`; NOT dispatched — no spawn mechanism in this session; orchestrator
action required).

## 9. Limitations

- Proves relation content of the scale identity only: no dynamics, no cosmology, no
  observational fit, no grid, no Q/RAR/MU2/EXP/MONO conclusion (the Q composition appears only
  as the named composition law in §3.3–3.4).
- kappa = 1/2 remains adopted; the identity’s inability to derive it is demonstrated by rank and
  by the negative control, and corroborated by the corpus’s own zero-mode record — this run adds
  no new derivation route.
- Both footings carried separately; no hybrid "fixed density AND fixed kappa" number is quoted.
- Numerical consistency checks (expansions §3.4) are finite checks of algebraic identities, not
  theorems; the identities themselves are Lean-certified.
- The substitution lemma (§8) is open; MONO/filtered and criterion-B statements are untouched by
  this run.

## 10. Files in this run dir

`audit_AS022_scale_identity.py`, `as022_numeric_run.out`, `as022_run_console.log`,
`as022_audit_summary.json`, `AS022_scale_identity_certificates.lean`, `lean_check.out`,
`AS022.C01_child_spec.md`, `derivation.md`, `result.json` (hashes in result.json).
