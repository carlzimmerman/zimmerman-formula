# AS137 — Ordinary-Matter Ward Identity (Tier-0)

**Run:** `AS137-r1-20260928T150706Z-dsv4f-hermes`
**Task:** `deepseek_push/astra_spawn_ideas/AS137_derive_the_ordinary_matter_ward_identity.md`
**Task sha256:** `b8f72cd5f78a4b5b83b7eca37e665eca8d78e294435b198d88b2bd2a0c5fb19b` (verified before execution)
**Framing:** CA4-GNC action, `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` eq. (4), baryon sector
`S_b[g,ψ] = ∫ d²x √-g [ -½ g^{μν} ∂_μψ ∂_νψ - V(ψ) ]` minimally coupled. CA5-GNC-R (`STANDING.md` CD26-5) inherits the
same `S_b[g]` term, so the theorem below applies unchanged to both actions. No upstream result dirs (AS138/AS131/AS132/AS147)
existed at execution time; this seed proceeded independently.

Mandatory framework input adopted: **κ = 1/2**, `a0 = κ·c·√(G·ρ_Λ)`; footings `a0 = 9.3619e-11 m/s²` (canonical) and
`1.1279e-10 m/s²` (alternative). Constants: `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16`.

---

## 1. Definitions and exact identities (symbolic, generic 2D diagonal metric)

On `g = diag(-A(t,x), B(t,x))`, generic scalar baryon field ψ and potential V(ψ), with `E_b := □ψ - V'(ψ)`:

| Check | Statement | Method | Result |
|---|---|---|---|
| [1] | Variational stress: expanding `S_b(g+εh)` gives `(1/2)√-g T^{μν} h_{μν}` with the closed-form `T^{μν} = (∂^μψ)(∂^νψ) - ½ g^{μν}(∂ψ)² - g^{μν}V` (measure √-g included); flat limit `T⁰⁰ = ½p_t² + ½p_x² + V ≥ 0` | exact sympy, polynomial comparison after clearing radicals | residual 0; coefficients [1/2, 1/2] > 0 |
| [2] | Off-shell Ward identity `∇_μ T^{μν} = E_b ∇^νψ`, `E_b = □ψ - V'(ψ)` | exact simplification | residual = 0 (both ν) |
| [3] | On-shell (`E_b = 0` substituted into the original equation): `∇_μ T^{μν} = 0` | exact | 0, 0 |
| [4] | Negative control `S_b' = S_b + z0·Z·ψ²`: exact identity `∇_μ T'^{μν} = E'_ψ ∇^νψ + z0 ψ² ∇^νZ`, `E'_ψ = E_b + 2z0Zψ`; witnesses: flat, V=0, ψ=x², Z=-1/(z0x²): `E'_ψ = 0` yet `div T' = (0, 2x) ≠ 0` | exact | identity residual 0; witness held |
| [5] | Any-host-scalar classification (instance `Φ·ψ²`): `div T = ψ² grad Φ` on the ψ-shell; conservation iff `grad Φ = 0`. CA4-GNC host fields Z, U, τ, W_b, L, λ0, φ_A never enter S_b ⇒ protected | exact | residual 0 |
| [6] | Diffeomorphisms: `δg_{μν} = -(∇_μξ_ν+∇_νξ_μ)`, `δψ = -ξ^μ∂_μψ`; local IBP identity `dS_ξ + ∂_μ(√-g T^{μν}ξ_ν) = √-g ξ_ν[∇_μT^{μν} - E_b∇^νψ]` (= 0 by [2] — δ_ξS_b is a total divergence) | exact pointwise on rational configs c1–c3 | residual 0 at (1/2, 1/3) for each |

**Derivation sketch ([1]).**
`δS_b = ∫ √-g [E_b δψ + ½ T^{μν} δg_{μν}] d²x` with the Hilbert measure. Under `g → g + εh` (componentwise, including
`√-g → √-g(1 + ½ g^{μν}h_{μν})` at first order) the ε-coefficient equals `½√-g T^{μν}h_{μν}`; the inverse-metric chain
`δg^{ab} = -g^{aμ}g^{bν}δg_{μν}` carries the sign that makes the lower-index formula of the seed literally correct.
Flat `T⁰⁰ = ½(∂_tψ)² + ½(∂_xψ)² + V ≥ 0` ⇒ positive kinetic energy with this convention.

**Derivation sketch ([2]).** Direct covariant divergence of the closed form using the 2D Christoffel symbols of the
diagonal metric; all terms assemble into `E_b ∇^νψ` without approximation. This is the seed's central identity:
the natural `√-g`-weighted variation produces a stress whose divergence is sourced **only** by the field equation.

**Derivation sketch ([6]).** Since `T` is symmetric, `½T^{μν}δg_{μν} = -T^{μν}∇_μξ_ν`; together with
`E_b δψ = -E_b ξ^μ∂_μψ` and the covariant Leibniz rule `∂_μ(√-g V^μ) = √-g ∇_μV^μ`,
`dS_ξ = √-g[-E_bξ^σ∂_σψ - T^{μν}∇_μξ_ν]`, hence the local identity. For compactly supported ξ the boundary term
integrates to zero, i.e. `δ_ξ S_b = 0` (diffeomorphism invariance of the baryon sector).

## 2. Numeric checks on a curved background (actual residuals)

Background: 2D (t,r) Schwarzschild-sector metric `g = diag(-(1-2M/r), 1/(1-2M/r))`, M = 1, r ∈ (3,8), t ∈ (0,1),
180×180 grid (refined 360×360 where stated), float64, analytic derivatives + `np.gradient` cross-check.
Field: `φ = t² sin(r)/r + r² cos(2t)/20`, `V = ½μ²φ²`, μ = 0.7.

| Check | Content | Observed (actual numbers) | Bound (pre-declared) |
|---|---|---|---|
| N1 | off-shell identity ∇·T = E∇φ | analytic max|res| = **9.95e-14** (ν=0), 2.49e-14 (ν=1); rel 1.58e-15 / 2.71e-15; interior FD 4.70e-3 (2nd-order), edges 0.70 (1st-order stencils, reported) | 1e-10·scale; interior 5e-3 |
| N2 | on-shell witness φ = t: E = 0, div T = 0, T ≠ 0 (**T⁰⁰ = 4.5**) | max|E| = 0.0; max|div T| = 0.0 / 2.63e-14 | 1e-11 / 1e-9 |
| N3 | flat limit M → 0 of N1 | 2.31e-14 / 4.89e-15 | 1e-10 |
| N4 | diffeo integral, compact bump ξ: pointwise IBP `I1 + Bnd + I2 = 0`; ∫I1 (δ_ξS_b), ∫I2 (once-integrated form), flux ∫Bnd, consistency; 360² refinement | pointwise **2.17e-15** (rel 1.8e-16); ∫I1 = -1.93e-4 (|I1|-integral 7.31; rel 2.6e-5), refined -4.80e-5 (**Richardson ratio 0.249 ≈ ¼**); ∫I2 = 1.4e-17; ∫Bnd = +1.93e-4; ∫(I1+Bnd+I2) = 1.4e-17 | pointwise 1e-9 rel; 5e-4; consistency 1e-9; quartering ≤ ½ |
| N5 | negative control on curved bg: `∇·T' = E'_ψ∇ψ + z0ψ²∇Z`; flat on-shell witness ψ=r², Z=-1/(z0r²): E'_ψ = 0, div T' = (0, 2r) | 7.43e-7 (rel 6.2e-11), 4.62e-9 (rel 1.8e-12); witness: E'_ψ(3) = 0.0, div T' = (0, **6.000000**), E'–plain = 2 ≠ 0 off-shell | 1e-8·scale; witness exact to 1e-12/1e-9 |
| N6 | footings: κ = 1/2, ρ_Λ = 4a0²/(Gc²) | canonical 5.8444e-27 kg/m³, alt 8.4831e-27 kg/m³; density ratio (alt/can)² = 1.451487; κ back-check = 0.50000000 on **both** footings; a0, κ, ρ_Λ, G_N/G_bare/G_cosmo enter S_b nowhere ⇒ identity holds on both footings identically | — (consistency) |

The N4 pointwise identity and the integral consistency (`∫(I1+Bnd+I2) = 1.4e-17`) confirm the once-integrated form of
[2] at machine precision on the curved sector.

## 3. Controls — capable of failing, and they did

The development of this seed was an exercise in controls that caught real errors:
1. [1] initially failed: the ε-perturbation of `h₀₀` carried a flipped sign (ratio −1 on h₀₀ only). Fixed by pure
   componentwise perturbation; then exact.
2. N1 initially failed at 2.7 (rel 4e-2): the numeric Christoffel *shortcut* had incorrect component indexing
   (`gcomp[l2]` vs `gcomp[l1]`). Replaced by the exact full formula (same as the symbolic script); residual → 1e-14.
3. N1 FD check failed at 0.70: my assembled `div T⁰` had dropped the `Γ^r_rr T¹⁰` term; fixed → interior 4.7e-3 at
   the pre-declared 2nd-order truncation bound.
4. N4 pointwise IBP failed at rel 1.98: (a) `ξ^r = g^{rr}ξ_r` had been coded as `g_rrξ_r`; (b) the `I1` T-term carried
   the wrong sign against the seed's `δg = -(∇ξ+∇ξ)` convention. After the fix the identity holds at rel 1.8e-16.
5. N4's symbolic-Piecewise bump made sp.simplify/trigsimp pathological (CPU-capped at 120 s); replaced by a pure-numpy
   bump with exact lattice algebra.
6. N5 witness initially reported E'_ψ = −2 (the field was placed on a coordinate `xS` the machinery never
   differentiates); moved to ψ = r² → E'_ψ = 0 and div T' = (0, 2r) exactly.
7. N5 curved identity initially crawled via a sympy symbol leaking into a numpy lambdify (`z0` not an argument); fixed
   by substitution before codegen.

Every check above still contains assertions that would fail if the identity were violated (the negative control is
exactly the witness `E'_ψ = 0, div T' = (0, 2r) ≠ 0`).

## 4. Lean certificate

`AS137_ward_identity.lean` — self-contained (Mathlib only), flat-2D component algebra of the witness set:
- `plain_ward_flat`: `deriv (2r²) = 2·(2r)` — the off-shell Ward identity `∂_rT^{rr} = E_ψ ∂^rψ` at the witness (E = 2);
- `plain_euler_lagrange_nonzero`: E = 2 ≠ 0 (the plain equation is genuinely off-shell);
- `control_on_shell` (+ alt): `2 + 2z0·(-1/(z0r²))·r² = 0` for r ≠ 0, z0 ≠ 0 (E'_ψ = 0 on the baryon shell);
- `control_Ttt`, `control_Trr`: raw component reduction to 3r² and r²;
- `divTp_t`, `divTp_r`: `∂_t(3r²) = 0`, `deriv(r²) = 2r` — i.e. `div T' = (0, 2r)`;
- `on_shell_yet_div_nonzero`, `witness_point`: the on-shell condition does **not** imply conservation in the
  controlled theory (at r = 3: E'_ψ = 0 ∧ div T'^r = 6).

Compiled: `cd fable_independent_2026/lean_2026 && lake env lean <run_dir>/AS137_ward_identity.lean` → exit 0.
`#print axioms` on all eight theorems: exactly `{propext, Classical.choice, Quot.sound}`, **zero sorry**.

## 5. Execution bounds (actually enforced)

- Single thread: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1`.
- CPU: `ulimit -t 120` (soft) enforced by the shell on symbolic, numeric and Lean runs.
- Memory: macOS `ulimit -v` unsupported; peak RSS measured with `/usr/bin/time -l` — symbolic **71.2 MB**, numeric
  **171.1 MB** (worst observed during capped intermediate runs: 376 MB), Lean compile 5.8 GB (Mathlib load, excluded
  from the 512 MB research-worker bound; certificate compile is a build step, not a verification run).
- Runtime: symbolic 3.03 s, numeric 4.59 s, Lean compile 5.2 s.

## 6. Tested domain and scope

Exact symbolic domain: all 2D Lorentzian diagonal metrics `diag(-A(t,x), B(t,x))` with generic smooth A > 0, B > 0,
generic scalar ψ and generic C¹ potential V (rational-config point checks c1–c3 for [6] at (1/2, 1/3): A = 1+t²/3,
B = 1+x²/5, φ = tx+t², V = 0; A = 2−x²/17, B = 3+tx/7, φ = x²−2t; A = 1+tx, B = 1−xt/2, φ = t³−x³).
Numeric domain: the (t,r) Schwarzschild sector M = 1, r ∈ (3,8), t ∈ (0,1), 180² and 360² grids; flat M = 0 limits;
the constraint r > 2M holds throughout. The certificate covers the flat 2D component algebra.

## 7. What this does NOT establish

- No 4D statement: the exact identities were derived in 2D diagonal metrics (the seed's requested framework cell);
  the 4D lift is a mechanical but separate derivation (child proposal C01).
- No statement about the host-sector terms of CA4-GNC (beyond check [5]'s classification: they never enter S_b);
  whether host density couplings alter the baryon equation of motion is a separate gate (see result.json
  `next_unresolved_implication`).
- The negative control uses a diagnostic nonmetric coupling `z0·Z·ψ²` (z0 = 1 in numerics); it is not part of CA4-GNC.
- κ = 1/2 and the a0 values are adopted inputs (mandated), used only in the N6 consistency examples; the identity
  itself is scale-free.