# AS064 — Sensitivity of the selected coefficient to channel asymmetry

**Run:** `AS064-r1-20260928T085213Z-aa76d89c`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter; Hermes subagent platform; identity taken from the executing agent's own system context)
**Started:** 2026-09-28T08:52:13Z · **Finished:** 2026-09-28T09:46:55Z (see result.json)
**Group/priority:** A03 (coefficient mechanisms and their missing premises) · P1 · derivation
**Branch:** CORE coefficient; conditional MU_n statistical response. **No branch is silently identified** — Q, RAR, MU2, EXP, MONO remain distinct; nothing here transfers to the operative filtered-MONO / criterion-B target (see §10).

---

## 1. Task integrity and pinned sources

- Seed sha256: `190cb46208aa72788edaeca8a34cccc1d1e38af39805c6e306aa11eb44415448` — **verified equal** before execution (shasum -a 256 on the on-disk file). Not renamed, not paraphrased: executed as written.
- Pinned sources verified against SOURCE_MANIFEST (recorded in result.json `input_sha256`):
  - `deepseek_push/PD01_polarization_count.py` = `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d` ✓
  - `deepseek_push/PD08_particle_free_derivation.py` = `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb` ✓
  - `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` = `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c` ✓
- Contracts read before computing: FRAMEWORK_CONTRACT.md and RESULT_CONTRACT.json (hashes in result.json).

## 2. Symbol dictionary, assumptions, boundary conditions

Framework base (adopted, not derived here — the seed supplies no independent argument):
- `a0 = kappa c sqrt(G rho_Lambda)` with **kappa = 1/2 ADOPTED as input**; `s = c sqrt(G rho_Lambda)` is the vacuum rate; `Y = g/s` dimensionless; `r_M = sqrt(G M_b/a0)`; `v_flat^4 = G M_b a0`.

The OR-class channel response (PD01 A1–A3/PD08, treated as the task's declared premises):
- n equal/independent channels, per-channel engagement `p_i(Y)`, with the OR-class boundary conditions
  **p_i(0) = 0** (zero drive → zero engagement; the action's frozen vacuum), **p_i'(0) = b_i** (linear coefficients — the L230 fraction identity fixes the *sum*; the *split* is the freedom under test), **p_i(∞) = 1** (saturation; mu(∞) = 1, the L230 normalization);
- response `mu(Y) = 1 - PRODUCT_i (1 - p_i(Y))` (OR; the corpus's μ_n family is the p = Y/(1+Y) member, PD01 A2);
- seed's asymmetry split: `b1 = 1 + epsilon`, `b2 = 1 - epsilon`, so `b1 + b2 = 2`.
  The seed's "lambda" is interpreted as the asymmetry strength **lambda := eps**, evaluated at the mandatory
  diagnostic counterexamples **lambda ∈ {1/2, 1, 2}**; a second reading (scale asymmetry,
  `p_2(Y) = Y/(1 + lambda Y)`) is evaluated in parallel (§5).
- Spherical deep-MOND matching (PD08 step 5): `div(mu grad Phi) = 4 pi G rho_b`, point source:
  `r^2 mu g = G M`, deep limit `mu ~ mu'(0) Y` ⇒ `g^2 = (s/mu'(0)) g_N` ⇒ the a0-line with **a0 = s/mu'(0)**, **kappa = a0/s = 1/mu'(0)**.

**Conclusions to be established (not inputs):** the invariance of mu'(0) (hence of kappa) under splits of a fixed
slope sum; the first order at which asymmetry becomes visible; the exact response residuals.

Numerical conventions (framework defaults): G = 6.67430e-11 m³ kg⁻¹ s⁻², c = 299792458 m/s,
M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m. G_N = G used throughout the a0-chain; G_bare, G_cosmo
not used (no coupling-ratio question arises in this task; recorded as untouched).

## 3. Derivation (all steps, signs, units)

### T0 — the OR chain rule (arbitrary completions)
mu = 1 − (1−p1)(1−p2). Then
mu'(Y) = p1'(Y)·(1−p2(Y)) + p2'(Y)·(1−p1(Y)).
At Y = 0 with p_i(0) = 0: **mu'(0) = p1'(0) + p2'(0) = b1 + b2 = 2**. Only p_i(0) = 0 and differentiability
are used: the deep slope is the **sum** of the channel slopes for every completion shape. Verified
symbolically by sympy on the generic composition (T0a, residual exactly 0) and for n = 3, 5 channels
(T0b): mu_n'(0) = Σ a_i. The general-n statement: for equal unit channels the slope is n, hence
**kappa = 1/n** (T6, n = 1,2,3,7), and any redistribution of a *fixed sum* leaves the coefficient invariant.

### T1 — the L230 matching chain and the sensitivity asked for
Deep Poisson with mu ~ S·Y, S = b1+b2: r²·(S g/s)·g = G M ⇒ g² = (s/S)(GM/r²) = (s/S) g_N ⇒
a0 = s/S, kappa = a0/s = 1/S. With S = 2: **kappa = 1/2 exactly for every eps**, and
**d kappa/d eps = 0 identically** (T1c). *The selected coefficient's sensitivity to channel asymmetry at
its defining (deep) order is exactly zero.*

### T2 — rational completions p_i(Y) = b_i Y/(1+Y): first visible order
Closed form (sympy-verified, also Lean-certified):
mu_r(Y) = 2Y/(1+Y) − (1−eps²)Y²/(1+Y)²  [dimensionless; units: Y = g/s].
Series: mu_r = 2Y − (3−eps²)Y² + (4−2eps²)Y³ − (5−3eps²)Y⁴ + O(Y⁵).
- linear term: 2Y — identical to the symmetric μ₂(Y) = 1−(1+Y)^(−2) = 2Y−3Y²+4Y³−5Y⁴+…;
- **first visible asymmetry at quadratic order** with dimensionless coefficient shift **Δc₂ = eps²** (T2a/T2b);
- Newtonian limit: mu(∞) = 1 + eps² (T2c) — the asymmetric rational family **breaks the L230
  normalization at exactly eps²** (exact, not numerical);
- pointwise residual vs the symmetric response: |mu_r − mu_2|(Y) = eps²Y²/(1+Y)² (T2d), so
  sup over the transition band Y ∈ [0,1] is **eps²/4** (at Y = 1), i.e. 6.25% of mu_2(1) = 3/4 at eps = 1/2.

Dimensions/units: everything is in the dimensionless variable Y = g/s; the transition band maps to
g ∈ [s/10, s]: canonical s = 2·9.3619e-11 = 1.87238e-10 m/s², band [1.872e-11, 1.872e-10] m/s²;
alternative s = 2·1.1279e-10 = 2.2558e-10 m/s², band [2.256e-11, 2.256e-10] m/s². The two footings
carry kappa = 1/2 **fixed** and therefore *different* densities by (a0_alt/a0_can)² = 1.4514872
(rho_L = 5.844412454021875e-27 kg/m³ canonical vs 8.483089619559097e-27 kg/m³ alternative; never conflated).

### T3 — power-law completions p_i(Y) = 1 − (1+Y)^(−b_i): exact invisibility
(1−p1)(1−p2) = (1+Y)^(−b1)·(1+Y)^(−b2) = (1+Y)^(−(b1+b2)) = (1+Y)^(−2), hence
**mu_p(Y) = 1 − (1+Y)^(−2) IDENTICALLY for every eps** (T3a; residual 0, exact algebra; Lean-certified
`powerlaw_collapse` through Real.rpow_add). Boundary conditions p_i(0) = 0, p_i(∞) = 1, mu(∞) = 1 are
preserved for every eps (T3b). *In this completion class channel asymmetry is invisible at EVERY order.*

### T4 — admissibility and the seeded diagnostics lambda ∈ {1/2, 1, 2} (theta)
The OR-class engagement is a fraction: p_i(Y) ∈ [0,1] for Y ≥ 0 forces b_i ∈ (0,2), i.e.
**eps ∈ (−1,1)** (scanned grid, step 1e-3, endpoints −0.99910…/0.99910…). At the seeded values:
- **lambda = 1/2**: (b1, b2) = (3/2, 1/2) admissible; slope exactly 2; kappa = 1/2; Y² coefficient
  −2.75 (shift +1/4); mu(∞) − 1 = 1/4; |Δmu(1)| = 1/16 = 0.0625.
- **lambda = 1**: boundary; b2 = 0 (channel 2 has no linear engagement); slope still exactly 2.
- **lambda = 2**: b2 = −1 < 0 — p2(Y) = −Y/(1+Y) < 0 for Y > 0 (not a fraction) yet the **total slope is
  exactly 2 and kappa = 1/2** (T4c): *slope equality does not determine the engagement structure* — the
  mandated asymmetric counterexample, live.
- Newtonian normalization discriminator: mu(∞) − 1 = lambda² exactly at all three values (T4d).

### General n ≥ 1 (symbolic)
mu_n'(0) = Σ_{i=1..n} b_i for the OR composition of n channels (T0b at n = 3,5); kappa = 1/S.
Equal unit channels: kappa = 1/n; n = 2 ⇒ kappa = 1/2 (the metric's count, PD01); n = 1 ⇒ kappa = 1.
Asymmetric redistributions of a fixed sum never move the coefficient (T6 for n = 1,2,3,7).

## 4. The mandated negative controls (capable of failing)

**Control A: "slope equality from kappa = 1/2 ⇒ same response" is FALSE.** Constructed counterexample:
eps = 1/2, rational class — slope 2 = slope of mu_2, yet mu ≠ mu_2 (quadratic coefficient −11/4 vs −3;
|Δmu(1)| = 1/16 > 0; Newtonian limit 5/4 vs 1). The control is *capable of failing*: for the power-law
completion class (T3) no counterexample exists — mu is pointwise-equal to mu_2 for every eps (exact
identity, residual 0). T2 ⇔ T3 is exactly the live/failed boundary of the control.

**Control B: limiting regimes / normalization / boundary.**
- Deep limit Y→0: slope exactly 2 in both completion classes, for all three lambda values (exact
  derivatives; independent Richardson finite differences, residuals ≈ 1e-24).
- Newtonian limit Y→∞: power-law mu(∞) = 1 exactly (normalization preserved for every eps); rational
  mu(∞) = 1 + eps² (normalization *fails* as the counterexample requires). Exact symbolic limits, not
  numerical extrapolation.
- Boundary cases: eps = 1 (b2 = 0, inert channel), eps = 2 (b2 < 0, inadmissible fraction), n = 1 and
  n > 2 — all checked.
- Exact identities are distinguished from finite numerics: T2 series, T3 collapse and T4 normalization
  deviations are exact algebra (0 residual); the finite-difference and mpmath witnesses are labelled as
  finite-consistency checks with their residuals recorded (≈1e-24 at 50 digits for Richardson;
  ≈1e-51/0.0 for the deep-Poisson substitution).

## 5. Secondary reading: scale asymmetry p_2(Y) = Y/(1+lam Y)

Alternative reading of the seed's "lambda": a one-parameter family where both channels keep unit slope
but the second channel's transition scale differs. Sympy: slope 2 for every lam (exact); mu(∞) = 1 for
every lam (normalization never broken — unlike slope asymmetry); first difference at quadratic order,
coefficient −(2+lam) vs −3 (shift 1−lam). At the mandated lambda grid: |Δmu(1)| = |1−lam|/(4(1+lam)) =
1/12, 0, 1/12 for lam = 1/2, 1, 2 (exact; verified at 50 digits). So *both* readings of the seed's
family share the same structure: the deep coefficient is immune; the response is not.

## 6. Numerical witnesses (actual residuals, 50-digit mpmath + exact sympy)

- T0a generic chain rule: symbolic residual 0 (exact).
- Richardson-extrapolated finite differences of the rational family at eps = 1/2, 1, 2 (50 digits, h = 1e-6,
  error floor ~h⁴ ≈ 1e-24): first three Taylor coefficients recovered with residuals
  ≈ 1.3e-24 / 2.9e-24 / 2.0e-22 (eps=1/2), ≈ 5e-25 / 1e-24 / 6.3e-23 (eps=1), ≈ 2.5e-24 / 6.5e-24 /
  5.0e-22 (eps=2) — actual residuals, not booleans.
- Footing hygiene: |s − c sqrt(G rho_Lambda)|/s = 0.0 exactly (mpf-decimal arithmetic, 50 digits) on both
  footings; deep-Poisson substitution residual r²·mu·g − GM over GM = 1.6e-51 (canonical) and 0.0
  (alternative) at g_N = a0/10 (M_b = 1e9 M_sun).
- Exact diagnostic values (lambda = 1/2, 1, 2): slope 2.0 (all); Y² coefficients −2.75, −2.0, +1.0;
  mu(∞)−1 = 0.25, 1, 4; |Δmu(1)| = 0.0625, 0.25, 1.0 — each equality verified to < 1e-45 where non-dyadic.
- Secondary reading: 1/12, 0, 1/12 checked to < 1e-45.

## 7. Lean 4 certificate

File: `AS064_channel_asymmetry.lean` (self-contained, in this directory; compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>`; **no files were written into the Lean
project directory** — probe compilation artifacts were removed; compile host only).

Certified theorems (all `namespace AS064`):
- `rational_closed_form` — exact closed form of the asymmetric rational response;
- `rational_slope_two` — punctured-neighbourhood limit lim_{x→0, x≠0} mu(x)/x = 2 (slope-2 invariance of
  the concrete family, all eps);
- `rational_quadratic_coefficient` — lim (mu(x)−2x)/x² = −3+eps² on the punctured neighbourhood
  (first visible order quadratic; shift eps²);
- `powerlaw_collapse` — 1−(1−p1)(1−p2) = 1−(1+x)^(−(b1+b2)) (exact invisibility class);
- `kappa_half_from_scale` — a0 = s/2 ⇒ a0/s = 1/2 (matching-chain landing);
- `normalization_decomposition` — (1−p1)(1−p2)(x) = −eps² + 2eps²/(1+x) + (1−eps²)/(1+x)² (exact
  Newtonian-limit anomaly algebra; mu(inf)−1 = eps² then follows and is verified exactly by sympy
  T2c/T4d).

Verification result: **compile exit 0; zero sorry; unfiltered `#print axioms` of all six theorems =
[propext, Classical.choice, Quot.sound]** (subset requirement satisfied; full list in
`lean_compile_and_axioms.txt`).

**Lean-scope limitation (recorded):** the fully-general chain-rule theorem
`HasDerivAt (fun x => 1-(1-p1 x)*(1-p2 x)) (a1+a2) 0` for *arbitrary* completion functions is NOT Lean-
certified. In this lean_2026 bundle (Lean 4.34.0-rc2), (i) function-space subtraction/multiplication
terms fail to elaborate when applied to an argument unless type-annotated, and (ii) HasDerivAt statements
reached through the tactic machinery carry a different AddCommGroup class instance
(Real.normedAddCommGroup.toAddCommGroup) than user-written HasDerivAt statements
(Real.instAddCommGroup), which no convert/simpa/exact bridge closes (attempted and recorded).
The mathematical content is covered by other means: generic symbolic differentiation in sympy (T0a,
residual 0), the exact closed form (Lean `rational_closed_form`), and the two Lean limit certificates
above for the concrete family. The carrier-level statement of PD01/PD08 (slope = channel count) is
untouched by this scope restriction.

## 8. Strongest surviving statement

**(S) Asymmetry invariance of the deep coefficient.** For the OR-class two-channel response with
per-channel engagements p1, p2 satisfying p_i(0) = 0 and p_1'(0) + p_2'(0) = 2, the deep-MOND slope is
exactly 2 and the framework matching chain gives kappa = 1/2 exactly, for *every* completion and *every*
asymmetric split b1 = 1+eps, b2 = 1−eps: **d kappa/d eps ≡ 0**.
- Responsely, asymmetry is *first visible at quadratic order* for rational completions, with
  dimensionless coefficient shift +eps² and Newtonian normalization deviation mu(∞)−1 = eps²; it is
  *invisible at every order* for power-law completions (mu ≡ mu_2 identically).
- Admissible asymmetry domain: eps ∈ (−1,1); eps = 1 is the inert-channel boundary; eps = 2 is the
  explicit counterexample showing slope-2 does not determine the response.
- Both footings: the dimensionless statement is proved once; per-footing transition bands quoted in §3.
  Domain of the deep form mu ≈ 2Y: |(mu−2Y)/2Y| ≈ ((3−eps²)/2)·Y + O(Y²), i.e. ≤ ~14% at Y = 0.1,
  ≤ ~1.4% at Y = 0.01 (eps ≤ 1/2); the leading neglected term is −(3−eps²)Y² down to O(Y³).

## 9. What this does NOT establish (limitations)

1. kappa = 1/2 remains **adopted**, not derived (the seed supplies no independent argument; PD01/PD08's
   conditional derivation with its OR-identification premise is the corpus's status quo; the k01
   zero-mode no-go is on record).
2. The exact completion (shape) of mu(Y) is not obtained: asymmetry funnels a genuinely free degree of
   freedom (b1−b2, or the scale ratio lam) into the finite-Y response — invisible to the coefficient.
3. A priori each completion class is one-parameter (p = bY/(1+Y) or 1−(1+Y)^(−b)); two-degree families
   would interpolate between the exact-invisibility and first-order-visibility cases; nothing here rules
   out mixed classes.
4. No transfer to the operative filtered-MONO target (criterion B): no kernel/filter/derivative
   statements; the counterexample family is labelled conditional on its own boundary conditions.
5. The Lean scope restriction of §7: the general chain rule is machine-verified symbolically/numerically,
   not Lean-certified in full generality.
6. Numerical results are finite witnesses of exact algebra (all closed forms are exact); no observational
   data were used (per the seed: no observational preference as proof).

## 10. Closure implication, gate, branching

- **Affected operative gate:** the CORE coefficient selection lane A03/PD01-D1 (the OR-identification
  premise) feeding the MU2-family conditional statements. Exact implication for a common-action closure
  witness: *any* candidate two-channel action whose OR response splits as b1 = 1+eps, b2 = 1−eps with
  b1+b2 = 2 reproduces the adopted kappa = 1/2 at deep order (a0 = s/2) with zero added physics, and is
  constrained at finite Y by the quadratic shift eps²·(g/s)² (rational class) — screening candidates
  against kernel/shape data (the L231-type kernel comparison is exactly such a finite-Y diagnostic).
- **No branch translation performed:** the result is a statement about the OR/MU2-family response; the
  seed's declared branch is CORE coefficient / conditional MU_n statistical response; Q / RAR / EXP /
  MONO numbers are not quoted.
- **First additional implication needed to transfer:** a principle fixing the asymmetry parameters
  (b1−b2) or (lam) from the carrier dynamics — e.g. the relative weights of the metric's two static
  channels (PPN-type ratio) — plus the actual finite-Y (kernel) diagnostics; without it the shape
  freedom quantified here remains open.

## 11. Failed attempts (preserved in the run history)

- sympy `solve`/`solveset` on the admissibility conjunction: refused (ValueError, recorded verbatim in
  raw_output.txt); replaced by grid scan with stated step. (Script-level only, not a scientific failure.)
- Lean: the general HasDerivAt chain rule, the `convert`/`simpa`/`exact` bridges, and the nhds-based
  (unpunctured) limit formulation all failed as documented in §7 — each attempt preserved in the run
  directory edits; final certificate compiles clean with the stated axioms.

## 12. Reproducibility

- `AS064_channel_asymmetry.py` — all algebra + numerics; `raw_output.txt` — full log (28/28 checks PASS,
  exit 0); `residuals.json` — machine-readable checks and bounds (wall 0.256 s vs 120 s SIGALRM cap;
  peak RSS ≈ 84.5 MB vs 512 MB; 1 thread); `stderr_time.txt` — /usr/bin/time report.
- `AS064_channel_asymmetry.lean` + `lean_compile_and_axioms.txt` — formal certificate (exit 0, axioms as
  listed).
- Execution bounds actually enforced: SIGALRM 120 s (in-process), 1 thread by construction; memory was
  NOT OS-enforced (macOS RLIMIT_AS refusal precedent — recorded in bounds) but measured peak ≈ 84.5 MB.