# AS026 — Exact inverse of the algebraic a0 line

**Run:** `AS026-r1-20260928T000625Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter); Hermes Agent focused subagent
**Branch for conclusions:** Q (algebraic a0-line). RAR, MU2, EXP, MONO enter only as labelled comparison curves — never imported for conclusions (FRAMEWORK_CONTRACT branch discipline).
**Task hash:** `39753bcaee627960aec61effa8ed011953c9fa360efe899320a8058d2348aeb3`
**Sources:** README.md, FRIED_CHICKEN_SPEC.md, peer_review README — all hash-verified against SOURCE_MANIFEST.json pins (see result.json `input_sha256`); STANDING.md rev. 9–11 blocks read and respected (Q branch is a historical/diagnostic branch; the operative target is filtered MONO with criterion B — this task's result is a Q-branch theorem with explicit conditional transfer statements, not an operative-target pass).

---

## 1. Precise claim, symbol dictionary, premises

**Claim (dimensionless, exact).** Let `x = g/a0 ≥ 0`, `y = B/a0 > 0`. On the Q branch
`g² = B² + a0·B` ⇔ `x² = y² + y`, the map `x ↦ y` defined by

```
y(x) = (sqrt(1 + 4 x²) - 1) / 2 = 2 x² / (sqrt(1 + 4 x²) + 1)          (dimensionless)
B(g) = 2 g² / (sqrt(a0² + 4 g²) + a0)                                   (SI)
```

is the unique inverse on the physical domain: for every `g ≥ 0` it returns the unique
`B ≥ 0` solving the Q-line, it is strictly increasing on `[0, ∞)`, it maps `[0, ∞)` onto
`[0, ∞)` bijectively, and it interpolates exactly between the two limiting regimes:

```
deep (x → 0,  B ≪ a0):    y  =  x² − x⁴ + 2x⁶ − 5x⁸ + 14x¹⁰ + O(x¹²)   (B ≈ g²/a0)
Newtonian (x → ∞, B ≫ a0): y =  x − ½ + 1/(8x) − 1/(128x³) + O(x⁻⁵)   (B ≈ g − a0/2)
knee (y = 1):              x = sqrt 2   ⇔   g_knee = sqrt(2)·a0
root bracket:               x²/(1+x²) < y(x) < x²    for all x > 0
derivative:                 dB/dg = 2g/sqrt(a0² + 4g²) ∈ [0, 1)       (y'(x) = 2x/sqrt(1+4x²))
```

**Root discrimination is NOT automatic**: the raw algebraic equation has two roots for every
g; the *other* root `y_neg = −(1+sqrt(1+4x²))/2` satisfies `y_neg² + y_neg = x²` exactly
(verified symbolically, numerically to 80 dps on the whole grid, and in Lean). It is
rejected by the physical branch conditions — `y = B/a0 > 0` (`B = g_N > 0` is the framework
contract's convention), the deep-limit sign (`y_neg ~ −x − ½` vs physical `+x² → x − ½`),
and the `g = 0` boundary (`B = −a0` vs physical `B = 0` by continuity from `g > 0`). The
forward law alone cannot reject it; the domain does. A mirror-image sign perturbation
(`−y_plus`) IS rejected by the forward law itself (measurement, below).

**Symbols / premises.**
- Framework inputs (not derived here): `a0 = κ·c·sqrt(G·ρ_Λ)`, κ = 1/2 **adopted**;
  both footings `a0_can = 9.3619e−11 m s⁻²` and `a0_alt = 1.1279e−10 m s⁻²` carried
  separately (ratio 1.204776808127; fixed-ρ_Λ effective κ = 1.204776808127; fixed-κ
  ρ-ratio 1.451487157400 — consistent with sibling AS010/AS013 bookkeeping);
  `r_M = sqrt(G·M_b/a0)`; `v_flat⁴ = G·M_b·a0`; `B = g_bar = g_N > 0`.
- `G = 6.67430e−11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI).
- Derived here: the exact inverse, its monotonicity, uniqueness, domain statement,
  asymptotics with leading neglected terms, knee mapping, root bracket, conditioning
  derivative, and the branch-fidelity comparison table (approach rates).

## 2. Derivation of the stable inverse (Step 2 of the work order)

Solve `y² + y − x² = 0` for y (quadratic in y, discriminant `1 + 4x²`):

```
y = (−1 ± sqrt(1 + 4x²))/2.
```

The plus root is `y₊ = (sqrt(1+4x²) − 1)/2 ≥ 0`; the minus root `y₋ = −(1+sqrt(1+4x²))/2 < 0`.
Rationalization (multiply numerator and denominator of `y₊` by `sqrt(1+4x²) + 1`,
using `(t−1)(t+1) = t² − 1 = 4x²`):

```
y₊ = (t − 1)/2 = (t − 1)(t + 1) / (2(t + 1)) = 4x² / (2(t + 1)) = 2x²/(t + 1).    (exact identity)
```

**Monotonicity.** `dy/dx = 2x/sqrt(1 + 4x²) ≥ 0`, zero only at x = 0; equivalently from the
forward law by implicit differentiation `2x dx = (2y + 1) dy` ⇒ `dy/dx = 2x/(2y+1) =
2x/sqrt(1+4x²)`. Strictly increasing on `[0, ∞)`; `y(0) = 0`; `y → ∞`. Both directions also
proved algebraically in Lean (H: strict monotonicity; G: uniqueness; K/K′: surjectivity).

**Comparison with the subtractive quadratic root near g = 0 (numerics, float64).** The
subtractive form `(t − 1)/2` suffers catastrophic cancellation: at x = 1e−3 relative error
6.2e−11, at x = 1e−5 8.3e−8, at x = 1e−7 8.0e−4, at x ≤ 1e−9 the float64 result is 100%
wrong (y underflows to garbage — measured). The rationalized form keeps relative error
~1e−16 at every x on the same float64 sweep (7 points, x = 10⁻³…10⁻¹⁵). At 80 decimal
digits the two forms agree to 80 digits at every grid point (they are the same function;
check `res_rationalized_symbolic = 0` and max roundtrip residual 4.0e−72). The
rationalized form is the numerically stable representative of the exact inverse.

## 3. Intermediate algebra, signs, units, and domain of each limiting regime (Step 3)

All factors/signs/units are tracked above; both forms are dimensionless (a0 drops out),
and the SI form `B(g) = 2g²/(sqrt(a0²+4g²)+a0)` restores `[B] = m s⁻²`.

- **Deep regime** (x → 0, i.e. `g ≪ a0`, `B ≪ a0`): exact series
  `y = x² − x⁴ + 2x⁶ − 5x⁸ + 14x¹⁰ + O(x¹²)` (alternating Catalan coefficients).
  Leading behaviour `B ≈ g²/a0` — the deep-law rearrangement `g = sqrt(a0·B)`.
  **Leading neglected term: `−x⁴` (i.e. `−g⁴/a0³`), domain of the truncation
  `y = x²(1 + O(x²))` is `x² ≪ 1`.** Exact correction identity available:
  `y/x² = 1/(1+y)` (verified 1e−10 vs analytic at y = 1e−10).
- **Newtonian regime** (x → ∞): exact series `y = x − ½ + 1/(8x) − 1/(128x³) + O(x⁻⁵)`.
  Leading behaviour `B ≈ g − a0/2`: the total acceleration exceeds the Newtonian one by a
  constant offset a0/2 (the historical "s^TX" offset structure of the retired α = 1 line —
  recorded here as pure algebra, no claim about any operative branch).
  **Leading neglected term: `+1/(8x)`; next `−1/(128x³)`; domain `1/x ≪ 1`.**
  Numerically at y = 1e8: `|(x−y) − ½| = 1.250000e−9` vs `1/(8y) = 1.25e−9` with second
  order `1/(16y²) = 6.25e−18` matched to 6.25e−18 (measured).
- **Exact root bracket** (proof-level, holds for all x > 0, no grid needed): from
  `y = x²/(y+1)` with `0 < y`:
  `y < x²` and `y > x²/(1 + x²)`  ⇒  `x²/(1+x²) < y(x) < x²`. Verified on all 181 grid
  points; proves any root is bracketed without treating the grid as a proof.
- **Knee mapping.** At `B = a0` (y = 1, i.e. r = r_M by definition of r_M): `x² = y² + y = 2`
  ⇒ `g(r_M) = sqrt(2)·a0` **on both footings**:
  `g_knee = 1.3239725949581e−10` (canonical) and `1.5950914770006e−10` m s⁻² (alternative).
  Lean: `knee_iff` (y=1 ↔ x²=2) and `knee_unique` (x = sqrt 2 is the unique preimage on
  x ≥ 0).
- **Grid.** Diagnostic grid per work order: `y = 10^k`, k = −10…8 step 0.1 → **181 points**.
  181-point grid residuals: max forward-law residual 2.11e−81, max inverse roundtrip
  3.98e−72 (both pure 80-dps rounding; the identities are exact — sympy residual 0, Lean
  proof). Grid is monotone in x (181/181).

## 4. Independent checks in a different representation (Step 4)

1. **Symbolic (sympy, exact):** `y² + y − x² ≡ 0`, `2x²/(t+1) − (t−1)/2 ≡ 0`,
   `d/dx[(t−1)/2] − 2x/sqrt(1+4x²) ≡ 0` — three exact residuals, all identically 0.
2. **High-precision substitution (mpmath 80 dps):** direct substitution of the inverse into
   the original equation with dimensional SI values at 14 (g, a0-footing) pairs, both
   footings: max relative residual 2.25e−81. This is a finite numerical consistency check
   of an algebraic identity (exactness is established by 1 and the Lean file).
3. **Direct differentiation (finite difference at 80 dps):** `dB/dg` from a centered
   difference with h = 1e−40 at x ∈ {1e−4, 0.5, 1, 2, 1e2}: max relative error 6.5e−39 vs
   `2x/sqrt(1+4x²)`. Conditioning: `0 ≤ dB/dg < 1`, `dB/dg(0) = 0` (quadratic contact,
   y ~ x²), `dB/dg(1e30) = 0.999999999999999999999999999999999999999999999999999999999999875`
   (→ 1).
4. **Lean 4 certificate (18 theorems, zero sorry, axioms {propext, Classical.choice,
   Quot.sound}):** see section 7.

## 5. Negative controls (Step 5 — each capable of failing, each measured)

- **NC1a — sign-perturbed inverse `y_pert = −2x²/(sqrt(1+4x²)+1) = −y₊`:** the FORWARD LAW
  rejects it: max relative residual over the full grid = **1.9999999998** (O(1), i.e. the
  perturbed candidate is not a solution). It also has the wrong deep sign (y_pert ~ −x²).
- **NC1b — true other root `y_neg = −(1+sqrt(1+4x²))/2`:** the raw quadratic ACCEPTS it
  (max absolute residual 1.9e−65 on the grid — i.e. 0 to numerical precision); it is
  negative on all 181 grid points; its g=0 boundary is B = −a0 and its deep limit is
  −x − ½. **This is the "discarding the unphysical root is NOT automatic" control**: the
  forward equation alone cannot reject it; the physical branch (y = B/a0 > 0, B = g_N > 0),
  the limit behaviour and the continuity-selected g = 0 value do.
- **NC2 — perturbed coefficient (discriminant 4 → 3, `y_pert = 2x²/(sqrt(1+3x²)+1)`):**
  the forward law rejects it with max relative residual **0.33333** over the grid and
  **0.15047** exactly at the knee (x = √2, y_pert = 4/(√7+1) ⇒ residual
  (y_pert² + y_pert − 2)/2 = 0.150472…). Control proves the checker can fail.
- **NC3 — subtractive quadratic root in float64 near g = 0:** relative error grows
  6.2e−11 → 8.3e−8 → 8.0e−4 → **1.0 (100%)** as x → 1e−9, while the rationalized form
  stays ~1e−16 at the same points (7-point float64 sweep x = 10⁻³…10⁻¹⁵, 80-dps reference).
  The two forms agree to 80 dps at high precision — same function, different cancellation
  behaviour.

All controls **passed as designed** (i.e., the perturbed objects were rejected or the
recorded phenomenon was exhibited with actual numbers, not booleans).

## 6. Branch fidelity: identical deep limit ≠ identical finite law

Comparison only — Q is the conclusion branch. At fixed y, the five framework branches give
different total accelerations x(y) even though all five satisfy `x ~ sqrt(y)` as y → 0
(exact rates):

| branch | x(y) form | exact deep approach `x/sqrt(y) − 1` at y = 1e−10 |
|---|---|---|
| **Q** | `sqrt(y²+y)` | `5.0000e−11` (= y/2 + O(y²)) |
| RAR | `y/(1−e^{−sqrt y})` | `5.0000e−6` (= sqrt(y)/2 + O(y)) |
| MU2 | solve `x·(1−(1+x/2)^{−2}) = y` | `3.7500e−6` |
| EXP | solve `x·(1−e^{−x}) = y` | `2.5000e−6` |
| MONO | `y·nu_mono(y)` (contract splice y* = 2.3374) | `5.0000e−6` (= RAR below splice) |

At y = 0.1 (finite, well inside the interpolation): `x_Q/x_RAR = 0.899159`,
`x_Q/x_MU2 = 0.928792`, `x_Q/x_EXP = 0.964809`, `x_Q/x_MONO = 0.899159` — i.e. the branches
differ by 3.5–11% of the total acceleration at y = 0.1 while sharing the exact deep line.
Quantitative statement of the task's principle: the Q-branch inverse computed here must
never be silently identified with the inverse of any other branch; matching one asymptote
(the deep line) does not make two kernels equivalent. Transfer of this result to the
operative MONO branch requires the explicit bridge (child AS026.C01).

## 7. Lean 4 certificate

File: `AS026_exact_inverse_qline.lean` (also copied into this run dir). Verified with
`cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS026_exact_inverse_qline.lean`,
**exit 0**, zero sorry, and `#print axioms` for all 18 theorems = **{propext,
Classical.choice, Quot.sound}** (18/18, from `AS026_exact_inverse_qline_axioms.lean`
output). Theorems: A `qline_yQ_nonneg`; B `qline_yQ_identity` (forward law);
A′ `qline_yQ_pos`; C `rationalized_form`; D `other_root_satisfies_raw_law`; E
`other_root_negative`; F1/F2 `physical_root_at_zero`/`other_root_at_zero`; G
`unique_nonneg_root`; H `qline_inverse_strict_mono`; I `qline_inverse_deriv`; J1/J2
`knee_iff`/`knee_unique`; K/K′ `inverse_composition`/`surjective_on_nonneg`; L
`injective_on_nonneg`; M1/M2 `sign_perturbation_rejected`/`sign_perturbation_outside_domain`.

Debug trail (honest): first compile round had 6 errors — forward reference
(qline_yQ_identity), `HasDerivAt.sqrt` requiring `≠ 0` (not `> 0`), slope normalization
`4*(2*x)` vs `8*x`, `field_simp` producing an inequality-shaped goal (cross-multiplied
equalities with side conditions — replaced by `eq_div_iff` + pure ring), `Real.eq_sqrt`
replaced by `norm_num` (which evaluates √9 = 3), and an inner `sq_sqrt` rewrite needed in
`inverse_composition`. All fixed; final compile clean; axiom audit 18/18.

## 8. Application to the framework (both footings, scale bookkeeping)

- Knee locations: `g(r_M) = √2·a0` = **1.32397e−10** (canonical) / **1.59509e−10** m s⁻²
  (alternative). `B(r_M) = a0` identically by definition of r_M.
- MOND radii: M_b = 1e9 M_sun → r_M = 1.220 kpc (canonical) / 1.112 kpc (alternative);
  M_b = 1e11 M_sun → 12.20 / 11.12 kpc.
- Vacuum densities implied by the two footings at κ = ½: ρ_Λ = 5.8444e−27 kg m⁻³
  (canonical) / 8.4831e−27 (alternative); the two footings never share fixed ρ_Λ AND fixed
  κ simultaneously (contract).
- κ = ½ remains adopted, not derived; this algebraic result is κ-independent (a0 cancels
  in dimensionless form) and therefore cannot remove the normalization freedom.

## 9. Strongest surviving statement (Step 5) and next implication

**Surviving statement.** On the declared Q branch, for every `g ≥ 0`, the unique physical
(`B ≥ 0`) solution of `g² = B² + a0·B` is `B = 2g²/(sqrt(a0²+4g²)+a0)`; the map is
bijective, strictly increasing, has the exact asymptotic regimes (deep `B ≈ g²/a0 − g⁴/a0³`,
Newtonian `B ≈ g − a0/2 + a0²/(8g)`), the exact knee `B = a0 ⇔ g = √2·a0`, the exact bracket
`g/a0·g/(a0+g²/a0) < B < g²/a0`, and `dB/dg ∈ [0,1)`. All of this is certified by the Lean
proofs (exact identities) and by the 80-dps numerical controls (consistency checks). The
other algebraic root is rejected by the physical domain, never by the raw equation.

**First additional implication needed to transfer to the full theory.** The operative
target is *filtered MONO with criterion B*, whose forward map `g = B·nu_mono(B/a0)` is NOT
algebraically invertible and differs from the Q-inverse by 0.9–11% in the interpolation
region (measured above). Transfer requires an explicit error budget for replacing the
operative MONO inverse by the Q-branch inverse in any same-action calculation — a
branch-translation lemma, not a silent identification. This is the child spec below.

**Affected operative gate:** requirement-1 content (knee/interpolation forward mapping
through the heat filter) — any inverse used in the operative weak-field quasistatic
equations (`∇²u = 4πGρ_b`, `∇²Φ = 4πGρ_b + S*∇·[(nu_mono(|∇Su|/a0) − 1)∇Su]`) must be the
MONO inverse, whose difference from the Q-inverse is quantified here.

## 10. Child proposal (ready spec, NOT dispatched — no spawn mechanism in this worker)

- **ID:** AS026.C01 — "Branch-transfer error of the Q-inverse as an enclosed-mass profile
  estimator against the operative MONO branch".
- **Claim:** for a measured circular-speed profile v(r), the Q-inverse mass profile
  `M_Q(<r) = B(r)·r²/G`, `B = 2g²/(√(a0²+4g²)+a0)`, deviates from the operative MONO mass
  profile `M_mono(<r)` by a bounded, computable factor `1 + f(y)`, with `f(y)` from the
  branch table (0 at the deep line, ~0.11 at y = 0.1, → 0 Newtonian); derive the exact
  `f_Q_mono(y)` band (Q vs MONO after the heat filter on a spherical source) and state the
  observable (rotation-curve shape/inclination-degenerate signature) that discriminates
  the two inverses at fixed g.
- **Parent:** AS026 run `AS026-r1-20260928T000625Z-dsv4f-hermes` (hashes in result.json).
- **Duplicate check:** scoured AS/MY manifests + FGF queue. Closest siblings are AS027
  (mu_Q(x) effective response — the forward Q response, not the mass-profile inversion
  error), AS030 (shared-deep-limit theorem — no operative-branch transfer numbers), AS045
  (Newtonian tail ordering), AS046 (numerical conditioning of the inverse), AS453
  (noise-induced bias of B(g) — single-point bias, not the branch-transfer mass-profile
  error). Distinct fingerprint: (Q-inverse as mass estimator, MONO-through-filter transfer
  error, rotation-curve observable).
- **Controls:** (i) deep limit: f → 0 as y → 0 on both footings; (ii) Newtonian limit:
  f → 0 as y → ∞; (iii) a perturbed filter width must move f (sensitivity); (iv) full-grid
  residual of the Q-inverse forward law re-checked.
- **Dispatch state:** NOT DISPATCHED (no subagent spawn mechanism available); ready spec
  for the orchestrator per FIRST_PRINCIPLES_AND_BRANCHING.md.

## 11. Reproducibility and bounds

- Code: `compute_as026.py` (this dir) → `raw_output.json` / `raw_output.stderr`.
- Bounds (declared AND enforced): wall clock 120 s via `signal.alarm` (observed elapsed
  0.142 s); threads 1 (single-process, no threads/subprocesses); memory 512 MB target —
  `RLIMIT_AS` rejected by macOS ("current limit exceeds maximum limit"), recorded as not
  enforceable, observed peak RSS far below 512 MB (0.35 s of mpmath/sympy work).
- Precision: mpmath 80 decimal digits; sympy exact; numpy float64 only for the dedicated
  float64-cancellation control.
- Hashes of every artifact and input: result.json `artifacts_sha256` / `input_sha256`.

## 12. Limitations

- Q-branch theorem only; no operative-branch (MONO) conclusion is claimed. Transfer needs
  AS026.C01-style explicit bridges (branch-translation error budget).
- The raw-law-accepts-both-roots fact means any numerical or analytic use of "the inverse"
  must state the physical branch; the Lean certificate formalizes this.
- κ = 1/2 remains adopted (framework input), unchanged by this algebra; a0 cancels in
  dimensionless form, so both footings carry the same dimensionless theorem with the SI
  knee values listed above.
- This is a constitutive/kinematic audit; no dynamics, no stability, no lensing content.
- Grid checks are finite consistency checks of exact identities (the identities are the
  Lean/sympy certificates); the float64 sweep is a numerical-stability demonstration.
