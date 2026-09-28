# AS003 — Critical-density closure as a dependency problem

**Run:** `AS003-20260927-r01` · **Task:** `AS003_critical_density_closure_as_a_dependency_problem.md`
(sha256 `5d61a28775f25284f86e001e487096402c97c21f2953c1767d27851ab34393dd`,
matches manifest.json) · **Group/priority:** A01 / P0 · **Branch:** CORE scale
identities (no Q/RAR/MU2/EXP/MONO import; no branch translation used — every object
below lives wholly inside the CORE scale identities declared in FRAMEWORK_CONTRACT.md).
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes subagent sa-2-04703921.

**Operative target context.** The amended thirteen-item target (FRIED_CHICKEN_SPEC.md,
user decision 2026-09-26) carries filtered ν_mono as kernel and criterion B as causality;
requirement 13 (cosmological acceleration-scale relation) reads: *preserve or derive if
mathematically possible: a₀ = (c/2)√(Gρ_Λ) … DO NOT fake a derivation.* This task does
not touch the kernel branches; it operates on requirement 13's identity content.

---

## 1. Precise claim, symbol dictionary, assumptions

### 1.1 Claim under test (task, "Mathematics and principal test")

Let the vacuum density be the framework input ρ_Lambda = 4 a0²/(G_N c²) (the κ = 1/2
restatement of a0 = κ c √(G_N ρ_Lambda)) and the critical density be the standard
Friedmann-closure definition ρ_crit = 3 H0²/(8π G_cosmo). Then, with Ω_L := ρ_Lambda/ρ_crit:

1. Under a common coupling (G_N = G_cosmo): **Ω_L = 32π a0²/(3 H0² c²)**.
2. If ρ_crit carries G_cosmo while the scale carries G_N: **Ω_L = (32π/3)(G_cosmo/G_N)(a0/(H0 c))²**,
   i.e. the expression acquires the factor G_cosmo/G_N.

The *dependency problem* under test: does the "critical-density closure"
(ρ_scale = ρ_crit, so that a0 is fixed by {H0, G}) make a0, H0 or Ω_L a **prediction**,
or is the third quantity merely a **re-expression** of the other two?

### 1.2 Symbol dictionary (units and convention, all per FRAMEWORK_CONTRACT)

| symbol | meaning | units | status |
|---|---|---|---|
| a0 | vacuum acceleration scale | m s⁻² | input (two registered footings: canonical 9.3619e-11, alternative 1.1279e-10) |
| κ | normalization in a0 = κ c √(G_N ρ_Lambda) | — | **adopted κ = 1/2**; not derived here, not derivable by the k01/k03 no-go class (README) |
| ρ_Lambda | mass density in the scale formula | kg m⁻³ | framework identity ρ_Lambda = 4 a0²/(G_N c²) is the κ = 1/2 restatement (input) |
| ρ_crit | critical density | kg m⁻³ | definition ρ_crit = 3 H0²/(8π G_cosmo) (Friedmann closure) |
| Ω_L | ρ_Lambda / ρ_crit | — | derived object of this task |
| G_N | coupling in the scale a0, in deep law v_flat⁴ = G_N M_b a0, in r_M = √(G_N M_b/a0) | m³ kg⁻¹ s⁻² | default 6.67430e-11; separate symbol |
| G_cosmo | coupling in the Friedmann equations / ρ_crit | m³ kg⁻¹ s⁻² | **separate symbol**; equals G_N only when the ratio G_cosmo/G_N is stated to be 1 |
| G_bare | action-level coupling | m³ kg⁻¹ s⁻² | recorded but unused (this task needs no action) |
| G_E | coupling in the Einstein vacuum-curvature term (Λ_eff = 32π(G_E/G_N) a0²/c⁴) | m³ kg⁻¹ s⁻² | enters ρ_Lambda only transitively; cancels (eq. 2.6) |
| H0 | Hubble constant today | s⁻¹ | H = h·100 km s⁻¹ Mpc⁻¹; pc = 3.085677581491367e16 m; anchors 67.4 and 73.0 km s⁻¹ Mpc⁻¹ (README k03) |
| c | speed of light | m s⁻¹ | 299792458 |
| Λ, Λ_eff | vacuum curvature scales | m⁻² | Λ = 32π a0²/c⁴ (G_E = G_N); Λ_eff = 32π(G_E/G_N) a0²/c⁴ generally |

**H convention.** All instances of H0 in this document mean the value in s⁻¹ obtained
from H0[km s⁻¹ Mpc⁻¹] × 1000/(pc × 1e6). A 1% error in pc propagates as 1% in H0 and
2% in H0²; a 1 km s⁻¹ Mpc⁻¹ error in the anchor is a 0.9% error in Ω_L (∂lnΩ_L/∂lnH0 = −2).

### 1.3 Assumptions and boundary conditions

- **A1 (domain).** a0 > 0, H0 > 0, G_N > 0, G_cosmo > 0, c > 0 (D = ℝ₊⁵). "Dimensionless
  witnesses use positive variables" (task inputs).
- **A2 (flat closure).** A k = 0 Friedmann background so the total density satisfies
  ρ_total = ρ_crit. Needed only for the alternative-footing *reading* (§2.5). Non-flatness
  enters through the leading neglected term −k c²/a² (eq. 2.2); |Ω_K| ≤ 0.001
  (Planck 2018, comparison value) makes that a ≤ 0.2 % correction to any ρ-total
  identification — well below every number quoted here; no fit is performed.
- **A3 (framework identity).** ρ_Lambda = 4 a0²/(G_N c²) is the adopted κ = 1/2 restatement
  of the declarative a0 relation. It is an INPUT; this task derives its consequences only.
- **A4 (couplings).** G_N, G_cosmo, G_E, G_bare are distinct symbols until a relation is
  derived (contract). The ratio r := G_cosmo/G_N is carried everywhere; where the ratio is
  quoted as 1 it is an explicitly stated convention, not a derived equality.
- **A5 (no limiting regime).** The principal object is an exact algebraic identity; no
  expansion is used. Where a limiting or boundary statement is needed the task wording
  ("otherwise check normalization and a boundary case") is followed (§5).

**Framework inputs versus conclusions.** Inputs: a0 values (both footings), κ = 1/2,
G_N default, pc, c, H0 anchors, ρ_Lambda identity, ρ_crit definition, Planck comparison
values. Conclusions established: claims (1)–(2) of §1.1, the Jacobian rank/level-set
structure, the closure verdict (re-expression vs prediction), the alt-footing
decomposition, the negative-control record.

---

## 2. Derivation

### 2.1 Critical density from the Friedmann equation (which G)

Take the flat, one-coupling Friedmann closure with coupling **G_cosmo** in the source side:

```
H² = (8π G_cosmo / 3) ρ_total ,        ρ_total = ρ_crit  on k = 0          (2.1)
```

ρ_crit is defined by H² = (8π G_cosmo/3) ρ_crit, hence

```
ρ_crit = 3 H0² / (8π G_cosmo)                                              (2.2)
```

Dimension check: [H0²] = s⁻², [1/G_cosmo] = kg s² m⁻³ ⇒ [ρ_crit] = kg m⁻³ ✓.
Non-flat leading neglected term: H² = (8πG_cosmo/3)ρ − k c²/a²; relative to (2.2) the
term is −|Ω_K|·H0²·(…) with |Ω_K| ≤ 0.001 ⇒ ≤ 0.2 % shift in the density identification
(A2). No other approximation enters (2.2); it is the definition.

### 2.2 Framework scale identity (which G)

The declared input a0 = κ c √(G_N ρ_Lambda), κ = 1/2 **adopted** (FRAMEWORK_CONTRACT;
README "κ = ½ fitted, not derived"). All factors positive ⇒ square both sides and invert:

```
ρ_Lambda = a0²/(κ² G_N c²) = 4 a0²/(G_N c²)                                (2.3)
```

Dimension: [a0²] = m² s⁻⁴, [G_N c²] = m⁵ kg⁻¹ s⁻⁴ ⇒ [ρ_Lambda] = kg m⁻³ ✓.
The identity (2.3) is exact on D; no regime assumption was used. It is **not** a
derivation of κ: it is the same statement as the adopted input (see §6).

### 2.3 Ω_L and the G-ratio

```
Ω_L := ρ_Lambda/ρ_crit
     = [4 a0²/(G_N c²)] · [8π G_cosmo/(3 H0²)]                             (2.4)
     = (32π/3) (G_cosmo/G_N) (a0²/(H0² c²))
     = (32π/3) (G_cosmo/G_N) (a0/(H0 c))²
```

Coefficient ledger: 4 from κ⁻² with κ = 1/2; 8π from ρ_crit's denominator; 3 from
ρ_crit's numerator; 32 = 4·8; no hidden π, no hidden factor of 2. Signs: all factors
positive on D. Units: [a0/(H0 c)]² = [(m s⁻²)/(s⁻¹ · m s⁻¹)]² = 1; (G_cosmo/G_N) is
dimensionless ⇒ **Ω_L is dimensionless** ✓.

- Common coupling (G_cosmo = G_N stated): Ω_L = 32π a0²/(3 H0² c²) — claim (1) verbatim.
- Distinct couplings: the factor G_cosmo/G_N appears linearly — claim (2) verbatim.
- **Ratio sensitivity:** ∂lnΩ_L/∂ln(G_cosmo/G_N) = 1 exactly: a 1 % ratio deviation is a
  1 % Ω_L deviation; the ratio must be quoted with every number (§4, C4).

### 2.4 Consistency with the Einstein-curvature convention (G_E)

If one writes Λ_eff = 32π (G_E/G_N) a0²/c⁴ (vacuum curvature feels G_E, scale feels G_N),
the mass density it implies is

```
ρ_Lambda = Λ_eff c²/(8π G_E) = [32π(G_E/G_N) a0²/c⁴]·c²/(8π G_E) = 4 a0²/(G_N c²)   (2.6)
```

G_E cancels; (2.3) is unchanged. Hence the *critical-density* ratio G_cosmo/G_N (from
(2.2)) and the *Einstein* ratio G_E/G_N are distinct objects; this task's claim involves
only G_cosmo/G_N. (Contract's analogous-ratio requirement satisfied by carrying both.)

### 2.5 Alternative-footing decomposition (contract requirement)

Footing A (canonical): a0 = 9.3619e-11 m s⁻² with ρ_Lambda_A = 4 a0_A²/(G_N c²) =
5.8444e-27 kg m⁻³ and κ = 1/2 (density fixed, κ fixed — the canonical cell).

Footing B (alternative): a0_B = 1.1279e-10 m s⁻². Footings A and B **cannot share both
fixed ρ_Lambda and fixed κ** (contract). Two decompositions:

- **κ held fixed** at 1/2 ⇒ the density in (2.3) changes to
  ρ_eff(B) = 4 a0_B²/(G_N c²) = 8.4831e-27 kg m⁻³ = 1.451487 × ρ_Lambda_A.
- **ρ_Lambda held fixed** at ρ_Lambda_A ⇒ κ_eff(B) = a0_B/(c√(G_N ρ_Lambda_A))
  = 0.602388 = (1/2)·(a0_B/a0_A).

Key numerical observation (this is the dependency problem made concrete):

```
ρ_eff(B)/ρ_crit(67.4) = Ω_total(alt, 67.4) = 0.99417                       (2.7)
ρ_eff(B) = ρ_crit  ⟺  H0 = 67.203 km s⁻¹ Mpc⁻¹
```

so the alternative footing is exactly the **critical-density closure** up to the H0
anchor round-off: it is κ = 1/2 applied to ρ_total, and in the flat ΛCDM background
ρ_total = ρ_crit. The canonical footing is **not** the closure (see §4, C3a). Both
statements are re-expressions of the adopted κ on different density conventions — no
new input is derived.

### 2.6 Jacobian, rank and the null direction (task step 2)

Let F : D → ℝ₊, F(a0, H0) = (32π/3)(G_cosmo/G_N)(a0/(H0 c))². F is smooth (analytic) on D
and depends only on the ratio q = a0/(H0 c). The Jacobian is the 1×2 matrix

```
J = ( ∂F/∂a0 , ∂F/∂H0 ) = ( 2F/a0 , −2F/H0 )                              (2.8)
```

- Both entries are nonzero on D; a 1×2 matrix with a nonzero entry has rank exactly 1 ⇒
  **rank(J) = 1 everywhere on D**.
- Level sets: F = const ⟺ a0/H0 = const; the null space of J (in (ln a0, ln H0)
  coordinates, where J′ = (2, −2)) is spanned by (1,1): the simultaneous rescaling
  (a0, H0) → (t a0, t H0) leaves Ω_L invariant. One relation, three quantities.

**Consequence (prediction vs re-expression).** Assigning any two of {a0, H0, Ω_L}
fixes the third by an *identity*; the third quantity carries no independent information.
In particular "a0 = c H0 √(3 Ω_L G_N/(32π G_cosmo))" is the same equation as the adopted
κ = 1/2 input read in cosmological variables, and "Ω_L(a0, H0)" is a restatement of the
input ρ_Lambda identity. A genuine prediction would require an independent input
(a measured Ω_L,obs that did not enter a0 or H0) or an added hypothesis (closure Ω_L = 1);
the identity itself provides neither. The README k03 "H0 lock"
(κ = 1/2 at H0 = 67.4 ≡ κ = 0.461 at H0 = 73.0, fixed Ω_Lambda) is the same null
direction: holding a0 and Ω_L fixed forces κ_eff ∝ 1/H0; the exact ratio
H0(67.4)/H0(73.0) = 0.923288 reproduces 0.461/0.5 = 0.922 to 0.14 % (computed, C7;
README quotes 0.2 %).

---

## 3. Numerical footings (every dimensional example, both footings)

Common-coupling values (G_cosmo = G_N = 6.67430e-11, c = 299792458, κ = 1/2 adopted):

| quantity | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 |
|---|---|---|
| ρ_Lambda (kg m⁻³) | 5.8444e-27 | 8.4831e-27 (= 1.4515 × canonical) |
| Ω_L at H0 = 67.4 (km s⁻¹ Mpc⁻¹) | **0.684930** | 0.994168 |
| Ω_L at H0 = 73.0 | 0.583876 | 0.847488 |
| κ_eff (fixed ρ_Lambda_A) | 0.5 (by construction) | 0.602388 |
| H0 making ρ_eff = ρ_crit (km s⁻¹ Mpc⁻¹) | — | 67.203 |
| Λ = 32π a0²/c⁴ (m⁻²) | 1.0908e-52 | 1.5821e-52 |

ρ_crit(67.4) = 8.5329e-27 kg m⁻³; ρ_crit(73.0) = 1.0010e-26 kg m⁻³.
The canonical Ω_L = 0.6849 agrees with the Planck 2018 comparison value
Ω_Λ = 0.6847 ± 0.0073 to +0.0002 (+0.03 %) — the celebrated "a0 ↔ Ω_Λ" coincidence is
this identity at κ = 1/2 (a consistency, not a derivation; §4, C5b). All digits above are
the recorded outputs of `as003_verify.py` (60-digit mpmath; residual of the identity at
1e-49 relative).

---

## 4. Controls (each capable of failing; actual residuals recorded in as003_verify.out)

**C1 — Identity in two representations (numeric, 50-digit budget).** Ω_direct =
ρ_Lambda/ρ_crit vs Ω_form = (32π/3)(G_cosmo/G_N)(a0/(H0c))² at both footings × both H0
anchors × three ratios r ∈ {1, 1.001, 0.99}: 12 checks, relative residual < 1e-45 each.
**C1s — symbolic identity (sympy):** simplify(Ω_direct − Ω_form) ≡ **0 exactly** (no
floats). This distinguishes the exact identity from a finite numerical consistency.

**C2 — Jacobian.** Numeric derivatives (mpmath Richardson extrapolation) vs closed forms
(2.8): relative residual < 1e-9 at all four cells; ∂F/∂a0 > 0, ∂F/∂H0 < 0; rank = 1.
Null direction: Ω(t a0, t H0) = Ω(a0, H0) for t ∈ {0.31, 3.7} to 1e-45. Non-null control:
Ω(1.1 a0, H0) differs from Ω(a0, H0) by 21 % — the map genuinely responds to its inputs
(the round-trip trap would have passed if F were constant; it is not).

**C3 — Closure verdicts (comparisons with the Planck 2018 value, flagged as such; no fit).**
- C3a: canonical footing gives Ω_L = 0.68493; the strict closure hypothesis ρ_Lambda =
  ρ_crit means Ω_L = 1, excluded at **(1 − 0.68493)/0.0073 = 43.2σ** (comparison).
- C3b: alternative footing gives Ω_total = 0.99417; deviation from 1 is 0.6 % — the alt
  footing *is* the critical-density closure up to the H0 round-off; the same formula that
  excludes the canonical closure *succeeds* here, so the control fails and passes on the
  two footings respectively — exactly what a discriminating control must do.
- C3c: H0 making the alt footing exactly critical = 67.203 km s⁻¹ Mpc⁻¹, within 0.3 % of
  the 67.4 anchor.

**C4 — G-ratio.** Ω_L(r·G_N)/Ω_L(G_N) = r to 1e-45 (r ∈ {1.001, 0.99}); log-sensitivity
∂lnΩ_L/∂ln(G_cosmo/G_N) = 1 − 4e-50. The ratio is therefore not absorbed into a0 or H0
and must be quoted.

**C5 — Negative control (circularity), task control 1.** (a) Construct
a0′ = c H0 √(3 Ω_L,in G_N/(32π G_cosmo)) from Ω_L,in = 0.6847; feeding a0′ back returns
Ω_L = 0.6847 identically (residual 1e-49). **Flagged CIRCULAR**: the agreement is by
construction, not evidence — the control passes only if so flagged, and it is.
(b) Independent-input check, same identity: the *galaxy-datum* canonical a0 gives
Ω_L = 0.68493 vs 0.6847 (finite residual +0.03 %), while the alt a0 gives 0.99417 (45 %
off) — the identity is not self-fulfilling; it discriminates between its inputs, which is
the condition that makes the control capable of failing. (A residual of exactly 0 against
both inputs would have been the signature of a broken control; it does not occur.)

**C6 — Boundaries / normalization (task control 2).** No limiting regime exists in an
algebraic identity (there is no deep or Newtonian regime to check), so per the task
wording: (a) Ω_L → 0 as a0 → 0⁺ at fixed H0 (values 1e-60 → 0); (b) Ω_L ∝ 1/H0² :
Ω(H0×1000) = Ω(0)/1e6 to 1e-5 relative; (c) dimension check both sides (dimensionless,
§2.3); (d) monotonicity signs ∂F/∂a0 > 0, ∂F/∂H0 < 0.

**C7 — k03 H0-lock.** κ_eff(73.0)/κ_eff(67.4) at fixed a0 and fixed Ω_L = H0(67.4)/H0(73.0)
= 0.923288 vs README 0.461/0.5 = 0.922: residual 0.14 % (README quotes 0.2 %).

**C8 — footing decomposition.** κ_eff(B) = 0.6023884 = (1/2)(a0_B/a0_A) (exact to 1e-45);
ρ_eff(B)/ρ_Lambda_A = (a0_B/a0_A)² = 1.4514872 (exact).

**C9 — Λ.** Λ = 32π a0²/c⁴ = 1.0908e-52 m⁻² (canonical), and Λ_eff = (G_E/G_N)Λ carries
the Einstein ratio separately.

**Harness failures recorded (transparency).** (i) First version of the script used
km_s_Mpc = 1000/pc (missing 1e6 pc per Mpc): ρ_crit came out 1e12 too large; the
cross-checks C3a/C3b/C6b **failed** — the controls caught the unit error (this is their
value; the identity checks C1 were insensitive because both representations share H0).
(ii) macOS refused to lower RLIMIT_AS below the interpreter's address space; the memory
cap is therefore reported as measured peak RSS (55.5 MB) with CPU rlimit hard-enforced
at 120 s. Actual run: 0.109 s wall, 1 thread.

---

## 5. Strongest surviving statement (domain and exact content)

**Theorem (algebraic, exact on D = {a0 > 0, H0 > 0, G_N > 0, G_cosmo > 0, c > 0}).**
With the adopted framework input ρ_Lambda = 4 a0²/(G_N c²) (κ = 1/2, not derived here)
and the definition ρ_crit = 3 H0²/(8π G_cosmo):

    Ω_L := ρ_Lambda/ρ_crit = (32π/3)(G_cosmo/G_N)(a0/(H0 c))²          (exact identity)

1. The task's claim (1) holds verbatim under a stated common coupling; claim (2) holds
   verbatim with the stated G-ratio factor. **Both claims SUPPORTED** as exact algebra.
2. The map (a0, H0) ↦ Ω_L has **Jacobian rank exactly 1** on D, with level sets
   a0/H0 = const (null direction = joint rescaling of a0 and H0). Assigning two of
   {a0, H0, Ω_L} makes the third a **re-expression of inputs**, never a prediction.
3. The critical-density closure ρ_scale = ρ_crit is a **dependency, not a derivation**:
   - on the canonical footing it is excluded by the Planck comparison at ≈ 43σ,
   - on the alternative footing it is realized to 0.6 % (H0 = 67.203 vs 67.4 km s⁻¹ Mpc⁻¹)
     because that footing's density is ρ_total = ρ_crit — a re-labelling of the adopted
     κ = 1/2, not an independent fix of a0.
4. κ = 1/2 remains an adopted input; nothing in this task removes its freedom,
   consistent with the k01 zero-mode/k03 H0-degeneracy record. The identity's success
   modes (0.03 % consistency vs Planck; k03 lock to 0.14 %) are finite numerical
   consistency checks — an exact identity and a numerical check are not the same thing,
   and the report keeps them distinct.

**Conditions of this conditional theorem.** κ = 1/2 adopted (A3); flat background only
for the alt-footing reading (A2, |Ω_K| ≤ 0.001, ≤ 0.2 % effect); Planck numbers are
comparison values, not fitted inputs; G-ratio conventions as stated (A4).

---

## 6. Transfer to the full theory; the affected gate; open dependencies

**Affected operative gate.** Amended requirement 13 (cosmological acceleration-scale
relation). This task's result does not pass or fail that gate; it characterizes its
dependency structure: the a0–(H0, Ω_L) relation is rank-1, so requirement 13's identity
content carries zero independent predictive power beyond the adopted κ and the measured
{H0, G-ratio}; consistency with Ω_Λ,obs (0.03 %) and the k03 lock are restatements of the
adopted normalization. This agrees with README's explicit position: the a0–Λ relation is
phenomenological input unless an independent argument removes the κ freedom.

**First additional implication needed.** A **same-action derivation of κ** (or an
independent physical mechanism that fixes κ without fitting), because every numerical
"prediction" flowing from (2.4) — Ω_L, a0(H0), the alt-footing closure — is a
re-expression of κ = 1/2. Second: the value (or a derivation) of **G_cosmo/G_N** in the
completion's cosmology, without which Ω_L numbers cannot be single-valued; the ratio is
exactly the leverage point (∂lnΩ_L/∂ln(G_cosmo/G_N) = 1). Third: the density convention
behind κ (ρ_DE vs ρ_total) — the two footings are two different closures with the same
adopted κ; the identity cannot choose between them.

**What this result does not establish.** It does not derive κ; does not fix
G_cosmo/G_N; does not adjudicate the density convention; does not touch dynamics,
kernels, lensing, stability or causality (criterion B is unaffected); the 43σ exclusion
is a data comparison, not a theorem. Nothing here transfers to Q/RAR/MU2/EXP/MONO;
no branch was imported and none is claimed.

---

## 7. Reproducibility

- `as003_verify.py` — the bounded verifier (rlimits inside; actual run 0.109 s, 55.5 MB
  peak RSS, 1 thread; 60-digit mpmath; deterministic, no RNG).
- `as003_verify.out` / `as003_verify.err` — raw outputs (37 checks, 0 FAIL,
  1 CIRCULAR-FLAGGED).
- `AS003_omegaL_identity.lean` — Lean 4 certificate (§8).
- All files hashed in result.json (`artifacts_sha256`).