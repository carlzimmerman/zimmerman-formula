# AS050 (REDO, authoritative run r2) — "A branch-specific primitive cannot fix its zero"

**Seed:** `deepseek_push/astra_spawn_ideas/AS050_a_branch_specific_primitive_cannot_fix_its_zero.md`
sha256 = `db6efad6ff61cc21a73a9ca913dad9a3190881b9f2bebee1f65f4d69da37c717` (verified; matches task pin).
This run supersedes `run_AS050-r1-*`, which executed the wrong text (AS028's seed, task_sha256 mismatch).
**Run dir:** `deepseek_push/astra_spawn_ideas/results/AS050/run_AS050-r2-20260928T070836Z-dsv4f-hermes/`

Claim under test (seed "Mathematics and principal test"):

> If F′(X) = μ(√X), then F(X) + C has identical static constitutive response.

Group A02 (constitutive kernels and branch fidelity). Outcome of this run: **supports_scoped_claim**.

---

## Step 1 — Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim (scoped).** Let X = x², x = g/a₀ ∈ (0, ∞), y = B/a₀ ∈ (0, ∞) be dimensionless
acceleration-squared, acceleration ratio and field-source ratio (B ≡ g_N = Newtonian
acceleration of the source). Let μ_b denote the static constitutive response of branch
b ∈ {Q, RAR, MU2, EXP, MONO}, i.e. the target-space function such that the primitive
F_b satisfies F_b′(X) = μ_b(√X) on its branch domain. Then for every C ∈ ℝ the
C-shifted primitive F_b + C has the **identical** static constitutive response:
(F_b + C)′(X) = F_b′(X) = μ_b(√X) pointwise on the branch domain. Consequently no
branch-specific primitive can fix its own zero: the choice F(0) = (any number) is a
normalization, invisible to every static constitutive observable x(y), μ(y), and to
the static filtered field equation.

**Dictionary (per FRAMEWORK_CONTRACT.md, exercised per branch — criterion B, all five
branches kept distinct):**

| branch | response law (y, x) | μ(√X) = dF/dX | primitive F(X) (closed form where elementary) |
|---|---|---|---|
| Q | x² = y² + y (x = √(y²+y)) | μ_Q(s) = (√(1+4s²) − 1)/(2s) | F_Q(X) = (s/2)·√(1+4X) + (1/4)·ln(2s + √(1+4X)) − s |
| RAR | x = y/(1 − e^{−√y}) (y = X) | μ_RAR(X) = y/x(y) (non-elementary in X; y-parametrized) | F_RAR(X) = ∫₀^X μ_RAR(u) du via y-quadrature |
| MU2 | y = x·μ2(x), μ2(x) = 1 − (1+x/2)^{−2} | μ_MU2(s) = 1 − (1+s/2)^{−2} | F_MU2(X) = X − 8·ln(1+s/2) − 8/(1+s/2) |
| EXP | y = x·(1 − e^{−x}) (historical AQUAL) | μ_EXP(s) = 1 − e^{−s} | F_EXP(X) = X + 2(1+s)e^{−s} |
| MONO | operative filter: ν_mono = 1 + h_mono/y, h = RAR-based bump(DELTA·h_p/(y+y_p)) with measured crossing at y★, μ = y/x(y) (non-elementary in X) | μ_MONO(X) = y/x(y) | F_MONO(X) = ∫₀^X μ_MONO(u) du via y-quadrature |

s = √X, w = √(1+4X). All branches: y = B/a₀ > 0, x = g/a₀ > 0, X = x² > 0.

**Framework inputs (adopted, not derived here):** κ = 1/2 (a₀ = κ·c·√(G·ρ_Λ)); G =
6.67430e-11 m³ kg⁻¹ s⁻²; c = 299792458 m/s; M_sun = 1.98847e30 kg; pc =
3.085677581491367e16 m. Both footings kept separate throughout:
canonical a₀ = **9.3619e-11 m/s²** and alternative a₀ = **1.1279e-10 m/s²** (see
framework cell in Step 3 — they cannot share both fixed density and fixed κ; with
κ = 1/2 the two footings give ρ_Λ = 5.844e-27 and 8.483e-27 kg/m³, ratio 1.45149, and the
alternative footing at the canonical density implies κ_eff = 0.60239).

**Assumptions (new/independent, all stated):** (A1) branch dictionary exactly as in
FRAMEWORK_CONTRACT (no mixing of branches); (A2) C ∈ ℝ is an additive constant on F
(the ELE potential's static side), constant in spacetime at the static level;
(A3) static observables are x(y), y(x), μ(y) — no dynamical probes in this task;
(A4) μ_b(√X) primitive exists on the declared domain (X > 0; also X = 0 for the
conventions theorem).

## Step 2 — Static invariance; what changes when C is coupled dynamically

**Algebraic core (generic, certified in Lean 4 — file
`AS050_primitive_zero_invariance.lean`, theorem `shift_invariant_derivative`):**

(F + C)′ = F′ at every X where F is differentiable, for any C ∈ ℝ. Proof in Lean:
`(hasDerivAt_const X C)` + pointwise-add chain rule + `add_zero`. No branch content is
used — the invariance is generic; the branch content is the identity F_b′ = μ_b(√·),
certified for the three elementary primitives (theorems `exp_primitive_deriv`,
`mu2_primitive_deriv`, `q_primitive_deriv`) and verified numerically for the
non-elementary branches (RAR, MONO) by quadrature.

**Numerical verification (actual residuals, Decimal(60)):**
C ∈ {−2, 0, 3, 10⁷} on branches Q, EXP, MU2 — max |(F+C)′ − F′| = **2.75e-37**
(tol 1e-20, pass). RAR/MONO invariance via y-parametrization (quadrature consistency,
below): max rel 3.40e-5 (tol 1e-3, pass).

**Static field-equation control (ELE shift control):** the static filtered field
equation's residual computed from Φ(r) and Φ(r) + 7.3 is unchanged:
max|Δres| = 2.366e-08 on norm 3.79e5 → relative shift **6.24e-14** (tol 1e-10, pass).
The additive constant is invisible to the static filter.

**What changes dynamically.** If the same constant is coupled to a dynamical metric
(e.g. the potential enters the Friedmann sector as a constant vacuum-energy offset),
the extra vacuum condition needed is

Δε_vac = [a₀²/(8πG)]·C  (J/m³ per unit C),
Δρ_vac = C·a₀²/(8πGc²)   (kg/m³ per unit C).

Numerical content (Step 5 of the seed's controls; `vacuum_constant_content`):
canonical footing: per-unit-C energy density 5.2250e-12 J/m³; the historical
EXP/SPEC requirement-12 normalization C = −2 (G(y) = y² + 2(1+y)e^{−y} − 2) shifts the
vacuum energy by −1.0450e-11 J/m³ (≈ 2.0% of ε_Λ = 5.2527e-10 J/m³);
alternative footing: per-unit-C 7.5840e-12 J/m³, C = −2 shift −1.5168e-11 J/m³
(ε_Λ = 7.6242e-10 J/m³). So the constant is a vacuum-density datum, not a static
observable — the Friedmann constraint is the first place that sees it.

## Step 3 — Intermediate algebra: factors, signs, units

All scale factors and signs are carried explicitly (X > 0, s = √X, w = √(1+4X), so
ds/dX = 1/(2s), dw/dX = 2/w).

**Q.** d/dX F_Q:
d/dX[s·w/2] = (1/2)(s′w + s w′) = w/(4s) + s/w;
d/dX[(1/4)·ln(2s+w)] = (1/4)(2s′ + w′)/(2s+w) = (1/4)(1/s + 2/w)/(2s+w) = (w+2s)/(4s·w·(2s+w));
d/dX[−s] = −1/(2s).
Sum, over the common denominator 4s·w·(2s+w), equals (w−1)/(2s): the certified
multiplied-out identity is

4·(w² + 4s²)(2s+w) + 2(2w+4s) − 8w(2s+w) = 8w(2s+w)(w−1),

which reduces with w² = 1+4s² to an exact ring identity (verified numerically
`deep_limit_Q_exact` ≤ 3.2e-16 and certified in Lean, incl. the mul_self_sqrt steps).
Result: F_Q′ = (w−1)/(2s) = μ_Q(s) ✓ (units: 1/X, dimensionless).

**EXP.** g(s) = 2(1+s)e^{−s}: dg/dX = 2[(e^{−s} − (1+s)e^{−s})]·(1/(2s)) = −e^{−s}.
F_EXP′ = 1 + dg/dX = 1 − e^{−s} = μ_EXP(s) ✓.

**MU2.** d[−8 ln(1+s/2)]/dX = −8·(1/(4s))·(1/(1+s/2)) = −2/(s(1+s/2));
d[−8(1+s/2)⁻¹]/dX = 8·(1/(4s))·(1+s/2)⁻² = 2/(s(1+s/2)²).
F_MU2′ = 1 − 2/(s(1+s/2)) + 2/(s(1+s/2)²) = 1 − (1+s/2)⁻² = μ_MU2(s) ✓.

**RAR / MONO (non-elementary in X).** x = x(y), μ = y/x(y); dX/dy = 2x(y)x′(y);
F(X(y)) = ∫₀^y μ(y′)·2x(y′)x′(y′) dy′; dF/dX = (dF/dy)/(dX/dy) = μ ✓ (chain rule;
computed by Simpson quadrature n = 20000 → 40000 refinement, integrand stored).

**Zero-convention theorem.** The two normalizations of the EXP primitive (C = −2,
the SPEC requirement-12 convention with G(0) = 0, and C = 0) **differ at X = 0**
(theorem `exp_zero_conventions_differ`, norm_num) but **share the constitutive
derivative at every X > 0** (theorems `exp_zero_conventions_same_derivative`,
`shift_invariant_derivative`). Hence the "zero" of the primitive is movable — the seed
name is exact.

## Step 4 — Independent checks (different representations, actual residuals)

1. **Direct differentiation vs closed form** (`derivative_closed_form`, Decimal(60),
   symmetric difference h = 1e-6·X): max rel over {Q, EXP, MU2} = 5.28e-14
   (pre-set tol 1e-10, pass).
2. **Quadrature (different representation) for RAR and MONO**
   (`quadrature_RAR_MONO`, Simpson, integrand μ·2x x′): max |dF/dX − μ|/|μ| = 3.40e-5
   (tol 1e-3, pass).
3. **Response-consistency by inversion** (fp64 and Decimal(60) deep): for each branch,
   forward map x(y) → μ(y) → invert to recover y and μ; max abs residual 5.55e-17
   (fp64, tol 1e-12) and 7.59e-17 (Decimal deep, tol 1e-16) — actual residuals saved
   in `raw_output.json`, not booleans.
4. **Lean 4 certificate** (`AS050_primitive_zero_invariance.lean`, 218 lines): six
   theorems, zero `sorry`, axioms exactly {propext, Classical.choice, Quot.sound}
   verified via `#print axioms` on all six theorems. Compiled host-only from
   `fable_independent_2026/lean_2026`: `timeout 580 lake env lean <abs>/…lean` → exit 0.

## Step 5 — Negative controls (capable of failing) and surviving statement

**Control 1 — "Treat F(0) = a chosen number as a derived field equation and reject
the claimed coefficient derivation."** Attempt to derive C from the static
constitutive observables: build the observable table (branches Q/EXP/MU2 × X at the
grid endpoints) for C ∈ {−2, 0, 3, 10⁷} and compute the per-column population
variance. Observed max column variance = **0.0** (tol 1e-20): the observables contain
F nowhere; F(0) is strictly underdetermined by static data. The control therefore
**rejects** any static derivation of a coefficient from F(0) — exactly as required,
and it is capable of failing (any C-dependence > 1e-20 would fail it).

**Control 2 — deep and Newtonian limiting regimes.**
Deep (y ≤ 1e-4): Q is exact (x² = y + y², residual ≤ 3.2e-16); RAR, MU2, EXP, MONO
follow x²/y − 1 ≈ c·√y with measured leading coefficients c = 1.0004, 0.7503, 0.5002,
1.0004 (theory: RAR c=1, MU2 c=3/4, EXP c=1/2 — each branch distinct, criterion B) and
log–log slope 0.5003–0.5004 (exponent 1/2).
Newtonian (y ≥ 100): Q: x − y → 1/2 exactly (measured 0.5 at y = 10⁸);
RAR/EXP: x − y → 0 (e^{−√y} decay, measured 0.0); MU2: 4.5e-8 (numeric floor of
1/y²-tail); MONO: by construction the operative filter continues beyond the bump with
a logarithmic offset (x − y → 1.19 at 10⁸) — this is a design property of the MONO
continuation, not a Newton-limit failure; flagged in limitations.

**Strongest surviving statement (domain: all five branches, y ∈ [1e-10, 10⁸]
grid in steps of 10^0.1, X > 0, C ∈ ℝ noticed through {−2, 0, 3, 10⁷}):**
For each branch of the dictionary, every F + C has the identical static constitutive
response; F(0) is unobservable statically; C is fixed only by dynamics through the
vacuum condition Δρ_vac = C·a₀²/(8πGc²). The seed claim is **supported** as a scoped
conditional statement: the fight "a branch-specific primitive cannot fix its zero"
holds — a primitive's zero is a normalization datum, never a static coefficient
derivation — while a₀ = (c/2)√(Gρ_Λ) remains the adopted framework input (κ = 1/2 not
derived here).

**Bounds (actually enforced, recorded in `raw_output.json`["bounds"]):**
wall: 120 s hard self-deadline (`check_wall` before each phase; observed 12.30 s) —
enforced; memory: RLIMIT_AS = 512 MB attempted, **refused by macOS**
(ValueError: current limit exceeds maximum limit) → NOT enforced; observed peak RSS
15.3 MB (ru_maxrss, bytes on macOS → 15632 KB); threads: 1 (stdlib, single-threaded
by construction) — enforced by construction.

## Files

- `AS050_compute.py` — bounded prototype (stdlib only), all checks, exit 0.
- `raw_output.json` — all numeric outputs (grid, landmarks, residuals, checks,
  framework cell, vacuum content, bounds).
- `run.log` — clean run transcript.
- `AS050_primitive_zero_invariance.lean` — Lean certificate (six theorems, no sorry).
- `AS050_axiomcheck.lean` — certificate + `#print axioms` appended; prints exactly
  `[propext, Classical.choice, Quot.sound]` for all six theorems.
- `result.json` — campaign result per RESULT_CONTRACT.json.